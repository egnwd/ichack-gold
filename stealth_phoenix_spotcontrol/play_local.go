package stealth_phoenix_spotcontrol

import (
	"flag"
	"fmt"
	"github.com/badfortrains/spotcontrol"
	"strings"
	"io/ioutil"
)

const defaultdevicename = "SpotControl"

func Play_local() {
	// fmt.Println("Play song")
	user, _ := ioutil.ReadFile("/Users/jaime/Workspace/golang/src/github.com/JayRod12/stealth_phoenix_spotcontrol/username")
	username := string(user)
	fmt.Println(username)
	username = strings.Replace(username, "\n", "", -1)
	pass, _ := ioutil.ReadFile("/Users/jaime/Workspace/golang/src/github.com/JayRod12/stealth_phoenix_spotcontrol/password")
	password := string(pass)
	fmt.Println(password)
	password = strings.Replace(password, "\n", "", -1)
	appkey := flag.String("appkey", "/Users/jaime/Workspace/golang/src/github.com/JayRod12/stealth_phoenix_spotcontrol/random.key", "spotify appkey file path")
	devicename := flag.String("devicename", defaultdevicename, "name of device")
	flag.Parse()

	var sController *spotcontrol.SpircController
	var err error

	sController, err = spotcontrol.Login(username, password, *appkey, *devicename)

	if err != nil {
		fmt.Println("Error logging in: ", err)
		return
	}

	devices := sController.ListDevices()
	for {
		if len(devices) > 0 {
			break
		}
		devices = sController.ListDevices()
	}
	track := make([]string, 1)
	track[0] = "6Nf1bklus7o9fpKto13nDc" // OK Go - This too shall pass
	sController.LoadTrack(devices[0].Ident, track)


}