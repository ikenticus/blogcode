package main

import (
	"os"
	"strings"

	"github.com/ikenticus/blogcode/go/app/loader"
)

func main() {
	loader.Run(strings.Join(os.Args[1:], " "))
}
