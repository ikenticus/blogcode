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
    Competition struct {
        Id        string `json:"id"`
        Officials []struct {
            FirstName string `json:"firstName,omitempty"`
            Id        string `json:"id,omitempty"`
            LastName  string `json:"lastName,omitempty"`
            Position  struct {
                Alias string `json:"alias,omitempty"`
                Id    string `json:"id,omitempty"`
                Name  string `json:"name,omitempty"`
            } `json:"position,omitempty"`
            Seasons int64 `json:"seasons,omitempty"`
        } `json:"officials,omitempty"`
        RecentMeetings []struct {
            Competition string `json:"competition,omitempty"`
            Season      string `json:"season,omitempty"`
        } `json:"recentMeetings"`
        StartDate time.Time `json:"startDate"`
        Status    string    `json:"status,omitempty"`
    } `json:"competition,omitempty"`
}
