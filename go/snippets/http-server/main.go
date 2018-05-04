// http-server is just a basic HTTP server that accepts lists GET/POST and sort them
package main

import (
	"fmt"
	"os"

	"github.com/ikenticus/blogcode/go/snippets/http-server/http"
)

func main() {
	if err := http.Server(); err != nil {
		fmt.Errorf("Error starting application: %v", err)
		os.Exit(1)
	}
}
