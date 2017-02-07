
package main

import (
	"github.com/gorilla/mux"
    sp_spotcontrol "github.com/JayRod12/stealth_phoenix_spotcontrol"
	"net/http"
	"fmt"
	"encoding/json"
    "os/exec"
    //"strings"
    "net/url"
    "strconv"
    "bytes"
    "time"
)

type MonzoTransaction struct{
	Type string
}

func main() {
    r := mux.NewRouter()
    r.HandleFunc("/monzo", postMembersHandler).Methods("POST")

    http.Handle("/", r)
    http.ListenAndServe("129.31.186.106:8080", nil)
    fmt.Println("Waiting for POST request from Monzo")
}


func postMembersHandler(w http.ResponseWriter, r *http.Request) {
	var m MonzoTransaction
    err := json.NewDecoder(r.Body).Decode(&m)
    if err != nil {
        http.Error(w, err.Error(), 400)
        return
    }
    if m.Type == "transaction.created" {
    	fmt.Println("Monzo Transaction Received!")
    	fmt.Println("---------------> Spotify")
    	activate_librespot()
    }
}

func send_done(id string) {
    apiUrl := "http://129.31.234.152:3000"
    resource := "/done"
    data := url.Values{}
    data.Set("id", id)

    u, _ := url.ParseRequestURI(apiUrl)
    u.Path = resource
    urlStr := fmt.Sprintf("%v", u)

    client := &http.Client{}
    r, _ := http.NewRequest("POST", urlStr, bytes.NewBufferString(data.Encode()))
    r.Header.Add("Content-Type", "application/x-www-form-urlencoded")
    r.Header.Add("Content-Length", strconv.Itoa(len(data.Encode())))

    resp, _ := client.Do(r)
    fmt.Println(resp.Status)
}

func activate_librespot() {
    send_done("0")
	sp_spotcontrol.Play_local()
    time.Sleep(5 * time.Second)
    send_done("1")
    time.Sleep(5 * time.Second)
    cmd := exec.Command("/bin/sh", "./next")
    cmd.Run()
}