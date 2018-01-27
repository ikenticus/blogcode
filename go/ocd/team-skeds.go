package main

import (
/*
    "regexp"
    "sort"
    "strconv"
    "strings"
*/
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "time"

    "github.com/pborman/getopt"
)

type Teams struct {
    Environment         string      `json:"environment"`
    LastModified        time.Time   `json:"last_modified"`
    Page                []struct {
        ConferenceKey   string      `json:"conference_key"`
        ConferenceName  string      `json:"conference_name"`
        DivisionKey     string      `json:"division_key"`
        DivisionName    string      `json:"division_name"`
        TeamAbbr        string      `json:"team_abbr"`
        TeamFirst       string      `json:"team_first"`
        TeamKey         string      `json:"team_key"`
        TeamLast        string      `json:"team_last"`
        TeamSlug        string      `json:"team_slug"`
    } `json:"page"`
}

type Team struct {
    City    string
    Name    string
}

type TeamMap map[string]Team

var (
    teamMap TeamMap
)

const (
    apiPath = "http://sports-service.production.gannettdigital.com/page/v2/%s/%s/%d/"
)

func buildTeams (league string, year int) {
    url := fmt.Sprintf(apiPath, league, "teams", year)
    fmt.Println("Parsing", url)

    client := &http.Client{}
    req, _ := http.NewRequest("GET", url, nil)
    resp, _ := client.Do(req)
    defer resp.Body.Close()

    data, err := ioutil.ReadAll(resp.Body)
 	if err != nil {
 		fmt.Println(err)
 		os.Exit(1)
 	}

    var teams Teams
    err = json.Unmarshal([]byte(data), &teams)
    if err != nil {
        panic(err)
    }
    //fmt.Println(teams.Page)

    teamMap = make(TeamMap)
    for _, t := range teams.Page {
        teamMap[t.TeamKey] = Team {
            City: t.TeamFirst,
            Name: t.TeamLast,
        }
    }
}

func main() {
    thisYear := time.Now().Year()
    optHelp := getopt.BoolLong("help", 'h', "Help")
    optAbbr := getopt.StringLong("abbr", 'a', "mlb", "League Abbr")
    optYear := getopt.IntLong("year", 'y', thisYear, "Year/Season")
    getopt.Parse()

    if *optHelp {
        getopt.Usage()
        os.Exit(0)
    }

    buildTeams(*optAbbr, *optYear)
    fmt.Println(teamMap)
}
