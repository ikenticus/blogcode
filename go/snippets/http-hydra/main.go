// http-hydra tries to download data concurrently
package main

import (
	"fmt"
	"os"

	"github.com/ikenticus/blogcode/go/snippets/http-hydra/helpers"
)

func main() {
	config := helpers.Yaml(os.Args[1])
	fmt.Println(config.BaseURL, config.APIKey)
}
