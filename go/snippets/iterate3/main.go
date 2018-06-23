package main

import (
    "encoding/json"
    "fmt"    
    "reflect"
)

func main() {
    // Creating the maps for JSON
    m := map[string]interface{}{}

    // Parsing/Unmarshalling JSON encoding/json
    err := json.Unmarshal([]byte(input), &m)

    if err != nil {
        panic(err)
    }
    parseMap(m)
}

func parseMap(aMap map[string]interface{}) {
    for key, val := range aMap {
		switch reflect.TypeOf(val).Kind() {
        case reflect.Map:
            fmt.Println(key, ": parseMap")
            parseMap(val.(map[string]interface{}))
        case reflect.Slice:
            fmt.Println(key, ": parseArray")
            parseArray(val.([]interface{}))
		case reflect.String:
            fmt.Println(key, ":", val.(string))
        }
    }
}

func parseArray(anArray []interface{}) {
    for i, val := range anArray {
        switch concreteVal := val.(type) {
        case map[string]interface{}:
            fmt.Println("Index:", i)
            parseMap(val.(map[string]interface{}))
        case []interface{}:
            fmt.Println("Index:", i)
            parseArray(val.([]interface{}))
        default:
            fmt.Println("Index", i, ":", concreteVal)

        }
    }
}

const input = `
{"meta":{"requestId":"ec2bd542-8207-478f-8f40-37c0626077ed"},"data":[{"id":3,"name":"Gannett Digital Production","added":"2015-04-21T18:18:42Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":4,"name":"Gannett Digital Staging","added":"2015-04-21T18:19:46Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":5,"name":"Gannett Digital Development","added":"2015-04-21T18:19:59Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":6,"name":"Gannett Digital Sandbox","added":"2015-04-21T18:20:17Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":9,"name":"Gannett Digital Feature","added":"2015-05-11T18:54:08Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":10,"name":"Gannett Digital Training","added":"2015-05-11T18:54:22Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":11,"name":"Gannett Digital Tools","added":"2015-05-11T18:55:18Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":24,"name":"scalr-test","added":"2016-03-23T18:09:45Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":25,"name":"PaaS-Tools","added":"2016-04-28T15:25:00Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":33,"name":"PaaS-Development","added":"2017-03-31T17:07:54Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":34,"name":"PaaS-Staging","added":"2017-03-31T17:25:07Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":36,"name":"PaaS-Production","added":"2017-03-31T17:28:08Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}},{"id":38,"name":"Product Development","added":"2017-09-13T16:35:06Z","status":"active","costCenter":{"id":"c6562c98-1dbd-4958-936c-047756e7ad52"}}],"pagination":{"first":null,"last":null,"prev":null,"next":null},"warnings":[]}
`
