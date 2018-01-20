package main
 
import (
    "crypto/hmac"
    "crypto/sha256"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"
    "path"
    "strings"
    "time"
 
    vaultApi "github.com/hashicorp/vault/api"
)
 
var myKeys = map[string]string{}
var scalrDate = fmt.Sprintf(time.Now().UTC().Format(time.RFC3339));
var scalrSearch = ""

const scalrPath = "https://scalr.gannettdigital.com"
const vaultPath = "secret/paas-api/paas-api-ci/production"
 
func init() {
    vaultConfig := vaultApi.DefaultConfig()
    vaultClient, err := vaultApi.NewClient(vaultConfig)
    if err != nil {
        fmt.Printf("An error occurred creating vaultClient: %v\n", err)
        return
    }
    dbConfig, err := vaultClient.Logical().Read(vaultPath)
    if err != nil {
        fmt.Printf("An error occurred reading secret: %v\n", err)
        return
    }
    myKeys["scalr-key-id"] = dbConfig.Data["scalraccess"].(string)
    myKeys["scalr-secret"] = dbConfig.Data["scalrsecret"].(string)
    return
}
 
func scalrCanonicalRequest (method string, date string, path string, params string, body string) string {
    return strings.Join([]string{method, date, path, params, body}, "\n")
}

func scalrSignatureAlgorithm (secret string, message string) string {
    key := []byte(secret)
    h := hmac.New(sha256.New, key)
    h.Write([]byte(message))
    return fmt.Sprintf("V1-HMAC-SHA256 %s", base64.StdEncoding.EncodeToString(h.Sum(nil)))
}

func scalrAPICall (path string, params string) string {
    //fmt.Println("Params: ", params)
    client := &http.Client{}
    req, _ := http.NewRequest("GET", scalrPath + path + "?" + params, nil)

    req.Header.Add("X-Scalr-Key-Id", myKeys["scalr-key-id"])
    req.Header.Add("X-Scalr-Signature", scalrSignatureAlgorithm(myKeys["scalr-secret"],
         scalrCanonicalRequest("GET", scalrDate, path, params, "")))
    req.Header.Add("X-Scalr-Date", scalrDate)
    //req.Header.Add("X-Scalr-Debug", "1")

    //fmt.Println(req);
    resp, _ := client.Do(req)
    defer resp.Body.Close()
    //fmt.Println(resp.Body);

 	htmlData, err := ioutil.ReadAll(resp.Body)
 	if err != nil {
 		fmt.Println(err)
 		os.Exit(1)
 	}
 	//fmt.Println(os.Stdout, string(htmlData)) 
    return string(htmlData)
}

func scalrAPIOut (apiKey string, apiPath string, params ...string) {
    apiQuery := ""
    if len(params) > 0 {
        apiQuery = params[0]
    }
    responseBody := scalrAPICall(apiPath, apiQuery)
    //fmt.Println(responseBody)

    var output map[string]interface{}
    err := json.Unmarshal([]byte(responseBody), &output)
    if err != nil {
        panic(err)
    }

    for _, val := range output["data"].([]interface{}) {
        data := val.(map[string]interface{})
        if scalrSearch == "" {
            fmt.Println(data["id"], ":", data[apiKey])
        } else {
            if strings.Contains(data[apiKey].(string), scalrSearch) {
                fmt.Println(data["id"], ":", data[apiKey])
            }
        }
    }

    //fmt.Println(output["pagination"])
    page := output["pagination"].(map[string]interface{})
    if page["next"] != nil {
        next := strings.Split(page["next"].(string), "?")[1]
        //fmt.Println(page["last"], ":", page["next"], "=>", next)
        scalrAPIOut(apiKey, apiPath, next)
    }
}

func searchCheck (userId string) string {
    if strings.Contains(userId, "=") {
        val := strings.Split(userId, "=")
        scalrSearch = val[1]
        return val[0]
    } else {
        return userId
    }
}

func showUsage() {
    fmt.Printf("Usage: %s <ENVID> <FARMID> <ROLEID>\n  Add: =SEARCH on last param to filter\n\n", path.Base(os.Args[0]))
}

func main() {
    //test()
    //fmt.Println(scalrDate);
    //fmt.Printf("Scalr %v / %v\n", myKeys["scalr-key-id"], myKeys["scalr-secret"])

    //fmt.Println(len(os.Args[1:]), os.Args[1:])
    showUsage()
    switch len(os.Args[1:]) {
        case 3:
            scalrAPIOut("privateIp", fmt.Sprintf("/api/v1beta0/user/%s/farm-roles/%s/servers/", os.Args[1], os.Args[3]))
        case 2:
            farmId := searchCheck(os.Args[2])
            scalrAPIOut("alias", fmt.Sprintf("/api/v1beta0/user/%s/farms/%s/farm-roles/", os.Args[1], farmId))
        case 1:
            envId := searchCheck(os.Args[1])
            scalrAPIOut("name", fmt.Sprintf("/api/v1beta0/user/%s/farms/", envId))
        default:
            scalrAPIOut("name", "/api/v1beta0/account/1/environments")
    }
    return
}
