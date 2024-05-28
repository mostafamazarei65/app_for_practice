package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

const DefaultNodeName = "default_node"

func getNodeName(context *gin.Context) {
	nodeName := os.Getenv("NODE_NAME")
	if nodeName == "" {
		hostname, err := os.Hostname()
		if err != nil {
			context.JSON(http.StatusInternalServerError, gin.H{"error": "failed to retrieve hostname"})
			return
		}
		nodeName = hostname
	}
	context.IndentedJSON(http.StatusOK, gin.H{"nodeName": nodeName})
}

func HealthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "UP"})
}

func main() {
	router := gin.Default()
	router.GET("/", getNodeName)
	router.GET("/health", HealthCheck)
	address := ":8080"
	router.Run(address)
}
