package helpers

import (
	"fmt"
	"reflect"
	"strconv"
	"strings"
)

func getField(c Config, key string) reflect.Value {
	v := reflect.ValueOf(c)
	for _, s := range strings.Split(key, ".") {
		v = v.FieldByName(s)
	}
	return v
}

func convertSlice(c Config, dataSlice []string) (ifaceSlice []interface{}, lists []string) {
	ifaceSlice = make([]interface{}, len(dataSlice))
	for i, d := range dataSlice {
		val := getField(c, "URL."+d)
		switch reflect.Value(val).Kind() {
		case reflect.Slice:
			ifaceSlice[i] = "{" + d + "}"
			lists = append(lists, d)
		case reflect.String:
			ifaceSlice[i] = val
		}
	}
	return ifaceSlice, lists
}

func replaceList(src []string, target string, ids []int) (results []string) {
	for _, s := range src {
		for _, i := range ids {
			results = append(results, strings.Replace(s, target, strconv.Itoa(i), 1))
		}
	}
	return results
}

func buildFiles(c Config, p Paths) (files []string) {
	values, lists := convertSlice(c, p.Params)
	for _, f := range p.Formats {
		line := fmt.Sprintf(f, values...)
		if len(lists) == 0 {
			files = append(files, line)
		} else {
			var temp []string
			temp = append(temp, line)
			for _, v := range lists {
				temp = replaceList(temp, "{"+v+"}", getField(c, "URL."+v).Interface().([]int))
			}
			files = append(files, temp...)
		}
	}
	return files
}
