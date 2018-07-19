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
		AggregateName    string `json:"aggregateName"`
		FrontDisplayName string `json:"frontDisplayName"`
		FrontID          int64  `json:"frontId"`
		FrontName        string `json:"frontName"`
		FrontParentID    int64  `json:"frontParentId"`
		ID               string `json:"id"`
		LayoutModules    []struct {
			Contents []struct {
				Headline   string `json:"headline"`
				ID         int64  `json:"id"`
				PromoImage struct {
					AggregateID          string      `json:"aggregateId"`
					AssetGroupID         int64       `json:"assetGroupId"`
					AssetGroupName       string      `json:"assetGroupName"`
					ContentSourceCode    string      `json:"contentSourceCode"`
					ContentSourceName    string      `json:"contentSourceName"`
					CreatedBySystem      string      `json:"createdBySystem"`
					CreatedByUser        string      `json:"createdByUser"`
					CreatedDate          string      `json:"createdDate"`
					Expiration           string      `json:"expiration"`
					ID                   int64       `json:"id"`
					LastPublishedDate    string      `json:"lastPublishedDate"`
					OriginalURL          string      `json:"originalUrl"`
					PromoBrief           string      `json:"promoBrief"`
					PromoHeadline        interface{} `json:"promoHeadline"`
					PromoImageID         interface{} `json:"promoImageId"`
					PropertyDisplayName  string      `json:"propertyDisplayName"`
					PropertyID           int64       `json:"propertyId"`
					PropertyName         string      `json:"propertyName"`
					ReadModelName        string      `json:"readModelName"`
					ScheduledPublishDate string      `json:"scheduledPublishDate"`
					ShortURL             string      `json:"shortUrl"`
					SiteCode             string      `json:"siteCode"`
					Title                string      `json:"title"`
					UpdatedBySystem      string      `json:"updatedBySystem"`
					UpdatedByUser        string      `json:"updatedByUser"`
					UpdatedDate          string      `json:"updatedDate"`
					URL                  string      `json:"url"`
					UserUpdatedDate      string      `json:"userUpdatedDate"`
				} `json:"promoImage"`
			} `json:"contents"`
			LayoutModuleID    string `json:"layoutModuleId"`
			ModuleDisplayName string `json:"moduleDisplayName"`
			ModuleID          int64  `json:"moduleId"`
			ModuleName        string `json:"moduleName"`
			ModulePosition    int64  `json:"modulePosition"`
		} `json:"layoutModules"`
		LayoutName      string `json:"layoutName"`
		SiteCode        string `json:"siteCode"`
		SiteID          int64  `json:"siteId"`
		UpdatedBySystem string `json:"updatedBySystem"`
		UpdatedByUser   string `json:"updatedByUser"`
		UpdatedDate     string `json:"updatedDate"`
		UserUpdatedDate string `json:"userUpdatedDate"`
	} `json:"readModel"`
}

func getAPI(config Config) (source JSONAPI, e error) {
	url := strings.Replace(config.URL.API, "{FRONTNAME}", config.Front, -1)
	fmt.Println(url)
	res, err := goreq.Request{Uri: url}.Do()
	if err != nil {
		return source, fmt.Errorf("Error retrieve JSON API %s: %v", url, err)
	}
	res.Body.FromJsonTo(&source)
	return source, nil
}

func getGraphQL(config Config) (source GraphQL, e error) {
	url := strings.Replace(config.URL.GraphQL, "{FRONTNAME}", config.Front, -1)
	fmt.Println(url)
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
