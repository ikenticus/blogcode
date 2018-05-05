// http-hydra tries to download data concurrently
package main

import (
	"os"

	"github.com/ikenticus/blogcode/go/snippets/http-hydra/helpers"
)

func main() {
	config := helpers.Yaml(os.Args[1])
	helpers.Build(config)
}
