// Read-Post scans specified paths and uploads data to APIs via POST
package main

import (
	"os"
	"path"

	"github.com/ikenticus/blogcode/go/snippets/read-post/helpers"
)

func main() {
	config := helpers.Yaml(path.Base(os.Args[0]))
	helpers.Scan(config)
}
