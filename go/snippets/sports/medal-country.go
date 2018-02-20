package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "path"
    "sort"
    "strconv"
    "time"

    "github.com/pborman/getopt"
)

const (
    apiPath = "http://%s/svc/Games_v2.svc/json/%s?languageCode=2&competitionSetId=%d&season=%s"
    execPath = "/exec/crawl/infostrada?paths=Games_v2.svc/json/%s&filters=languageCode=2,competitionSetId=%d,season=%s,nocId=%d\n"
    queryString = "languageCode=2&competitionSetId=%d&season=%s&nocId=%d"
    module = "Games_v2"
)

var (
    baseName string
    gtype    int
    season   string
    nocIds   []int

    methods = map[string]string {
        "all": "GetNOCList",
        "win": "GetMedalTable_Season",
        "noc": "GetMedalTableNOCDetail_Season",
    }
)

// curl read.json | gojson -name=ReadData, then breaking apart
type InfoFeed struct {
    Method       string `json:"c_Method"`
    Module       string `json:"c_Module"`
    QueryString  string `json:"c_QueryString"`
}

type InfoData struct {
	Data []InfoFeed `json:"data"`
}

// curl methods[all] | gojson -name=NOCList
type NOCList []struct {
    NOCID    int    `json:"n_NOCID"`
    NOCGeoID int    `json:"n_NOCGeoID"`
    NOC      string `json:"c_NOC"`
    NOCShort string `json:"c_NOCShort"`
}

// curl methods[win] | gojson -name=MedalTable
type MedalTable struct {
    MedalTableInfo struct {
        AsOfDate        string      `json:"c_AsOfDate"`
        Sport           interface{} `json:"c_Sport"`
        SportShort      interface{} `json:"c_SportShort"`
        EventsFinished  int         `json:"n_EventsFinished"`
        EventsScheduled int         `json:"n_EventsScheduled"`
        EventsTotal     int         `json:"n_EventsTotal"`
        MedalsBronze    int         `json:"n_MedalsBronze"`
        MedalsGold      int         `json:"n_MedalsGold"`
        MedalsSilver    int         `json:"n_MedalsSilver"`
        MedalsTotal     int         `json:"n_MedalsTotal"`
        SportID         int         `json:"n_SportID"`
    } `json:"MedalTableInfo"`
    MedalTableNOC []struct {
        NOC           string `json:"c_NOC"`
        NOCShort      string `json:"c_NOCShort"`
        Bronze        int    `json:"n_Bronze"`
        Gold          int    `json:"n_Gold"`
        NOCGeoID      int    `json:"n_NOCGeoID"`
        NOCID         int    `json:"n_NOCID"`
        RankGold      int    `json:"n_RankGold"`
        RankSortGold  int    `json:"n_RankSortGold"`
        RankSortTotal int    `json:"n_RankSortTotal"`
        RankTotal     int    `json:"n_RankTotal"`
        Silver        int    `json:"n_Silver"`
        Total         int    `json:"n_Total"`
    } `json:"MedalTableNOC"`
}

func callAPI (url string) []byte {
    //fmt.Println("Parsing", url)

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

func getNocs (domain string, source string) {
    url := fmt.Sprintf(apiPath, domain, methods[source], gtype, season)
    data := callAPI(url)

    //var output []byte
    if source == "all" {
        var srcAll NOCList
        json.Unmarshal([]byte(data), &srcAll)
        //output, _ = json.MarshalIndent(srcAll, "", "    ")
        for _, n := range srcAll {
            nocIds = append(nocIds, n.NOCID)
        }
    } else {
        var srcWin MedalTable
        json.Unmarshal([]byte(data), &srcWin)
        //output, _ = json.MarshalIndent(srcWin, "", "    ")
        for _, m := range srcWin.MedalTableNOC {
            nocIds = append(nocIds, m.NOCID)
        }
    }
    //fmt.Println(string(output))
    sort.Ints(nocIds)
}

func printList (domain string, out string) {
    method := methods["noc"]
    switch out {
    case "curl":
        for _, n := range nocIds {
            fmt.Printf(apiPath + "&nocId=%d\n", domain, method, gtype, season, n)
        }
    case "exec":
        for _, n := range nocIds {
            fmt.Printf(execPath, method, gtype, season, n)
        }
    case "read":
        var data InfoData
        var feed InfoFeed
        for _, n := range nocIds {
            feed.Method = method
            feed.Module = module
            feed.QueryString = fmt.Sprintf(queryString, gtype, season, n)
            data.Data = append(data.Data, feed)
        }
        output, _ := json.MarshalIndent(data, "", "    ")
        fmt.Println(string(output))
    default:
        fmt.Printf("NOCS: %v\n", nocIds)
    }
}

func main() {
    baseName = path.Base(os.Args[0])
    thisYear := time.Now().Year()
    optHelp := getopt.BoolLong("help", 'h', "Help")
    optOut := getopt.StringLong("output", 'o', "", "Output Format")
    optSrc := getopt.StringLong("source", 's', "win", "Source URL")
    optUrl := getopt.StringLong("url", 'u', "", "Domain URL")
    optYear := getopt.IntLong("year", 'y', thisYear, "Season")
    getopt.Parse()

    if *optHelp {
        getopt.Usage()
        os.Exit(0)
    }

    if (*optYear % 2) == 1 {
        *optYear++
    }
    gtype = (*optYear % 4) / 2 + 1
    if gtype == 2 {
        season = fmt.Sprintf("%d%d", *optYear - 1, *optYear)
    } else {
        season = strconv.Itoa(*optYear)
    }

    getNocs(*optUrl, *optSrc)
    printList(*optUrl, *optOut)
}
