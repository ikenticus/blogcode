package main

import (
	"encoding/json"
	"fmt"
	"strconv"
)

type Year struct {
	ID      string `json:"id"`
	Display string `json:"display"`
}

func main() {
	var year []Year
	for y := 2018; y >= 1988; y-- {
		year = append(year, Year{
			ID:      strconv.Itoa(y),
			Display: fmt.Sprintf("%d Season", y),
		})
	}
	output, err := json.MarshalIndent(year, "", "    ")
	if err != nil {
		fmt.Errorf("Error marshaling JSON", err)
	} else {
		fmt.Println(string(output))
	}
}
