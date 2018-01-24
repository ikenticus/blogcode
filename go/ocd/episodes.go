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
    wikiPath = "https://scalr.gannettdigital.com"
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
    //fmt.Println("Episodes:", episodes)
    output, _ := json.MarshalIndent(episodes, "", "    ")
    ioutil.WriteFile(show + ".json", output, 0644)
}

func buildMove (show string) {
    fmt.Println("Building", show)
    data, err := ioutil.ReadFile(show + ".list")
    if err != nil {
        panic(err)
    }

    var moves []string
    var lines []string
    lines = strings.Split(string(data), "\r\n")
    for _, line := range lines {
        pos := strings.LastIndex(line, "Season ")
        off := len(line) - pos
        if strings.Contains(line, "\\Season ") && off > 10 {
            //fmt.Printf("%v : %s\n", index, line[pos:])

            var num int = 0
            type2 := regexp.MustCompile("^.*[Ss]([0-9]+)[Ee]([0-9]+).*$")
            type3 := regexp.MustCompile("^.*([0-9]+)x([0-9]+).*$")
            if type2.MatchString(line) {
                num, _ = strconv.Atoi(type2.ReplaceAllString(line, "$1$2"))
            } else if type3.MatchString(line) {
                num, _ = strconv.Atoi(type3.ReplaceAllString(line, "$1$2"))
            }
            if num > 0 {
                season := strings.Split(line[pos:], "\\")[0]
                dots := strings.Split(line[pos:], ".")
                ext := dots[len(dots)-1]
                moves = append(moves, fmt.Sprintf("move \"%s\" \"%s\\%d - %s.%s\"", line[pos:], season, num, episodes[num], ext))
            }
        }
    }
    ioutil.WriteFile(show + ".cmd", []byte(strings.Join(moves, "\r\n") + "\r\npause\r\n"), 0644)
}

func main() {
    optHelp := getopt.BoolLong("help", 'h', "Help")
    optName := getopt.StringLong("name", 'n', "", "TV Show name")
    optWiki := getopt.StringLong("wiki", 'w', "", "Wiki Page Name")
    optFile := getopt.BoolLong("file", 'f', "Process Files in Dir")
    optList := getopt.BoolLong("list", 'l', "Process File List")
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
        if *optList {
            buildMove(*optName)
        }
    }
}
