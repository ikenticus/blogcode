package helpers

import (
	"reflect"
	"testing"
)

const testDir = "test_data/"

func TestCleanXML(t *testing.T) {
	tests := []struct {
		description string
		input       string
		output      string
	}{
		{
			description: "successful clean",
			input:       "<html><body><table></table></body></html>",
			output:      "<html>\n\t<body>\n\t\t<table></table>\n\t</body>\n</html>",
		},
		{
			description: "unmarshal failure",
			input:       "<html><body><table</body></html>",
			output:      "<html></html>",
		},
	}

	for _, test := range tests {
		if got, want := cleanXML(test.input), test.output; got != want {
			t.Errorf("Test %q - got %v, want %v", test.description, got, want)
		}
	}
}

/*
func TestGetXMLNode(t *testing.T) {
	(x xmlNode, key string) xmlNode {
	for _, s := range strings.Split(key, ".") {
		for _, n := range x.Children {
			if n.XMLName.Local == s {
				x = n
			}
		}
	}
	return x
}
*/
func TestParseXML(t *testing.T) {
	tests := []struct {
		description string
		xmlFile     string
		pathType    string
		findKey     string
		wantValues  []int
	}{
		{
			description: "successful results",
			xmlFile:     testDir + "results.xml",
			pathType:    "Results",
			findKey:     "competition",
			wantValues:  []int{123456, 135791},
		},
		{
			description: "successful teams",
			xmlFile:     testDir + "teams.xml",
			pathType:    "Teams",
			findKey:     "team",
			wantValues:  []int{1234, 5678, 9999},
		},
		{
			description: "successful tourneys",
			xmlFile:     testDir + "tourneys.xml",
			pathType:    "Results",
			findKey:     "competition",
			wantValues:  []int{1234, 5678},
		},
	}

	for _, test := range tests {
		gotValues := parseXML(test.xmlFile, test.pathType, test.findKey)
		if got, want := gotValues, test.wantValues; !reflect.DeepEqual(got, want) {
			t.Errorf("Test %q - got %v, want %v", test.description, got, want)
		}
	}
}
