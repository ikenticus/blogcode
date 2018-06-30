package merge

type Child struct {
	Base

	Competition struct {
		Away struct {
			Player struct {
				FirstName  string `json:"firstName"`
				Id         string `json:"id"`
				Statistics []struct {
					GamesClean       int64  `json:"gamesClean,omitempty"`
					GamesLost        int64  `json:"gamesLost,omitempty"`
					GamesPlayed      int64  `json:"gamesPlayed,omitempty"`
					GamesScoredFirst int64  `json:"gamesScoredFirst,omitempty"`
					GamesTied        int64  `json:"gamesTied,omitempty"`
					GamesWon         int64  `json:"gamesWon,omitempty"`
					GoalsHalf1       int64  `json:"goalsHalf1,omitempty"`
					GoalsHalf2       int64  `json:"goalsHalf2,omitempty"`
					Key              string `json:"key,omitempty"`
				} `json:"statistics"`
			} `json:"player"`
			Team struct {
				Id         string `json:"id"`
				Name       string `json:"name"`
				Statistics []struct {
					GamesClean       int64  `json:"gamesClean,omitempty"`
					GamesLost        int64  `json:"gamesLost,omitempty"`
					GamesPlayed      int64  `json:"gamesPlayed,omitempty"`
					GamesScoredFirst int64  `json:"gamesScoredFirst,omitempty"`
					GamesTied        int64  `json:"gamesTied,omitempty"`
					GamesWon         int64  `json:"gamesWon,omitempty"`
					GoalsHalf1       int64  `json:"goalsHalf1,omitempty"`
					GoalsHalf2       int64  `json:"goalsHalf2,omitempty"`
					Key              string `json:"key,omitempty"`
				} `json:"statistics"`
			} `json:"team"`
		} `json:"away"`
		Home struct {
			Player struct {
				FirstName  string `json:"firstName"`
				Id         string `json:"id"`
				Statistics []struct {
					GamesClean       int64  `json:"gamesClean,omitempty"`
					GamesLost        int64  `json:"gamesLost,omitempty"`
					GamesPlayed      int64  `json:"gamesPlayed,omitempty"`
					GamesScoredFirst int64  `json:"gamesScoredFirst,omitempty"`
					GamesTied        int64  `json:"gamesTied,omitempty"`
					GamesWon         int64  `json:"gamesWon,omitempty"`
					GoalsHalf1       int64  `json:"goalsHalf1,omitempty"`
					GoalsHalf2       int64  `json:"goalsHalf2,omitempty"`
					Key              string `json:"key,omitempty"`
				} `json:"statistics"`
			} `json:"player"`
			Team struct {
				Id         string `json:"id"`
				Name       string `json:"name"`
				Statistics []struct {
					GamesClean       int64  `json:"gamesClean,omitempty"`
					GamesLost        int64  `json:"gamesLost,omitempty"`
					GamesPlayed      int64  `json:"gamesPlayed,omitempty"`
					GamesScoredFirst int64  `json:"gamesScoredFirst,omitempty"`
					GamesTied        int64  `json:"gamesTied,omitempty"`
					GamesWon         int64  `json:"gamesWon,omitempty"`
					GoalsHalf1       int64  `json:"goalsHalf1,omitempty"`
					GoalsHalf2       int64  `json:"goalsHalf2,omitempty"`
					Key              string `json:"key,omitempty"`
				} `json:"statistics"`
			} `json:"team"`
		} `json:"home"`
	} `json:"competition1"`
}
