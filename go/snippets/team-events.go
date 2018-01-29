package main

import (
    "encoding/json"
    "fmt"
    "html"
    "io/ioutil"
    "net/http"
    "os"
    "sort"
    "strings"
    "text/template"
    "time"

    "github.com/pborman/getopt"
)

type EventPage struct {
    EventKey        string      `json:"event_key"`
    StartDate       time.Time   `json:"start_date"`
    DateTime        string      `json:"date_time"`
    EventStatus     string      `json:"event_status"`
    GameStatus      string      `json:"game_status"`
    AwayKey         string      `json:"away_key"`
    AwayScore       int         `json:"away_score"`
    HomeKey         string      `json:"home_key"`
    HomeScore       int         `json:"home_score"`
    VenueName       string      `json:"venue_name"`
    SubSeason       string      `json:"sub_season"`
    TVCoverage      string      `json:"tv_coverage"`
}

type EventsAPI struct {
    Environment         string      `json:"environment"`
    LastModified        time.Time   `json:"last_modified"`
    Page                []EventPage `json:"page"`
}

type Event struct {
    Alignment   string
    StartDate   time.Time
    SubSeason   string
    VenueName   string
    VsCity      string
    VsName      string
}

type EventMap map[string][]Event

type TeamsAPI struct {
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

type TeamEventMap struct {
    Season  int
    League  string
    Teams   []string
    Events  map[string][]Event
}

var (
    teamMap TeamMap
    eventMap EventMap
    teamEventMap TeamEventMap
)

const (
    apiPath = "http://sports-service.production.gannettdigital.com/page/v2/%s/%s/%d/"
)

func callAPI (league string, subtype string, year int) []byte {
    url := fmt.Sprintf(apiPath, league, subtype, year)
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
    return data
}

func buildTeams (league string, year int) {
    data := callAPI(league, "teams", year)

    var teams TeamsAPI
    json.Unmarshal([]byte(data), &teams)
    //fmt.Println(teams.Page)

    teamMap = make(TeamMap)
    for _, t := range teams.Page {
        teamMap[t.TeamKey] = Team {
            City: t.TeamFirst,
            Name: t.TeamLast,
        }
    }
}

func appendEvent (e EventPage, align string) {
    alignment := "home"
    myTeam := teamMap[e.HomeKey].Name
    vsCity := teamMap[e.AwayKey].City
    vsName := teamMap[e.AwayKey].Name
    if align == e.AwayKey {
        alignment = "away"
        myTeam = teamMap[e.AwayKey].Name
        vsCity = teamMap[e.HomeKey].City
        vsName = teamMap[e.HomeKey].Name
    }

    event := Event {
        Alignment: alignment,
        StartDate: e.StartDate,
        SubSeason: e.SubSeason,
        VenueName: e.VenueName,
        VsCity: vsCity,
        VsName: vsName,
    }
    if eventMap == nil {
        eventMap = make(EventMap)
    }
    eventMap[myTeam] = append(eventMap[myTeam], event)
}

func buildEvents (league string, year int) {
    data := callAPI(league, "events", year)

    var events EventsAPI
    json.Unmarshal([]byte(data), &events)
    //fmt.Println(events.Page)

    for _, e := range events.Page {
        appendEvent(e, e.AwayKey)
        appendEvent(e, e.HomeKey)
    }
}
// preseason Mar. 05 / Brewers, Tempe /  2:10
// L.A. Angels Apr. 6 at Seattle,  4:10

func formatDate(t time.Time) string {
    return t.Format("Jan. 2")
}

func formatHtml(s string) string {
    return html.EscapeString(s)
}

func formatTime(t time.Time) string {
    return t.Format("3:04")
}

func callTemplates (season string, league string, year int) {
    fmap := template.FuncMap{
        "formatDate": formatDate,
        "formatHtml": formatHtml,
        "formatTime": formatTime,
        //"formatAsDollars": formatAsDollars,
        //"formatAsDate": formatAsDate,
        //"urgentNote": urgentNote,
    }

    output := fmt.Sprintf("%s_%d_%s.doc", strings.ToUpper(league), year, season)
    f, ferr := os.Create(output)
    if ferr != nil {
        fmt.Println("create file: ", ferr)
        return
    }

    xmlFile := season + ".xml"
    t := template.Must(template.New(xmlFile).Funcs(fmap).ParseFiles(xmlFile))
    err := t.Execute(f, teamEventMap)
    if err != nil {
        panic(err)
    } else {
        fmt.Println("Generated", output)
    }
}

func sortData (league string, year int) {
    teams := make([]string, 0)
    for _, t := range teamMap {
        teams = append(teams, t.Name)
    }
    sort.Strings(teams)
    teamEventMap.League = strings.ToUpper(league)
    teamEventMap.Season = year
    teamEventMap.Teams = teams
    teamEventMap.Events = eventMap
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
    //fmt.Println(teamMap)
    //output, _ := json.MarshalIndent(teamMap, "", "    "); fmt.Println(string(output))

    buildEvents(*optAbbr, *optYear)
    //fmt.Println(eventMap)
    //output, _ := json.MarshalIndent(eventMap, "", "    "); fmt.Println(string(output))

    sortData(*optAbbr, *optYear)
    //fmt.Println(teamEventMap)
    //output, _ := json.MarshalIndent(teamEventMap, "", "    "); fmt.Println(string(output))

    callTemplates("pre", *optAbbr, *optYear)
    callTemplates("regular", *optAbbr, *optYear)
}
