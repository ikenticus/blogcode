package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"strings"

	yaml "gopkg.in/yaml.v2"
)

// Settings contains the format and start/finish values of the loop
type Settings struct {
	Format string
	Start  int
	Finish int
}

func parseYaml() {
	base := strings.Split(path.Base(os.Args[0]), ".")[0]
	data, err := ioutil.ReadFile(base + ".yaml")
	if err != nil {
		panic(err)
	}

	var settings Settings
	err = yaml.Unmarshal(data, &settings)
	if err != nil {
		panic(err)
	}

	fmt.Println(settings.Format)
	for i := settings.Start; i <= settings.Finish; i++ {
		fmt.Printf(settings.Format, i)
	}
}

func main() {
	parseYaml()
}
