package helpers

import (
	"fmt"
	"reflect"
	"strings"
)

type Tally struct {
	Fail  int
	Pass  int
	Total int
}

func loopFronts(config Config, fronts []string) {
	var count Tally
	count.Total = len(fronts)

	for _, f := range fronts {

		gqData, err := getGraphQL(config, f)
		if err != nil {
			fmt.Errorf("Failed to get GraphQL API\n")
		}

		jsData, err := getAPI(config, f)
		if err != nil {
			fmt.Errorf("Failed to get JSON API\n")
		}

		result := testFront(f, gqData, jsData)
		switch {
		case strings.HasPrefix(result, "FAIL "):
			count.Fail++
		case strings.HasPrefix(result, "PASS "):
			count.Pass++
		}
		fmt.Println(result)
	}

	fmt.Printf("\nTotal: %5d\nFail:  %5d\nPass:  %5d\n", count.Total, count.Fail, count.Pass)
}

func testFront(f string, g GraphQL, j JSONAPI) string {
	gLayoutCount := len(g.Data.Front.LayoutModules)
	jLayoutCount := len(j.ReadModel.LayoutModules)
	if gLayoutCount != jLayoutCount {
		return fmt.Sprintf("FAIL %-50s: Mismatched Layout Mods (GQL %3d vs %3d API)", f, gLayoutCount, jLayoutCount)
	}

	var gAssetCount int
	var gAssetIDs []string
	for _, gModule := range g.Data.Front.LayoutModules {
		gAssetCount += len(gModule.Contents)
		//fmt.Printf("  gMODULE: %s\n", gModule.ModuleDisplayName)
		for _, gAsset := range gModule.Contents {
			gAssetIDs = append(gAssetIDs, gAsset.ID)
			//fmt.Printf("    gASSET: %+v %s\n", gAsset, gAsset.ID)
		}
	}

	var jAssetCount int
	var jAssetIDs []string
	for _, jModule := range j.ReadModel.LayoutModules {
		jAssetCount += len(jModule.Contents)
		//fmt.Printf("  jMODULE: %s\n", jModule.ModuleDisplayName)
		for _, jAsset := range jModule.Contents {
			jAssetIDs = append(jAssetIDs, fmt.Sprintf("%d", jAsset.ID))
			//fmt.Printf("    jASSET: %+v %d\n", jAsset, jAsset.ID)
		}
	}

	switch {
	case gAssetCount != jAssetCount:
		return fmt.Sprintf("FAIL %-50s: Mismatched Asset Count (GQL %3d vs %3d API)", f, gAssetCount, jAssetCount)
	case !reflect.DeepEqual(gAssetIDs, jAssetIDs):
		return fmt.Sprintf("FAIL %-50s: Mismatched Asset IDs\n%+v\n%+v", f, gAssetIDs, jAssetIDs)
	default:
		return fmt.Sprintf("PASS %-50s: All Checks Succeeded", f)
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
