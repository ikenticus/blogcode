package merge

import "time"

type Base struct {
	DataType string `json:"dataType"`
	Id       string `json:"id"`
	League   struct {
		Alias string `json:"alias"`
		Id    string `json:"id"`
		Name  string `json:"name"`
	} `json:"league"`
	Season struct {
		EndDate   time.Time `json:"endDate"`
		Id        string    `json:"id"`
		Name      string    `json:"name"`
		StartDate time.Time `json:"startDate"`
	} `json:"season"`
	Game `json:"competition"`
}
