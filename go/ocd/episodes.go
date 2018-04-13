package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/pborman/getopt"
	yaml "gopkg.in/yaml.v2"
)

const (
	crlf     = "\r\n"
	wikiPath = "https://en.wikipedia.org/wiki/"
)

func cleanWiki(clean string) string {
	messy := []string{"? ", ": ", "... "}
	for _, ugly := range messy {
		clean = strings.Replace(clean, ugly, " - ", -1)
	}
	dirty := []string{"!", "?", "&", "[", "]", "'", "..."}
	for _, dirt := range dirty {
		clean = strings.Replace(clean, dirt, "", -1)
	}

	//fmt.Println("Clean:", clean)
	if strings.Contains(clean, "\"") {
		return strings.Split(clean, "\"")[0]
	}
	return clean
}

func processWiki(show string) {
	var episodes = map[int]string{}

	fmt.Println("Processing", show)
	data, err := ioutil.ReadFile(show + ".wiki")
	if err != nil {
		panic(err)
	}

	sep := "\n"
	if strings.HasPrefix(string(data), crlf) {
		sep = crlf
	} else if strings.HasPrefix(string(data), "\r") {
		sep = "\r"
	}

	var season int = 0
	var lines []string
	lines = strings.Split(string(data), sep)
	for _, line := range lines {
		if strings.HasPrefix(line, "Season ") || strings.HasPrefix(line, "Series ") {
			//fmt.Printf("%d : %s\n", index, line)
			r := regexp.MustCompile("^(Season|Series) ([0-9]+).*$")
			season, _ = strconv.Atoi(r.ReplaceAllString(line, "$2"))
			//fmt.Println("Season:", 100 * season)
		}

		clean := cleanWiki(line)
		single := regexp.MustCompile("^[0-9]+[^0-9]+([0-9]+)[^0-9]+\"([^\"]+)\".*$")
		if single.MatchString(clean) {
			if season > 0 {
				ep := strings.Split(single.ReplaceAllString(clean, "$1|$2"), "|")
				num, err := strconv.Atoi(ep[0])
				if err == nil {
					//fmt.Println("Episode:", 100 * season + num, ep[1], line)
					episodes[100*season+num] = ep[1]
				}
			}
		}
	}
	//fmt.Println("Episodes:", episodes)
	output, _ := json.MarshalIndent(episodes, "", "    ")
	ioutil.WriteFile(show+".json", output, 0644)
}

func buildMove(show string) {
	var episodes = map[int]string{}

	fmt.Println("Building", show)
	data, err := ioutil.ReadFile(show + ".list")
	if err != nil {
		panic(err)
	}

	var moves []string
	var lines []string
	lines = strings.Split(string(data), crlf)
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
	output := fmt.Sprintf("%s%spause%s", strings.Join(moves, crlf), crlf, crlf)
	ioutil.WriteFile(show+".cmd", []byte(output), 0644)
}

func buildList(show string) {
	fmt.Println("Reading", show)

	//data, err := filepath.Glob("*")
	data, err := ioutil.ReadDir("./")
	if err != nil {
		panic(err)
	}

	var files []string
	for _, d := range data {
		if strings.HasPrefix(d.Name(), "Season ") {
			season, _ := ioutil.ReadDir(d.Name())
			for _, f := range season {
				files = append(files, fmt.Sprintf("\\%s\\%s", d.Name(), f.Name()))
			}
		}
	}
	//fmt.Println("Files:", strings.Join(files, crlf))
	output := fmt.Sprintf("%s%s", strings.Join(files, crlf), crlf)
	ioutil.WriteFile(show+".list", []byte(output), 0644)
}

func parseWiki(show string, uri string, textOut bool) {
	var episodes = map[int]string{}
	var schedule = map[int]string{}
	fmt.Println("Parsing", uri)

	client := &http.Client{}
	req, _ := http.NewRequest("GET", wikiPath+uri, nil)
	resp, _ := client.Do(req)
	defer resp.Body.Close()

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	//fmt.Println(os.Stdout, string(data))

	var title string = ""
	var season int = 1
	var episode int = 0
	var active bool = false
	var eis bool = false

	s := regexp.MustCompile("^.*class=\"mw-headline\" id=\"(Season|Series)_([0-9]+).*$")
	n := regexp.MustCompile("^.*th scope=\"row\" id=\"ep([0-9]+)\".*$")
	e := regexp.MustCompile("^.*<td>([0-9]+)</td>.*$")
	t := regexp.MustCompile("^.*td class=\"summary\" style=\"text-align:left\">\"(.+)\".*</td.*$")
	v := regexp.MustCompile("^.*td class=\"summary\" style=\"text-align:left\">.*title=\"(.+)\".+vs.+title=\"(.+)\".+</td.*$")
	h := regexp.MustCompile("<a href=\".+\">(.+)</a>")
	d := regexp.MustCompile("^.*<td>([A-Za-z]+)&#160;([0-9]+),&#160;([0-9]+)<span.+bday dtstart.+$")
	a := regexp.MustCompile("^.*<td>([0-9]+)&#160;([A-Za-z]+)&#160;([0-9]+)<span.+bday dtstart.+$")

	var lines []string
	lines = strings.Split(string(data), "\n")
	for _, line := range lines {
		if strings.Contains(line, "id=\"Episodes\"") {
			active = true
		} else if strings.Contains(line, "<h2>") {
			active = false
		}

		if active {
			//fmt.Printf("%d : %s\n", index, line)
			if strings.Contains(line, "class=\"mw-headline\"") {
				season = 0 // zero Season during Movie headers
			}
			if s.MatchString(line) {
				season, _ = strconv.Atoi(s.ReplaceAllString(line, "$2"))
			}
			if n.MatchString(line) {
				episode, _ = strconv.Atoi(n.ReplaceAllString(line, "$1"))
				eis = true // episode-in-season
			}
			if eis && e.MatchString(line) {
				episode, _ = strconv.Atoi(e.ReplaceAllString(line, "$1"))
				eis = false
			}

			if t.MatchString(line) || v.MatchString(line) {
				if t.MatchString(line) {
					title = t.ReplaceAllString(line, "$1")
					if h.MatchString(title) {
						title = h.ReplaceAllString(title, "$1")
					}
				} else if v.MatchString(line) {
					title = v.ReplaceAllString(line, "$1 vs $2")
				}
				if len(title) > 0 && episode > 0 {
					key := 100*season + episode
					//fmt.Printf("%d: %s\n", key, title)
					episodes[key] = cleanWiki(title)
					schedule[key] = "TBA"
				}
			}
			if a.MatchString(line) || d.MatchString(line) {
				var timestamp string
				if d.MatchString(line) {
					timestamp = d.ReplaceAllString(line, "$1 $2, $3")
				} else if a.MatchString(line) {
					timestamp = a.ReplaceAllString(line, "$2 $1, $3")
				}
				//fmt.Printf("%s %s: %s on %s\n", season, episode, title, timestamp)
				if len(title) > 0 && episode > 0 {
					key := 100*season + episode
					raw, _ := time.Parse("January 2, 2006", timestamp)
					schedule[key] = fmt.Sprintf("%04d/%02d/%02d", raw.Year(), raw.Month(), raw.Day())
				}
			}
		}
	}
	if textOut {
		var text []string
		keys := make([]int, 0)
		for k, _ := range episodes {
			keys = append(keys, k)
		}
		sort.Ints(keys)
		for _, k := range keys {
			text = append(text, fmt.Sprintf("%s\t%d - %s", schedule[k], k, episodes[k]))
		}
		var timeline string
		if len(text) > 0 {
			timeline = strings.Join(text, crlf)
		} else {
			timeline = string(data)
		}
		ioutil.WriteFile(show+".txt", []byte(timeline), 0644)
	} else {
		//fmt.Println("Episodes:", episodes)
		output, _ := json.MarshalIndent(episodes, "", "    ")
		ioutil.WriteFile(show+".json", output, 0644)
	}
}

func parseYaml(config string) {
	fmt.Println("Parsing", config)
	data, err := ioutil.ReadFile(config + ".yaml")
	if err != nil {
		panic(err)
	}

	type Show struct {
		Name string
		Wiki string
	}

	var shows []Show
	err = yaml.Unmarshal(data, &shows)
	if err != nil {
		panic(err)
	}

	showLength := len(shows)
	var wg sync.WaitGroup
	wg.Add(showLength)
	fmt.Printf("Found %d shows\n", showLength)

	/*
		    for _, show := range shows {
				fmt.Println("Processing", show.Name, show.Wiki)
			}
	*/
	for i := 0; i < showLength; i++ {
		go func(i int) {
			defer wg.Done()
			show := shows[i]
			//fmt.Println("Processing", show.Name, show.Wiki)
			parseWiki(show.Name, show.Wiki, true)
		}(i)
	}
	wg.Wait()
	fmt.Printf("Processed %d shows\n", showLength)
}

func main() {
	optHelp := getopt.BoolLong("help", 'h', "Help")
	optList := getopt.BoolLong("list", 'l', "Process File List")
	optRead := getopt.BoolLong("read", 'r', "Read Current Dir")
	optTime := getopt.BoolLong("time", 't', "Output Time Text")
	optName := getopt.StringLong("name", 'n', "", "TV Show name (required)")
	optWiki := getopt.StringLong("wiki", 'w', "", "Wiki Page Name")
	optYaml := getopt.BoolLong("yaml", 'y', "Load YAML Config (name)")
	getopt.Parse()

	if *optHelp || len(os.Args) < 2 {
		getopt.Usage()
		os.Exit(0)
	}

	//fmt.Printf("Name: %v, Wiki: %v, Read: %v, List: %v\n", *optName, *optWiki, *optRead, *optList)
	if len(*optName) > 0 {
		if *optYaml {
			parseYaml(*optName)
		} else if len(*optWiki) < 1 {
			processWiki(*optName)
		} else {
			parseWiki(*optName, *optWiki, *optTime)
		}
		if *optList {
			buildMove(*optName)
		} else if *optRead {
			buildList(*optName)
			buildMove(*optName)
		}
	} else {
		getopt.Usage()
	}
}
