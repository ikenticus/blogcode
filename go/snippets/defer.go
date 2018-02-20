package main

import (
    "fmt"
    "sort"
)

func main() {
    words := []string {"3cruel","1hello","2there"}
    defer fmt.Println("world")

    sort.Strings(words)
    for _, word := range words {
        fmt.Println(word[1:])
    }
}
