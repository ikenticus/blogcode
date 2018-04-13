package main

import (
	/*
	   "bytes"
	   "fmt"
	   "encoding/json"
	   "log"
	   "net/http"
	*/

	"os"
	"path"

	"github.com/ikenticus/blogcode/go/snippets/read-post/helpers"
)

func main() {
	config := helpers.Yaml(path.Base(os.Args[0]))
	helpers.Scan(config)
}
