"""
K8s Ops Platform - Backend
Kubernetes 自动化运维平台后端服务
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import json
import redis
import asyncio

app = FastAPI(
    title="K8s Ops Platform API",
    description="Kubernetes Operations Management Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Kubernetes client
try:
    config.load_incluster_config()
    print("Loaded in-cluster config")
except:
    config.load_kube_config()
    print("Loaded kube config")

v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
autoscaling_v2 = client.AutoscalingV2Api()

# Redis for caching
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

# ============== Models ==============

class NamespaceInfo(BaseModel):
    name: str
    status: str
    pods_count: int
    created_at: Optional[str] = None

class PodInfo(BaseModel):
    name: str
    namespace: str
    status: str
    node: str
    ip: str
    cpu_request: str
    memory_request: str
    created_at: Optional[str] = None

class DeploymentInfo(BaseModel):
    name: str
    namespace: str
    replicas: int
    ready_replicas: int
    image: str
    created_at: Optional[str] = None

class HPAConfig(BaseModel):
    name: str
    namespace: str
    min_replicas: int
    max_replicas: int
    current_replicas: int
    target_cpu_utilization: Optional[int] = None
    target_memory_utilization: Optional[int] = None

class HPACreateRequest(BaseModel):
    name: str
    namespace: str
    target_deployment: str
    min_replicas: int = 2
    max_replicas: int = 10
    target_cpu_utilization: int = 70

class LogQuery(BaseModel):
    namespace: str
    pod_name: Optional[str] = None
    container: Optional[str] = None
    lines: int = 100
    since: Optional[str] = None

class CostEstimate(BaseModel):
    namespace: str
    cpu_cost: float
    memory_cost: float
    total_cost: float
    currency: str = "CNY"

class AlertRule(BaseModel):
    name: str
    namespace: str
    metric: str
    threshold: float
    comparison: str  # gt, lt, eq
    action: str  # email, webhook, slack

# ============== Health & Metrics ==============

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        v1.get_api_resources()
        k8s_status = "connected"
    except:
        k8s_status = "disconnected"
    
    try:
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"
    
    return {
        "status": "healthy",
        "service": "k8s-ops-backend",
        "kubernetes": k8s_status,
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics"""
    return {
        "service": "k8s-ops-backend",
        "requests_total": 0,
        "k8s_api_calls": 0
    }

# ============== Namespace Management ==============

@app.get("/api/v1/namespaces", response_model=List[NamespaceInfo])
async def list_namespaces():
    """获取所有命名空间"""
    try:
        namespaces = v1.list_namespace()
        result = []
        
        for ns in namespaces.items:
            pods = v1.list_pod_for_all_namespaces(field_selector=f"metadata.namespace={ns.metadata.name}")
            
            result.append(NamespaceInfo(
                name=ns.metadata.name,
                status="Active" if ns.status.phase == "Active" else "Terminating",
                pods_count=len(pods.items),
                created_at=ns.metadata.creation_timestamp.isoformat() if ns.metadata.creation_timestamp else None
            ))
        
        return result
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/namespaces/{namespace}/pods", response_model=List[PodInfo])
async def list_pods(namespace: str):
    """获取命名空间下的所有 Pod"""
    try:
        pods = v1.list_namespaced_pod(namespace)
        result = []
        
        for pod in pods.items:
            result.append(PodInfo(
                name=pod.metadata.name,
                namespace=namespace,
                status=pod.status.phase,
                node=pod.spec.node_name or "N/A",
                ip=pod.status.pod_ip or "N/A",
                cpu_request=get_resource_request(pod, "cpu"),
                memory_request=get_resource_request(pod, "memory"),
                created_at=pod.metadata.creation_timestamp.isoformat() if pod.metadata.creation_timestamp else None
            ))
        
        return result
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_resource_request(pod, resource_type: str) -> str:
    """获取 Pod 资源请求"""
    total = 0
    for container in pod.spec.containers:
        if container.resources and container.resources.requests:
            value = container.resources.requests.get(resource_type, "0")
            if resource_type == "cpu":
                total += parse_cpu(value)
            elif resource_type == "memory":
                total += parse_memory(value)
    
    if resource_type == "cpu":
        return f"{total}m"
    else:
        return f"{total}Mi"

def parse_cpu(cpu_str: str) -> int:
    """解析 CPU 字符串为毫核"""
    if cpu_str.endswith("m"):
        return int(cpu_str[:-1])
    return int(float(cpu_str) * 1000)

def parse_memory(mem_str: str) -> int:
    """解析内存字符串为 Mi"""
    if mem_str.endswith("Gi"):
        return int(float(mem_str[:-2]) * 1024)
    elif mem_str.endswith("Mi"):
        return int(mem_str[:-2])
    elif mem_str.endswith("Ki"):
        return int(float(mem_str[:-2]) / 1024)
    return int(mem_str) // (1024 * 1024)

# ============== Deployment Management ==============

@app.get("/api/v1/namespaces/{namespace}/deployments", response_model=List[DeploymentInfo])
async def list_deployments(namespace: str):
    """获取命名空间下的所有 Deployment"""
    try:
        deployments = apps_v1.list_namespaced_deployment(namespace)
        result = []
        
        for deploy in deployments.items:
            result.append(DeploymentInfo(
                name=deploy.metadata.name,
                namespace=namespace,
                replicas=deploy.spec.replicas or 0,
                ready_replicas=deploy.status.ready_replicas or 0,
                image=deploy.spec.template.spec.containers[0].image if deploy.spec.template.spec.containers else "N/A",
                created_at=deploy.metadata.creation_timestamp.isoformat() if deploy.metadata.creation_timestamp else None
            ))
        
        return result
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/namespaces/{namespace}/deployments/{name}/scale")
async def scale_deployment(namespace: str, name: str, replicas: int):
    """扩缩容 Deployment"""
    try:
        body = {"spec": {"replicas": replicas}}
        apps_v1.patch_namespaced_deployment_scale(
            name=name,
            namespace=namespace,
            body=body
        )
        return {"message": f"Scaled {name} to {replicas} replicas"}
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== HPA Management ==============

@app.get("/api/v1/namespaces/{namespace}/hpas", response_model=List[HPAConfig])
async def list_hpas(namespace: str):
    """获取命名空间下的所有 HPA"""
    try:
        hpas = autoscaling_v2.list_namespaced_horizontal_pod_autoscaler(namespace)
        result = []
        
        for hpa in hpas.items:
            cpu_target = None
            mem_target = None
            
            if hpa.spec.metrics:
                for metric in hpa.spec.metrics:
                    if metric.type == "Resource" and metric.resource.name == "cpu":
                        cpu_target = metric.resource.target.average_utilization
                    elif metric.type == "Resource" and metric.resource.name == "memory":
                        mem_target = metric.resource.target.average_utilization
            
            result.append(HPAConfig(
                name=hpa.metadata.name,
                namespace=namespace,
                min_replicas=hpa.spec.min_replicas or 1,
                max_replicas=hpa.spec.max_replicas,
                current_replicas=hpa.status.current_replicas or 0,
                target_cpu_utilization=cpu_target,
                target_memory_utilization=mem_target
            ))
        
        return result
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/hpas", response_model=HPAConfig)
async def create_hpa(hpa_request: HPACreateRequest):
    """创建 HPA"""
    try:
        hpa_body = autoscaling_v2.V2HorizontalPodAutoscaler(
            metadata=client.V1ObjectMeta(
                name=hpa_request.name,
                namespace=hpa_request.namespace
            ),
            spec=autoscaling_v2.V2HorizontalPodAutoscalerSpec(
                scale_target_ref=autoscaling_v2.V2CrossVersionObjectReference(
                    api_version="apps/v1",
                    kind="Deployment",
                    name=hpa_request.target_deployment
                ),
                min_replicas=hpa_request.min_replicas,
                max_replicas=hpa_request.max_replicas,
                metrics=[
                    autoscaling_v2.V2MetricSpec(
                        type="Resource",
                        resource=autoscaling_v2.V2ResourceMetricSource(
                            name="cpu",
                            target=autoscaling_v2.V2MetricTarget(
                                type="Utilization",
                                average_utilization=hpa_request.target_cpu_utilization
                            )
                        )
                    )
                ]
            )
        )
        
        result = autoscaling_v2.create_namespaced_horizontal_pod_autoscaler(
            namespace=hpa_request.namespace,
            body=hpa_body
        )
        
        return HPAConfig(
            name=result.metadata.name,
            namespace=result.metadata.namespace,
            min_replicas=result.spec.min_replicas or 1,
            max_replicas=result.spec.max_replicas,
            current_replicas=result.status.current_replicas or 0,
            target_cpu_utilization=hpa_request.target_cpu_utilization
        )
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== Log Management ==============

@app.post("/api/v1/logs")
async def get_logs(query: LogQuery):
    """获取 Pod 日志"""
    try:
        if query.pod_name:
            logs = v1.read_namespaced_pod_log(
                name=query.pod_name,
                namespace=query.namespace,
                container=query.container,
                tail_lines=query.lines
            )
            return {"logs": logs, "pod": query.pod_name}
        else:
            # 获取命名空间下所有 Pod 的日志
            pods = v1.list_namespaced_pod(query.namespace)
            all_logs = []
            
            for pod in pods.items[:5]:  # 限制返回前 5 个 Pod
                try:
                    logs = v1.read_namespaced_pod_log(
                        name=pod.metadata.name,
                        namespace=query.namespace,
                        tail_lines=query.lines
                    )
                    all_logs.append({
                        "pod": pod.metadata.name,
                        "logs": logs[:2000]  # 限制日志长度
                    })
                except:
                    continue
            
            return {"logs": all_logs}
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== Cost Analysis ==============

@app.get("/api/v1/cost/namespace/{namespace}")
async def estimate_namespace_cost(namespace: str):
    """估算命名空间资源成本"""
    try:
        pods = v1.list_namespaced_pod(namespace)
        
        total_cpu = 0
        total_memory = 0
        
        for pod in pods.items:
            for container in pod.spec.containers:
                if container.resources and container.resources.requests:
                    if "cpu" in container.resources.requests:
                        total_cpu += parse_cpu(container.resources.requests["cpu"])
                    if "memory" in container.resources.requests:
                        total_memory += parse_memory(container.resources.requests["memory"])
        
        # 简单成本估算 (按阿里云价格)
        cpu_cost_per_milli = 0.0001  # 每毫核每小时 0.0001 元
        memory_cost_per_mi = 0.00002  # 每 Mi 每小时 0.00002 元
        
        hourly_cpu_cost = total_cpu * cpu_cost_per_milli
        hourly_memory_cost = total_memory * memory_cost_per_mi
        
        return CostEstimate(
            namespace=namespace,
            cpu_cost=round(hourly_cpu_cost, 2),
            memory_cost=round(hourly_memory_cost, 2),
            total_cost=round(hourly_cpu_cost + hourly_memory_cost, 2),
            currency="CNY"
        )
    except ApiException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/cost/cluster")
async def estimate_cluster_cost():
    """估算整个集群成本"""
    try:
        namespaces = v1.list_namespace()
        total_cost = 0
        
        for ns in namespaces.items:
            if ns.metadata.name in ["kube-system", "kube-public"]:
                continue
            
            cost = await estimate_namespace_cost(ns.metadata.name)
            total_cost += cost.total_cost
        
        return {
            "total_hourly_cost": round(total_cost, 2),
            "daily_cost": round(total_cost * 24, 2),
            "monthly_cost": round(total_cost * 24 * 30, 2),
            "currency": "CNY"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============== Alert Management ==============

alert_rules = []

@app.post("/api/v1/alerts")
async def create_alert(rule: AlertRule):
    """创建告警规则"""
    rule_dict = rule.dict()
    rule_dict["id"] = len(alert_rules) + 1
    rule_dict["created_at"] = datetime.now().isoformat()
    alert_rules.append(rule_dict)
    return rule_dict

@app.get("/api/v1/alerts")
async def list_alerts():
    """获取所有告警规则"""
    return alert_rules

@app.delete("/api/v1/alerts/{alert_id}")
async def delete_alert(alert_id: int):
    """删除告警规则"""
    global alert_rules
    alert_rules = [r for r in alert_rules if r["id"] != alert_id]
    return {"message": f"Alert {alert_id} deleted"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
