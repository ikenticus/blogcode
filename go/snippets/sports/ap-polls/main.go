package main

import (
	"encoding/json"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/franela/goreq"
	"github.com/pborman/getopt"
	"golang.org/x/net/html"
)

const (
	pollType  = "2"
	pollName  = "Associated Press"
	pollTeams = "http://sports-service.production.%s/page/v2/%s/teams/%d/"
)

var (
	teams TeamsAPI
	polls = map[string]string{
		//"ncaaf": "http://www.espn.com/college-football/rankings/_/week/%d/year/%d/seasontype/2",
		//"ncaab": "http://www.espn.com/mens-college-basketball/rankings/_/poll/1/year/%d/week/%d",
		"ncaaw": "http://www.espn.com/womens-college-basketball/rankings/_/poll/1/year/%d/week/%d",
	}
)

// curl http://sports-service.production.domain.com/page/v2/ncaab/teams/2017/ | gojson --name TeamsAPI
type TeamsAPI struct {
	Environment  string     `json:"environment"`
	LastModified string     `json:"last_modified"`
	Page         []TeamPage `json:"page"`
}

type TeamPage struct {
	ConferenceKey  string `json:"conference_key"`
	ConferenceName string `json:"conference_name"`
	DivisionKey    string `json:"division_key"`
	DivisionName   string `json:"division_name"`
	TeamAbbr       string `json:"team_abbr"`
	TeamFirst      string `json:"team_first"`
	TeamKey        string `json:"team_key"`
	TeamLast       string `json:"team_last"`
	TeamRank       int64  `json:"team_rank"`
	TeamSlug       string `json:"team_slug"`
}

// cat ~/repos/sql-sports/SDIPolls/polls/AP_ncaaf_2017-12-03.json | gojson --name=TeamPolls
type TeamPolls struct {
	Season      string `json:"season"`
	Sport       string `json:"sport"`
	Subcategory string `json:"subcategory"`
	Subsport    string `json:"subsport"`
	Subtype     string `json:"subtype"`
	SubtypeID   string `json:"subtypeId"`
	Type        string `json:"type"`
	TypeID      string `json:"typeId"`
	Feed        struct {
		Sport         TeamPollSport `json:"sport"`
		LeagueContent struct {
			League struct {
				ID   string       `json:"id"`
				Name []LeagueName `json:"name"`
			} `json:"league"`
			SeasonContent struct {
				Season struct {
					Name string `json:"name"`
				} `json:"season"`
				PollContent struct {
					Poll struct {
						Date string `json:"date"`
						Name string `json:"name"`
					} `json:"poll"`
					Teams []TeamPollRanking `json:"team-poll-ranking"`
				} `json:"poll-content"`
			} `json:"season-content"`
		} `json:"league-content"`
	} `json:"feed"`
}

type LeagueName struct {
	Type string `json:"type"`
	Name string `json:"_"`
}

type TeamPollSport struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

// note the ,omitempty to avoid empty strings in the output
type TeamPollRanking struct {
	Rank     string `json:"rank,omitempty"`
	Previous string `json:"previous-rank,omitempty"`
	Points   string `json:"points"`
	FPVotes  string `json:"first-place-votes,omitempty"`
	Team     struct {
		ID   string `json:"id,omitempty"`
		Name string `json:"name"`
	} `json:"team"`
}

type node struct {
	XMLName  xml.Name
	Text     string     `xml:",chardata"`
	Attrs    []xml.Attr `xml:",any,attr"` // since go1.8
	Children []node     `xml:",any"`
}

func getTeams(name string, year int) TeamsAPI {
	var teams TeamsAPI
	work, _ := os.LookupEnv("DOMAIN")
	url := fmt.Sprintf(pollTeams, work, name, year-1)
	res, err := goreq.Request{Uri: url}.Do()
	if err != nil || res.StatusCode != 200 {
		fmt.Printf("%v", err)
		os.Exit(1)
	}
	res.Body.FromJsonTo(&teams)
	return teams
}

// ugly-ass-long func, will refactor it later
func getPoll(name string, text string, year int, week int) {
	url := page(name, text, year, week)
	//fmt.Println("Url:", url)
	res, err := goreq.Request{Uri: url}.Do()
	if err != nil || res.StatusCode != 200 {
		fmt.Printf("%v", err)
		os.Exit(1)
	}
	doc, _ := html.Parse(res.Body)
	//fmt.Println(doc)

	sport := "basketball"
	season := year - 1
	seasonSpan := fmt.Sprintf("%s-%s", strconv.Itoa(season-1), strconv.Itoa(season))
	if name == "ncaaf" {
		sport = "football"
	}

	teampoll := TeamPolls{
		Subcategory: "sdi",
		Season:      strconv.Itoa(season),
		Sport:       sport,
		Subsport:    strings.ToUpper(name),
		Type:        "team-polls",
		TypeID:      strconv.Itoa(season),
		Subtype:     "poll-type",
		SubtypeID:   pollType,
	}

	teampoll.Feed.Sport = TeamPollSport{
		ID:   "/sport/" + sport,
		Name: sport,
	}

	leagueName := LeagueName{
		Type: "nick",
		Name: strings.ToUpper(name),
	}
	teampoll.Feed.LeagueContent.League.ID = fmt.Sprintf("/sport/%s/league", sport)
	teampoll.Feed.LeagueContent.League.Name = append(teampoll.Feed.LeagueContent.League.Name, leagueName)
	teampoll.Feed.LeagueContent.SeasonContent.Season.Name = seasonSpan
	teampoll.Feed.LeagueContent.SeasonContent.PollContent.Poll.Name = pollName

	teamrank := TeamPollRanking{
		Rank:     "RK",
		Previous: "NR",
		Points:   "PTS",
		FPVotes:  "",
	}

	var f func(*html.Node)
	cnt := 0
	status := ""
	hasFPV := false
	lastWeek := week
	f = func(n *html.Node) {
		//fmt.Println(n.Type, n.Attr, n.Data, n.DataAtom)
		switch n.Type {
		case html.ElementNode:
			switch n.Data {
			case "h1":
				for _, a := range n.Attr {
					if a.Key == "class" && a.Val == "h2" {
						status = "date"
						//fmt.Println("Date:", n.Data, status)
						break
					}
				}
			case "option":
				for _, a := range n.Attr {
					if a.Key == "value" {
						//fmt.Println("Drop:", n.Data, a.Val)
						paths := strings.Split(a.Val, "/")
						for i, p := range paths {
							if p == "week" {
								//fmt.Println("Week:", paths[i+1])
								lastWeek, _ = strconv.Atoi(paths[i+1])
							}
						}
					}
				}
			case "tr":
				for _, a := range n.Attr {
					if a.Key == "class" {
						if a.Val == "stathead" {
							status = "stats"
							//fmt.Println("Node:", n.Data, status)
							break
						} else {
							if status == "stats" {
								cnt = 0
								//fmt.Println("Team")
								if teamrank.Rank != "RK" && teamrank.Points != "PTS" {
									teampoll.Feed.LeagueContent.SeasonContent.PollContent.Teams = append(
										teampoll.Feed.LeagueContent.SeasonContent.PollContent.Teams, teamrank)
								}
							}
						}
					}
				}
			}
		case html.TextNode:
			if len(status) > 0 {
				switch status {
				case "date":
					title := strings.Split(n.Data, "(")
					short := title[len(title)-1]
					dt, _ := time.Parse("Jan. 2)", short)
					short = dt.Format("01-02")
					month, _ := strconv.Atoi(strings.Split(short, "-")[0])
					pollYear := season
					if month < 7 {
						pollYear = season + 1
					}
					teampoll.Feed.LeagueContent.SeasonContent.PollContent.Poll.Date = fmt.Sprintf("%d-%s", pollYear, short)
					teampoll.TypeID = strings.Replace(teampoll.Feed.LeagueContent.SeasonContent.PollContent.Poll.Date, "-", "", -1)
					//fmt.Println("Date:", teampoll.Feed.LeagueContent.SeasonContent.PollContent.Poll.Date)
					status = ""
				case "stats":
					if n.Data == "Others receiving votes:" {
						status = "others"
					} else {
						cnt++
						//fmt.Printf("Text: %d %q\n", cnt, n.Data)
						switch cnt {
						case 1:
							teamrank.Rank = n.Data
						case 2:
							teamrank.Team.Name = remap(n.Data)
							var teampage TeamPage
							for t := range teams.Page {
								data, _ := json.Marshal(teams.Page[t])
								json.Unmarshal(data, &teampage)
								if teampage.TeamFirst == teamrank.Team.Name {
									teamrank.Team.ID = teampage.TeamKey
								}
							}
						case 4:
							if strings.Contains(n.Data, "(") {
								hasFPV = true
								teamrank.FPVotes = strings.Replace(strings.Replace(n.Data, "(", "", -1), ")", "", -1)
							} else {
								hasFPV = false
								teamrank.Points = strings.Replace(n.Data, ",", "", -1)
								teamrank.FPVotes = ""
							}
						case 5:
							teamrank.Previous = n.Data
						case 6:
							if hasFPV {
								teamrank.Points = strings.Replace(n.Data, ",", "", -1)
							}
						case 7:
							if hasFPV {
								teamrank.Previous = n.Data
							}
						}
					}
				case "others":
					status = ""
					//fmt.Println("ELSE:", strings.Trim(n.Data, " "))
					if teamrank.Rank != "RK" && teamrank.Points != "PTS" {
						teampoll.Feed.LeagueContent.SeasonContent.PollContent.Teams = append(
							teampoll.Feed.LeagueContent.SeasonContent.PollContent.Teams, teamrank)
					}
					others := strings.Split(strings.Trim(n.Data, " "), ", ")
					for _, o := range others {
						//fmt.Println("ELSE:", o)
						rank := strings.Split(o, " ")
						//fmt.Printf("(%s)-(%s)\n", strings.Join(rank[:len(rank)-1], " "), rank[len(rank)-1])
						teamrank = TeamPollRanking{
							Points:  rank[len(rank)-1],
							FPVotes: "",
						}
						teamrank.Team.Name = strings.Join(rank[:len(rank)-1], " ")
						teampoll.Feed.LeagueContent.SeasonContent.PollContent.Teams = append(
							teampoll.Feed.LeagueContent.SeasonContent.PollContent.Teams, teamrank)
					}
				}
			}
		}
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			f(c)
		}
	}
	f(doc)

	output, _ := json.MarshalIndent(teampoll, "", "    ")
	//fmt.Println(string(output))

	// ${sport}_${LEAGUE}_team-polls_${pdate}_poll-type_${ptype}.json
	filename := fmt.Sprintf("%s_%s_team-polls_%s_poll-type_%s.json", sport, name, teampoll.TypeID, pollType)
	fmt.Println("Writing", filename)
	err = ioutil.WriteFile(filename, output, 0644)
	if err != nil {
		panic(err)
	}
	if week < lastWeek {
		getPoll(name, text, year, week+1)
	}
}

func page(id string, text string, year int, week int) string {
	url := fmt.Sprintf(text, year, week)
	if id == "ncaaf" {
		year--
		url = fmt.Sprintf(text, week, year)
	}
	return url
}

// fix known misnamed team names
func remap(name string) string {
	switch name {
	case "UConn":
		return "Connecticut"
	default:
		return name
	}
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
		teams = getTeams(i, *optYear)
		getPoll(i, p, *optYear, 1)
	}
}
