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
	output, err := xml.MarshalIndent(data, "", "    ")
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

// getResults will retrieve competition.ids
func getResults(root xmlNode) (results []int) {
	fmt.Println("Processing results")
	node := getXMLNode(root, "team-sport-content.league-content.season-content")
	for _, n := range node.Children {
		if n.XMLName.Local == "competition" {
			for _, c := range n.Children {
				if c.XMLName.Local == "id" {
					game := strings.Split(c.Text, ":")
					id, err := strconv.Atoi(game[len(game)-1])
					if err == nil {
						results = append(results, id)
					}
				}
			}
		}
	}
	return results
}

// getTeams will retrieve team.ids
func getTeams(root xmlNode) (teams []int) {
	fmt.Println("Processing teams")
	node := getXMLNode(root, "team-sport-content.league-content.season-content.conference-content.division-content.team-content")
	fmt.Println(node.XMLName.Local)
	return teams
}

func parseXML(pathType string, xmlFile string) (values []int) {
	root := readXML(xmlFile)

	// leaving below to demonstrate dynamic function call
	// if different parameters, then use a switch(p.Type)
	// however, since no idea how to return values, nixed
	//funcMap[strings.ToLower(pathType)].(func(xmlNode))(root)

	switch pathType {
	case "Results":
		values = getResults(root)
	case "Teams":
		values = getTeams(root)
	}
	return values
}
