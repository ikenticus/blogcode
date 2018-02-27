package main

import (
	"fmt"
	"os"

	"github.com/franela/goreq"
	"golang.org/x/net/html"
	"golang.org/x/net/html/atom"
)

func main() {
	var url string
	if len(os.Args) > 1 {
		url = os.Args[1]
	} else {
		url = "http://www.espn.com/college-football/rankings"
	}
	resp, _ := goreq.Request{Uri: url}.Do()
	doc := html.NewTokenizer(resp.Body)

	start := false
	for tokenType := doc.Next(); tokenType != html.ErrorToken; {
		token := doc.Token()
		//fmt.Printf("Token: (%q)\n", token)

		if tokenType == html.StartTagToken {
			//fmt.Println("Atom:", token.DataAtom)
			if token.DataAtom == atom.Tr {
				for _, a := range token.Attr {
					if a.Key == "class" && a.Val == "stathead" {
						if start {
							start = false
						} else {
							start = true
						}
						fmt.Println("Node:", token.Data, start)
						break
					}
				}
			}

			// see https://godoc.org/golang.org/x/net/html/atom
			if token.DataAtom != atom.A {
				tokenType = doc.Next()
				continue
			}

			for _, attr := range token.Attr {
				if attr.Key == "href" {
					fmt.Printf("Link: %q => %q\n", token.Data, attr.Val)
				}
			}
		}
		tokenType = doc.Next()
	}
	resp.Body.Close()
}
