package main

import (
	"encoding/xml"
	"fmt"
	"os"
	"time"

	"github.com/franela/goreq"
	"github.com/pborman/getopt"
)

var (
	polls = map[string]string{
		"ncaaf": "http://www.espn.com/college-football/rankings/_/week/%d/year/%d/seasontype/2",
		"ncaab": "http://www.espn.com/mens-college-basketball/rankings/_/year/%d/week/%d/seasontype/2",
		"ncaaw": "http://www.espn.com/womens-college-basketball/rankings/_/year/%d/week/%d/seasontype/2",
	}
)

// cat ~/repos/sql-sports/SDIPolls/polls/AP_ncaaf_2017-12-03.json | gojson --name=TeamPolls
type TeamPolls struct {
	Feed struct {
		League_content struct {
			League struct {
				ID   string `json:"id"`
				Name []struct {
					_    string `json:"_"`
					Type string `json:"type"`
				} `json:"name"`
			} `json:"league"`
			Season_content struct {
				Poll_content struct {
					Poll struct {
						Date string `json:"date"`
						Name string `json:"name"`
					} `json:"poll"`
					Team_poll_ranking []struct {
						First_place_votes int64  `json:"first-place-votes"`
						Points            string `json:"points"`
						Previous_rank     string `json:"previous-rank"`
						Rank              string `json:"rank"`
						Team              struct {
							ID   string `json:"id"`
							Name string `json:"name"`
						} `json:"team"`
					} `json:"team-poll-ranking"`
				} `json:"poll-content"`
				Season struct {
					Name string `json:"name"`
				} `json:"season"`
			} `json:"season-content"`
		} `json:"league-content"`
		Sport struct {
			ID   string `json:"id"`
			Name string `json:"name"`
		} `json:"sport"`
	} `json:"feed"`
	LastModified struct {
		Pull string `json:"pull"`
	} `json:"lastModified"`
	Season      string `json:"season"`
	Sport       string `json:"sport"`
	Subcategory string `json:"subcategory"`
	Subsport    string `json:"subsport"`
	Subtype     string `json:"subtype"`
	SubtypeID   string `json:"subtypeId"`
	Type        string `json:"type"`
	TypeID      string `json:"typeId"`
}

type node struct {
	XMLName  xml.Name
	Text     string     `xml:",chardata"`
	Attrs    []xml.Attr `xml:",any,attr"` // since go1.8
	Children []node     `xml:",any"`
}

func get(url string, name string) {
	res, err := goreq.Request{Uri: url}.Do()
	if err != nil || res.StatusCode != 200 {
		fmt.Printf("%v", err)
		os.Exit(1)
	}
	html, _ := res.Body.ToString()
	/*
		err = ioutil.WriteFile(name, []byte(html), 0644)
		if err != nil {
			panic(err)
		}
	*/
	data := node{}
	xml.Unmarshal([]byte(html), &data)
	fmt.Println(data)
	output, _ := xml.MarshalIndent(data, "", "    ")
	fmt.Println(string(output))
}

func page(id string, text string, year int, week int) string {
	url := fmt.Sprintf(text, year, 1)
	if id == "ncaaf" {
		year--
		url = fmt.Sprintf(text, 1, year)
	}
	return url
}

func main() {
	thisYear := time.Now().Year()
	optHelp := getopt.BoolLong("help", 'h', "Help")
	optYear := getopt.IntLong("year", 'y', thisYear, "Season")
	getopt.Parse()

	if *optHelp {
		getopt.Usage()
		os.Exit(0)
	}

	for i, p := range polls {
		url := page(i, p, *optYear, 1)
		fmt.Println(i, p, url)
		get(url, i)
	}
	//defer printList(*optUrl, *optOut)
}
