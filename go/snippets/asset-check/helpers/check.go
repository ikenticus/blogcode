package helpers

import (
	"fmt"
	"reflect"
	"strings"
)

type Tally struct {
	Total           int
	Pass            int
	Fail            int
	FailCountLayout int
	FailCountAsset  int
	FailSliceAsset  int
}

func loopFronts(config Config, fronts []string) {
	var count Tally
	count.Total = len(fronts)

	for _, f := range fronts {

		gqData, err := getGraphQL(config, f)
		if err != nil {
			fmt.Errorf("Failed to get GraphQL API\n")
		}

		jsData, err := getPresAPI(config, f)
		if err != nil {
			fmt.Errorf("Failed to get JSON API\n")
		}

		result := testFront(f, gqData, jsData)
		switch {
		case strings.HasPrefix(result, "FAIL"):
			count.Fail++
			switch {
			case strings.HasPrefix(result, "FAIL1"):
				count.FailCountLayout++
			case strings.HasPrefix(result, "FAIL2"):
				count.FailCountAsset++
			case strings.HasPrefix(result, "FAIL3"):
				count.FailSliceAsset++
			}
		case strings.HasPrefix(result, "PASS "):
			count.Pass++
		}
		fmt.Println(result)
	}

	fmt.Printf("\nTotal: %5d\nPass:  %5d\nFail:  %5d", count.Total, count.Pass, count.Fail)
	fmt.Printf("\n  Count Layout: %5d\n  Count Asset:  %5d\n  Slice Asset:  %5d\n", count.FailCountLayout, count.FailCountAsset, count.FailSliceAsset)
}

func testFront(f string, g GraphQL, j PresAPI) string {
	layoutModules := j.LayoutModules // diagAPI, presAPI
	//layoutModules = j.ReadModel.LayoutModules	// jsonAPI

	gLayoutCount := len(g.Data.Front.LayoutModules)
	jLayoutCount := len(layoutModules)
	if gLayoutCount != jLayoutCount {
		return fmt.Sprintf("FAIL1 %-50s: %s Mismatched Layout Mods (GQL %3d vs %3d API)", f, j.UpdatedDate, gLayoutCount, jLayoutCount)
	}

	var gAssetCount int
	var gAssetIDs []string
	for _, gModule := range g.Data.Front.LayoutModules {
		gAssetCount += len(gModule.Contents)
		for _, gAsset := range gModule.Contents {
			gAssetIDs = append(gAssetIDs, gAsset.ID)
		}
	}

	var jAssetCount int
	var jAssetIDs []string
	for _, jModule := range layoutModules {
		jAssetCount += len(jModule.Contents)
		for _, jAsset := range jModule.Contents {
			jAssetIDs = append(jAssetIDs, fmt.Sprintf("%d", jAsset.ID))
		}
	}

	switch {
	case gAssetCount != jAssetCount:
		return fmt.Sprintf("FAIL2 %-50s: %s Mismatched Asset Count (GQL %3d vs %3d API)", f, j.UpdatedDate, gAssetCount, jAssetCount)
	case !reflect.DeepEqual(gAssetIDs, jAssetIDs):
		return fmt.Sprintf("FAIL3 %-50s: %s Mismatched Asset IDs\n%+v\n%+v", f, j.UpdatedDate, gAssetIDs, jAssetIDs)
	default:
		return fmt.Sprintf("PASS  %-50s: %s All Checks Succeeded", f, j.UpdatedDate)
	}
}

func Check(config Config) error {
	if debug {
		fmt.Println(config.APIKey, config.Front, config.SiteCode)
		fmt.Println(config.Couchbase, config.Bucket, config.SASL)
		fmt.Println(config.Query)
	}

	fronts, err := runQuery(config)
	if err != nil {
		return err
	}

	loopFronts(config, fronts)
	return nil
}
