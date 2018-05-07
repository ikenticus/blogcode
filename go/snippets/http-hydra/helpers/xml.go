package helpers

import (
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

type xmlNode struct {
	XMLName  xml.Name
	Text     string     `xml:",chardata"`
	Attrs    []xml.Attr `xml:",any,attr"` // since go1.8
	Children []xmlNode  `xml:",any"`
}

// readXML will read and unmarshal XML file
func readXML(xmlFile string) xmlNode {
	node := xmlNode{}
	data, err := ioutil.ReadFile(xmlFile)
	if err == nil {
		xml.Unmarshal([]byte(data), &node)
	}
	return node
}

// cleanXML pretty-prints input
func cleanXML(input string) string {
	data := xmlNode{}
	xml.Unmarshal([]byte(input), &data)
	output, err := xml.MarshalIndent(data, "", "\t")
	if err != nil {
		fmt.Errorf("Error marshaling XML:", err)
		return ""
	}
	return string(output)
}

// getXMLNode will extract xmlNode via dot-notation
func getXMLNode(x xmlNode, key string) xmlNode {
	for _, s := range strings.Split(key, ".") {
		for _, n := range x.Children {
			if n.XMLName.Local == s {
				x = n
			}
		}
	}
	return x
}

// funcMap maps path types to functions
var funcMap = map[string]interface{}{
	"results": getResults,
	"teams":   getTeams,
}

// getContent will loop through node-content and retrieve key.ids
func getContent(node xmlNode, input []int, findKey string) (output []int) {
	copy(input, output)
	for _, c := range node.Children {
		if strings.HasSuffix(c.XMLName.Local, "-content") {
			input = getContent(c, output, findKey)
			output = append(output, input...)
		}
		if c.XMLName.Local == findKey {
			for _, t := range c.Children {
				if t.XMLName.Local == "id" {
					keyId := strings.Split(t.Text, ":")
					id, err := strconv.Atoi(keyId[len(keyId)-1])
					if err == nil {
						output = append(output, id)
					}
				}
			}
		}
	}
	return output
}

// getResults will retrieve competition.ids
func getResults(root xmlNode) (results []int) {
	results = getContent(root, results, "competition")
	if debug {
		fmt.Println("RESULTS", results)
	}
	return results
}

// getTeams will retrieve team.ids
func getTeams(root xmlNode) (teams []int) {
	teams = getContent(root, teams, "team")
	if debug {
		fmt.Println("TEAMS", teams)
	}
	return teams
}

func parseXML(xmlFile string, pathType string, findKey string) (values []int) {
	root := readXML(xmlFile)

	// leaving below to demonstrate dynamic function call
	// however, since no idea how to return values, nixed
	//funcMap[strings.ToLower(pathType)].(func(xmlNode))(root)

	// if different parameters, or returning value, then use a switch(pathType)
	/*
		switch pathType {
		case "Results":
			values = getResults(root)
		case "Teams":
			values = getTeams(root)
		}
	*/

	values = getContent(root, values, findKey)
	fmt.Printf("+Found %s: %v\n", findKey, values)
	return values
}
