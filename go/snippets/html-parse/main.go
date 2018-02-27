package main

import (
    "encoding/xml"
    "fmt"
    "io/ioutil"
    "os"
    "strings"
    "golang.org/x/net/html"
)

type node struct {
    XMLName  xml.Name
    Text     string     `xml:",chardata"`
    Attrs    []xml.Attr `xml:",any,attr"`   // since go1.8
    Children []node     `xml:",any"`
}

func main() {
    source := os.Args[1]
    //fmt.Println("source", source)
    input, _ := ioutil.ReadFile(source)

    doc, _ := html.Parse(strings.NewReader(string(input)))
    var f func(*html.Node)
    start := false
    f = func(n *html.Node) {
        //fmt.Println(n.Type, n.Attr, n.Data, n.DataAtom)
        switch n.Type {
        case html.ElementNode:
            if n.Data == "tr" {
                for _, a := range n.Attr {
                    if a.Key == "class" && a.Val == "stathead" {
                        if start {
                            start = false
                        } else {
                            start = true
                        }
                        fmt.Println("Node:", n.Data, start)
                        break
                    }
                }
            } else if n.Data == "a" {
                for _, a := range n.Attr {
                    if a.Key == "href" {
                        if n.FirstChild != nil {
                            fmt.Printf("Link: %q => %q\n", strings.TrimSpace(n.FirstChild.Data), a.Val)
                        }
                        break
                    }
                }
            }
        case html.TextNode:
            if start {
                fmt.Printf("Text: %q\n", n.Data) 
            }
        }
    	for c := n.FirstChild; c != nil; c = c.NextSibling {
	    	f(c)
	    }
    }
    f(doc)
}
