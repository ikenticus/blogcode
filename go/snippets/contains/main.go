package main

import (
    "fmt"
)

func containsString(source []string, item string) bool {
	for _, s := range source {
        if s == item {
			return true
		}
	}
	return false
}

func main() {
    ABCs := []string{"A", "B", "C"}
    fmt.Println("ABCs contain A:", containsString(ABCs, "A"))
    fmt.Println("ABCs contain C:", containsString(ABCs, "C"))
    fmt.Println("ABCs contain X:", containsString(ABCs, "X"))
    fmt.Println("ABCs contain Z:", containsString(ABCs, "Z"))
}
