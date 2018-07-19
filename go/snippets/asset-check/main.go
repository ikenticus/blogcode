// asset-check compares API to GraphQL assets
package main

import (
	"fmt"
	"os"
	"path"

	"github.com/ikenticus/blogcode/go/snippets/asset-check/helpers"
)

func main() {
	if len(os.Args) > 1 {
		config := helpers.Yaml(os.Args[1])
		err := helpers.Check(config)
		if err != nil {
			fmt.Printf("Asset Check failed: %s\n", err)
		}
	} else {
		fmt.Printf("Usage: %s <config>.yaml\n", path.Base(os.Args[0]))
	}
}
