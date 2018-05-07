package helpers

import (
	"reflect"
	"testing"
)

const testPath = "test_data/"

func TestSetDefaults(t *testing.T) {
	tests := []struct {
		description string
		xmlFile     string
		pathType    string
		findKey     string
		wantValues  []int
	}{
		{
			description: "successful results",
			xmlFile:     testPath + "results.xml",
			pathType:    "Results",
			findKey:     "competition",
			wantValues:  []int{123456, 135791},
		},
		{
			description: "successful teams",
			xmlFile:     testPath + "teams.xml",
			pathType:    "Teams",
			findKey:     "team",
			wantValues:  []int{1234, 5678, 9999},
		},
		{
			description: "successful tourneys",
			xmlFile:     testPath + "tourneys.xml",
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
