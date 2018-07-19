package helpers

import (
	"fmt"
	"strings"

	"github.com/franela/goreq"
)

// curl config.URL.GraphQL | gojson --name GraphQL
type GraphQL struct {
	Data struct {
		Front struct {
			DisplayName   string `json:"displayName"`
			ID            string `json:"id"`
			LayoutModules []struct {
				Contents []struct {
					Asset struct {
						ContentSourceCode string `json:"contentSourceCode"`
						Headline          string `json:"headline"`
						ID                string `json:"id"`
						Type              string `json:"type"`
					} `json:"asset"`
					ID string `json:"id"`
				} `json:"contents"`
				ModuleDisplayName string `json:"moduleDisplayName"`
			} `json:"layoutModules"`
		} `json:"front"`
	} `json:"data"`
}

// curl config.URL.API | gojson --name JSONAPI
type JSONAPI struct {
	ID        string `json:"id"`
	ReadModel struct {
		FrontDisplayName string `json:"frontDisplayName"`
		ID               string `json:"id"`
		LayoutModules    []struct {
			Contents []struct {
				Headline   string `json:"headline"`
				ID         int64  `json:"id"`
				PromoImage struct {
					SiteCode string `json:"siteCode"`
				} `json:"promoImage"`
			} `json:"contents"`
			LayoutModuleID    string `json:"layoutModuleId"`
			ModuleDisplayName string `json:"moduleDisplayName"`
		} `json:"layoutModules"`
		SiteCode string `json:"siteCode"`
		SiteID   int64  `json:"siteId"`
	} `json:"readModel"`
}

func getAPI(config Config, front string) (source JSONAPI, e error) {
	url := strings.Replace(config.URL.API, "{FRONTNAME}", front, -1)
	res, err := goreq.Request{Uri: url}.Do()
	if err != nil {
		return source, fmt.Errorf("Error retrieve JSON API %s: %v", url, err)
	}
	res.Body.FromJsonTo(&source)
	return source, nil
}

func getGraphQL(config Config, front string) (source GraphQL, e error) {
	url := strings.Replace(config.URL.GraphQL, "{FRONTNAME}", front, -1)
	res, err := goreq.Request{Uri: url}.
		WithHeader("X-API-Key", config.APIKey).
		WithHeader("X-SiteCode", config.SiteCode).
		Do()
	if err != nil {
		return source, fmt.Errorf("Error retrieve JSON API %s: %v", url, err)
	}
	res.Body.FromJsonTo(&source)
	return source, nil
}
