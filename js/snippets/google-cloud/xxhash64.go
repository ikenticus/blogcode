package main

import (
    "fmt"
    "io"
    "strings"

    x0 "github.com/cespare/xxhash"
    x1 "github.com/OneOfOne/xxhash"
)

const word = "teamstats_mlb_2017_2973"

func main() {
    fmt.Println(x0.Sum64String(word))

    h := x1.New64()
    r := strings.NewReader(word)
    io.Copy(h, r)
    fmt.Println(h.Sum64())
}
