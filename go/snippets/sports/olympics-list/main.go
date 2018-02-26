package main

import (
    "fmt"
    "os"
    "path"
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
    listIds  []int

    methods = map[string]string {
        "nocs": "GetNOCList",
        "medals": "GetMedalTable_Season",
        "nocmedals": "GetMedalTableNOCDetail_Season",
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

func getIds (domain string, source string) {
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

func main() {
    baseName = path.Base(os.Args[0])
    thisYear := time.Now().Year()
    optHelp := getopt.BoolLong("help", 'h', "Help")
    optOut := getopt.StringLong("output", 'o', "", "Output Format")
    optUrl := getopt.StringLong("url", 'u', "", "Domain URL")
    optType := getopt.StringLong("type", 's', "date", "List Type")
    optYear := getopt.IntLong("year", 'y', thisYear, "Season")
    getopt.Parse()

    defer fmt.Println(*optOut, *optType, *optUrl)

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

    //defer printList(*optUrl, *optOut)
}
