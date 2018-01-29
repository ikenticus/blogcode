package main

import (
    "encoding/json"
    "encoding/xml"
    "fmt"
    "io/ioutil"
    "os"
    "strings"
)

type node struct {
    Attr     []xml.Attr
    XMLName  xml.Name
    Children []node `xml:",any"`
    Text     string `xml:",chardata"`
}

func main() {
    source := os.Args[1]
    fmt.Println("source", source)
    input, _ := ioutil.ReadFile(source)

    var output []byte
    var data interface{}

    if strings.HasSuffix(source, ".json") {
        json.Unmarshal(input, &data)
        output, _ = json.MarshalIndent(data, "", "    ")
    } else if strings.HasSuffix(source, ".xml") {
        data := node{}
        xml.Unmarshal([]byte(input), &data)
        output, _ = xml.MarshalIndent(data, "", "    ")
    }

    if len(output) > 0 {
        os.Stdout.Write([]byte(output))
    }
}
