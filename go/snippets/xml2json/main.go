
package main

import (
    "encoding/json"
	"fmt"
	"io/ioutil"
    "os"
    "strings"

	xj "github.com/basgys/goxml2json"
)

func main() {
	source := os.Args[1]
	input, err := ioutil.ReadFile(source)
	if err != nil {
		fmt.Errorf("failed to read json file %q: %v", source, err)
		os.Exit(10)
	}

	data := strings.NewReader(string(input))
	output, err := xj.Convert(data)
	if err != nil {
		fmt.Errorf("failed to convert %s to json: %v", source, err)
		os.Exit(20)
	}
	//fmt.Println(output.String())

    var clean interface{}
    json.Unmarshal(output.Bytes(), &clean)
    pretty, _ := json.MarshalIndent(clean, "", "    ")
    fmt.Println(string(pretty))
}
