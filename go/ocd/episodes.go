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
	comma := []string{"\"", "<"}
	for _, char := range comma {
		clean = strings.Split(clean, char)[0]
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

func parseWiki(show string, uri string, textOut bool, debug bool, rules *Rule) {
	var episodes = map[int]string{}
	var schedule = map[int]string{}
	fmt.Println("Parsing", uri)
	//fmt.Println("Rules", rules)

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

	s := regexp.MustCompile(rules.Season)
	n := regexp.MustCompile(rules.Number)
	e := regexp.MustCompile(rules.Episode)
	t := regexp.MustCompile(rules.Title)
	v := regexp.MustCompile(rules.Versus)
	h := regexp.MustCompile(rules.Hyper)
	d := regexp.MustCompile(rules.Datum)
	a := regexp.MustCompile(rules.Alpha)

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
			if debug {
				fmt.Printf("LINE : %s\n", line)
			}
			if strings.Contains(line, "class=\"mw-headline\"") {
				season = 0 // zero Season during Movie headers
			}
			if s.MatchString(line) {
				season, _ = strconv.Atoi(s.ReplaceAllString(line, "$2"))
				if debug {
					fmt.Println("SEASON:", season)
				}
			}
			if n.MatchString(line) {
				episode, _ = strconv.Atoi(n.ReplaceAllString(line, "$1"))
				if debug {
					fmt.Println("NUMBER:", episode)
				}
				eis = true // episode-in-season
			}
			if eis && e.MatchString(line) {
				episode, _ = strconv.Atoi(e.ReplaceAllString(line, "$1"))
				if debug {
					fmt.Println("EPISODE:", episode)
				}
				eis = false
			}

			if t.MatchString(line) || v.MatchString(line) {
				if v.MatchString(line) {
					title = v.ReplaceAllString(line, "$1 vs $2")
					if debug {
						fmt.Println("VERSUS:", title)
					}
				} else if t.MatchString(line) {
					title = t.ReplaceAllString(line, "$1")
					if debug {
						fmt.Println("TITLE:", title)
					}
					if h.MatchString(title) {
						title = h.ReplaceAllString(title, "$1")
						if debug {
							fmt.Println("HYPER:", title)
						}
					}
				}
				if len(title) > 0 && episode > 0 {
					key := 100*season + episode
					if key < 100 {
						key += 100
					}
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
				if debug {
					fmt.Println("AIRING:", timestamp)
					//fmt.Printf("%s %s: %s on %s\n", season, episode, title, timestamp)
				}
				if len(title) > 0 && episode > 0 {
					key := 100*season + episode
					if key < 100 {
						key += 100
					}
					raw, _ := time.Parse("January 2, 2006", timestamp)
					if raw.Year() == time.Now().Year() {
						schedule[key] = fmt.Sprintf("%02d/%02d", raw.Month(), raw.Day())
					} else {
						schedule[key] = fmt.Sprintf("%04d/%02d/%02d", raw.Year(), raw.Month(), raw.Day())
					}
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

type Rule struct {
	Season string
	Number string
	Episode string
	Title string
	Versus string
	Hyper string
	Datum string
	Alpha string
}

type Show struct {
	Name string
	Wiki string
}

type Settings struct {
	Rules Rule
	Shows []Show
}

func parseYaml(config string, debug bool) {
	fmt.Println("Parsing", config)
	data, err := ioutil.ReadFile(config + ".yaml")
	if err != nil {
		panic(err)
	}

	var settings Settings
	err = yaml.Unmarshal(data, &settings)
	if err != nil {
		panic(err)
	}

	showLength := len(settings.Shows)
	var wg sync.WaitGroup
	wg.Add(showLength)
	fmt.Printf("Found %d shows\n", showLength)

	/*
		    for _, show := range settings.Shows {
				fmt.Println("Processing", show.Name, show.Wiki)
			}
	*/
	for i := 0; i < showLength; i++ {
		go func(i int) {
			defer wg.Done()
			show := settings.Shows[i]
			//fmt.Println("Processing", show.Name, show.Wiki)
			parseWiki(show.Name, show.Wiki, true, debug, &settings.Rules)
		}(i)
	}
	wg.Wait()
	fmt.Printf("Processed %d shows\n", showLength)
}

func main() {
	optDbug := getopt.BoolLong("dbug", 'd', "Debug")
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
			parseYaml(*optName, *optDbug)
		} else if len(*optWiki) < 1 {
			processWiki(*optName)
		} else {
			rules := &Rule {
				Season: "^.*class=\"mw-headline\" id=\"(Season|Series)_([0-9]+).*$",
				Number: "^.*th scope=\"row\"(?: rowspan=\"[0-9]+\")? id=\"ep([0-9]+)\".*$",
				Episode: "^.*<td style=\"text-align:center\">([0-9]+)</td>.*(?:class=\"summary\").*$",
				Title: "^.*>[0-9]+</td><td class=\"summary\" style=\"text-align:left\">\"(.+).*</td.*$",
				Versus: "^.*td class=\"summary\" style=\"text-align:left\">.*title=\"(.+)\".+vs.+title=\"(.+)\".+</td.*$",
				Hyper: "<a href=\".+\">(.+)</a>\"",
				Datum: "^.*<td style=\"text-align:center\">([A-Za-z]+)&#160;([0-9]+),&#160;([0-9]+)<span.+bday dtstart.+$",
				Alpha: "^.*<td style=\"text-align:center\">([0-9]+)&#160;([A-Za-z]+)&#160;([0-9]+)<span.+bday dtstart.+$",
			}
			parseWiki(*optName, *optWiki, *optTime, *optDbug, rules)
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
