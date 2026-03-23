package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var (
	db     *gorm.DB
	jwtKey = []byte(os.Getenv("JWT_SECRET"))
)

type User struct {
	ID        uint   `gorm:"primaryKey" json:"id"`
	Username  string `gorm:"uniqueIndex;size:50" json:"username"`
	Email     string `gorm:"uniqueIndex;size:100" json:"email"`
	Password  string `gorm:"size:255" json:"-"`
	CreatedAt time.Time `json:"created_at"`
}

type LoginRequest struct {
	Username string `json:"username" binding:"required"`
	Password string `json:"password" binding:"required"`
}

type RegisterRequest struct {
	Username string `json:"username" binding:"required"`
	Email    string `json:"email" binding:"required,email"`
	Password string `json:"password" binding:"required,min=6"`
}

type Claims struct {
	UserID   uint   `json:"user_id"`
	Username string `json:"username"`
	jwt.RegisteredClaims
}

func main() {
	initDB()
	
	r := gin.Default()
	
	// Health check
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "healthy",
			"service": "user-service",
			"timestamp": time.Now().Format(time.RFC3339),
		})
	})
	
	// Routes
	v1 := r.Group("/api/v1")
	{
		v1.POST("/register", register)
		v1.POST("/login", login)
		v1.GET("/users/:id", getUser)
		v1.PUT("/users/:id", updateUser)
	}
	
	port := os.Getenv("PORT")
	if port == "" {
		port = "8001"
	}
	
	log.Printf("User service starting on port %s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

func initDB() {
	dsn := os.Getenv("MYSQL_DSN")
	if dsn == "" {
		dsn = "root:password@tcp(mysql:3306)/blog?charset=utf8mb4&parseTime=True&loc=Local"
	}
	
	var err error
	for i := 0; i < 30; i++ {
		db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
		if err == nil {
			break
		}
		log.Printf("Waiting for database... attempt %d", i+1)
		time.Sleep(2 * time.Second)
	}
	
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}
	
	db.AutoMigrate(&User{})
	log.Println("Database migration completed")
}

func register(c *gin.Context) {
	var req RegisterRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to hash password"})
		return
	}
	
	user := User{
		Username: req.Username,
		Email:    req.Email,
		Password: string(hashedPassword),
	}
	
	if err := db.Create(&user).Error; err != nil {
		c.JSON(http.StatusConflict, gin.H{"error": "Username or email already exists"})
		return
	}
	
	c.JSON(http.StatusCreated, gin.H{
		"message": "User registered successfully",
		"user_id": user.ID,
	})
}

func login(c *gin.Context) {
	var req LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	var user User
	if err := db.Where("username = ?", req.Username).First(&user).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid credentials"})
		return
	}
	
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(req.Password)); err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid credentials"})
		return
	}
	
	token := generateToken(user)
	c.JSON(http.StatusOK, gin.H{
		"token": token,
		"user": gin.H{
			"id":       user.ID,
			"username": user.Username,
			"email":    user.Email,
		},
	})
}

func generateToken(user User) string {
	claims := Claims{
		UserID:   user.ID,
		Username: user.Username,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
		},
	}
	
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, _ := token.SignedString(jwtKey)
	return tokenString
}

func getUser(c *gin.Context) {
	id := c.Param("id")
	var user User
	if err := db.First(&user, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"id":        user.ID,
		"username":  user.Username,
		"email":     user.Email,
		"created_at": user.CreatedAt,
	})
}

func updateUser(c *gin.Context) {
	id := c.Param("id")
	var user User
	if err := db.First(&user, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
		return
	}
	
	var updates map[string]interface{}
	if err := c.ShouldBindJSON(&updates); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	db.Model(&user).Updates(updates)
	c.JSON(http.StatusOK, gin.H{"message": "User updated successfully"})
}

// Metrics endpoint for Prometheus
func metricsHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, `
# HELP user_service_requests_total Total number of requests
# TYPE user_service_requests_total counter
user_service_requests_total 0
# HELP user_service_uptime Service uptime in seconds
# TYPE user_service_uptime gauge
user_service_uptime 0
`)
}
