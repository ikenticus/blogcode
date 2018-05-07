// http-hydra tries to download data concurrently
package main

import (
	"os"

	"github.com/ikenticus/blogcode/go/snippets/http-hydra/helpers"
)

func main() {
	for _, y := range os.Args[1:] {
		config := helpers.Yaml(y)
		helpers.Build(config)
	}
}
