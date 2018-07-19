package helpers

import (
	"fmt"
)

func Check(config Config) {
	if debug {
		fmt.Println(config.APIKey, config.Front, config.SiteCode)
	}

	gqData, err := getGraphQL(config)
	if err != nil {
		fmt.Errorf("Failed to get GraphQL API\n")
	}
	jsData, err := getAPI(config)
	if err != nil {
		fmt.Errorf("Failed to get JSON API\n")
	}

	fmt.Println(gqData.Data.Front.DisplayName)
	fmt.Println(jsData.ReadModel.FrontDisplayName)
}
