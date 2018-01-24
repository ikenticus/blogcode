package main

import (
    /*
    "crypto/hmac"
    "crypto/sha256"
    "encoding/base64"
    "net/http"
    "time"
    */
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"
    "regexp"
    "strconv"
    "strings"

    "github.com/pborman/getopt"
)

var (
    episodes = map[int]string{}
)

const (
    scalrPath = "https://scalr.gannettdigital.com"
    vaultPath = "secret/paas-api/paas-api-ci/production"
)

func cleanWiki (show string) {
    fmt.Println("Processing", show)
    data, err := ioutil.ReadFile(show + ".wiki")
    if err != nil {
        panic(err)
    }

    sep := "\n"
    if strings.HasPrefix(string(data), "\r\n") {
        sep = "\r\n"
    } else if strings.HasPrefix(string(data), "\r") {
        sep = "\r"
    }

    var season int = 0
    var lines []string
    lines = strings.Split(string(data), sep)
    for _, line := range lines {
        if strings.HasPrefix(line, "Season ") {
            //fmt.Printf("%d : %s\n", index, line)
            r := regexp.MustCompile("^Season ([0-9]+).*$")
            season, _ = strconv.Atoi(r.ReplaceAllString(line, "$1"))
            //fmt.Println("Season:", 100 * season)
        }

        //dirty := regexp.MustCompile("[")
        //dirty.ReplaceAllString(line, "")
        clean := line
        messy := []string {"? ", ": ", "... "}
        for _, ugly := range messy {
            clean = strings.Replace(clean, ugly, " - ", -1)
        }
        dirty := []string {"!", "?", "&", "[", "]", "'", "..."}
        for _, dirt := range dirty {
            clean = strings.Replace(clean, dirt, "", -1)
        }
        //fmt.Println("Clean:", clean)

        single := regexp.MustCompile("^[0-9]+[^0-9]+([0-9]+)[^0-9]+\"([^\"]+)\".*$")
        if single.MatchString(clean) {
            if season > 0 {
                ep := strings.Split(single.ReplaceAllString(clean, "$1|$2"), "|")
                num, err := strconv.Atoi(ep[0])
                if err == nil {
                    //fmt.Println("Episode:", 100 * season + num, ep[1], line)
                    episodes[100 * season + num] = ep[1]
                }
            }
        }
    }

    fmt.Println("Episodes:", episodes)
    output, _ := json.MarshalIndent(episodes, "", "    ")
    ioutil.WriteFile(show + ".json", output, 0644)
}

func main() {
    optHelp := getopt.BoolLong("help", 0, "Help")
    optName := getopt.StringLong("name", 'n', "", "TV Show name")
    optWiki := getopt.StringLong("wiki", 'w', "", "Wiki Page Name")
    optFile := getopt.BoolLong("file", 0, "Process Files in Dir")
    optList := getopt.BoolLong("list", 0, "Process File List")
    getopt.Parse()

    if *optHelp || len(os.Args) < 2 {
        getopt.Usage()
        os.Exit(0)
    }

    fmt.Printf("Name: %v, Wiki: %v, File: %v, List: %v\n", *optName, *optWiki, *optFile, *optList)
    if len(*optName) > 0 {
        if len(*optWiki) < 1 {
            cleanWiki(*optName)
        }
    }
}
