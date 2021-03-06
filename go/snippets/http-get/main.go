package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "strings"
)

const Services = "google,youtube"

func get(name string) {
    resp, err := http.Get(fmt.Sprintf("https://www.%s.com", name))
    fmt.Printf("-----\n%s\nError: %v\n", name, err)
    fmt.Println(resp)
    fmt.Println(resp.Body)
    //io.Copy(os.Stdout, resp.Body)

    //var data status.Data
    //json.Unmarshal(body, &data)
}

func main() {
    services := strings.Split(Services, ",")
    for _, name := range services {
        get(name)
    }
}
