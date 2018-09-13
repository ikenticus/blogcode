package main

import (
    "encoding/json"
    "encoding/xml"
	"fmt"
	"io/ioutil"
    "os"
    "time"
)

type Vote struct {
	ElectionDate string    `json:"electionDate" xml:"ElectionDate,attr"`
	Timestamp    time.Time `json:"timestamp" xml:"Timestamp,attr"`
	Races        []Race    `json:"Races" xml:"Race"`
	NextRequest  string    `json:"nextrequest" xml:"NextRequest"`
}

type Race struct {
	Test           bool             `json:"test" xml:"Test,attr"`
	RaceID         string           `json:"raceID" xml:"ID,attr"`
	RaceType       string           `json:"raceType" xml:"Type,attr"`
	RaceTypeID     string           `json:"raceTypeID" xml:"TypeID,attr"`
	OfficeID       string           `json:"officeID" xml:"OfficeID,attr"`
	OfficeName     string           `json:"officeName" xml:"OfficeName,attr`
	NumRunoff      int              `json:"numRunoff" xml:"NumRunOff,attr"`
	National       bool             `json:"national" xml:"National,attr"`
	ReportingUnits []ReportingUnit  `json:"ReportingUnits" xml:"ReportingUnit"`
}

type ReportingUnit struct {
	StatePostal           string        `json:"statePostal" xml:"StatePostal,attr"`
	StateName             string        `json:"stateName"`
	Level                 string        `json:"level" xml:"Level,attr"`
	LastUpdated           time.Time     `json:"lastUpdated" xml:"LastUpdated,attr"`
	ReportingunitName     string        `json:"reportingunitName" xml:"Name,attr"`
	ReportingunitID       string        `json:"reportingunitID" xml:"ID,attr"`
	FipsCode              string        `json:"fipsCode" xml:"FIPSCode,attr"`
	PrecinctsReporting    int           `json:"precinctsReporting"`
	PrecinctsTotal        int           `json:"precinctsTotal"`
	PrecinctsReportingPct float64       `json:"precinctsReportingPct"`
    Precincts             Precinct      `json:"Precincts" xml:"Precincts"`
	Candidates            []Candidate   `json:"Candidates" xml:"Candidate"`
}

type Precinct struct {
	Reporting       int         `json:"precinctsReporting" xml:"Reporting,attr"`
	ReportingPct    float64     `json:"precinctsReportingPct" xml:"ReportingPct,attr"`
	Total           int         `json:"precinctsTotal" xml:"Total,attr"`
}

type Candidate struct {
	FirstName   string `json:"firstname" xml:"First,attr"`
	LastName    string `json:"lastname" xml:"Last,attr"`
	Abbrv       string `json:"abbrv" xml:"Abbrv,attr"`
	Party       string `json:"party" xml:"Party,attr"`
	Incumbent   bool   `json:"incumbent" xml:"Incumbent,attr"`
	CandidateID string `json:"candidateID" xml:"ID,attr"`
	PolID       string `json:"polID" xml:"PolID,attr"`
	BallotOrder int    `json:"ballotOrder" xml:"BallotOrder,attr"`
	PolNum      string `json:"polNum" xml:"PolNum,attr"`
	VoteCount   int    `json:"voteCount" xml:"VoteCount,attr"`
	Winner      string `json:"winner" xml:"Winner,attr"`
}

func main() {
	source := os.Args[1]
	input, err := ioutil.ReadFile(source)
	if err != nil {
		fmt.Errorf("failed to read xml file %q: %v", source, err)
		os.Exit(10)
	}
	fmt.Println(string(input))

    var data Vote
    err = xml.Unmarshal(input, &data)
	fmt.Printf("DATA: %+v\n", data)
	if err != nil {
		fmt.Printf("failed to unmarshal %s to xml: %v", source, err)
		os.Exit(20)
	}
    pretty, _ := xml.MarshalIndent(data, "", "    ")
    fmt.Println(string(pretty))

    /*
    var clean interface{}
    json.Unmarshal(output.Bytes(), &clean)
    pretty, _ := json.MarshalIndent(clean, "", "    ")
    */

    pretty, _ = json.MarshalIndent(data, "", "    ")
    fmt.Println(string(pretty))
}

