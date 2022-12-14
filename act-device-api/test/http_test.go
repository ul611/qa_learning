package test

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"github.com/antihax/optional"
	swagger "github.com/ozonmp/act-device-api/test/client"
	route_client "github.com/ozonmp/act-device-api/test/route-client"
	"github.com/stretchr/testify/assert"
	"io"
	"io/ioutil"
	"math/rand"
	"net/http"
	"net/url"
	"strconv"
	"testing"
	"time"
)

type ListOfItemsResponse struct {
	Items []struct {
		ID        string     `json:"id"`
		Platform  string     `json:"platform"`
		UserID    string     `json:"userId"`
		EnteredAt *time.Time `json:"enteredAt"`
	} `json:"items"`
}

type ItemRequest struct {
	Platform string `json:"platform"`
	UserID   string `json:"userId"`
}

func Test_HttpServer_List(t *testing.T) {
	rand.Seed(time.Now().UnixNano())

	t.Run("GET on list return 200", func(t *testing.T) {
		response, err := http.Get("http://127.0.0.1:8080/api/v1/devices?page=1&perPage=1")
		if err != nil {
			panic(err)
		}

		if response.StatusCode != http.StatusOK {
			t.Errorf("Got %v, but want %v", response.StatusCode, http.StatusOK)
		}
	})

	t.Run("GET on list return devices list", func(t *testing.T) {
		countOfItems := 10
		response, err := http.Get(fmt.Sprintf("http://127.0.0.1:8080/api/v1/devices?page=1&perPage=%d", countOfItems))
		if err != nil {
			panic(err)
		}

		data, err := ioutil.ReadAll(response.Body)
		if err != nil {
			panic(err)
		}

		list := new(ListOfItemsResponse)
		err = json.Unmarshal(data, &list)
		if err != nil {
			panic(err)
		}

		if len(list.Items) != countOfItems {
			t.Errorf("Want %d, get %d items", countOfItems, len(list.Items))
		}
	})

	t.Run("GET on list return devices list if zeroed", func(t *testing.T) {
		countOfItems := 0
		response, err := http.Get(fmt.Sprintf("http://127.0.0.1:8080/api/v1/devices?page=1&perPage=%d", countOfItems))
		if err != nil {
			panic(err)
		}

		data, err := ioutil.ReadAll(response.Body)
		if err != nil {
			panic(err)
		}

		list := new(ListOfItemsResponse)
		err = json.Unmarshal(data, &list)
		if err != nil {
			panic(err)
		}

		if len(list.Items) != countOfItems {
			t.Errorf("Want %d, get %d items", countOfItems, len(list.Items))
		}
	})

	t.Run("POST on creating device", func(t *testing.T) {
		data := []byte(`{"platform": "Android", "userId": "123456"}`)
		r := bytes.NewReader(data)
		contentType := "application/json"

		_, err := http.Post("http://127.0.0.1:8080/api/v1/devices", contentType, r)
		if err != nil {
			panic(err)
		}

		payload := ItemRequest{Platform: "Android", UserID: "123456"}
		payloadJSON, _ := json.Marshal(payload)

		_, err = http.Post("http://127.0.0.1:8080/api/v1/devices", contentType, bytes.NewBuffer(payloadJSON))
		if err != nil {
			panic(err)
		}
	})

	t.Run("GET on list w autogenerated client", func(t *testing.T) {
		cfg := swagger.NewConfiguration()
		client := swagger.NewAPIClient(cfg)

		ctx := context.TODO()
		page := optional.NewString("1")
		perPage := optional.NewString("10")
		opts := swagger.ActDeviceApiServiceApiActDeviceApiServiceListDevicesV1Opts{Page: page, PerPage: perPage}
		items, resp, err := client.ActDeviceApiServiceApi.ActDeviceApiServiceListDevicesV1(ctx, &opts)

		if err != nil {
			panic(err)
		}

		if resp.StatusCode != http.StatusOK {
			panic(resp.StatusCode)
		}

		if len(items.Items) > 0 {
			t.Errorf("Got items %d, expected %d", len(items.Items), 10)
		}

	})

	t.Run("Why do we need a client?", func(t *testing.T) {
		// nc -lp 9090
		_, err := http.Get("http://127.0.0.1:9090")
		if err != nil {
			panic(err)
		}
	})

	t.Run("POST with client", func(t *testing.T) {
		// arrange
		payload := ItemRequest{Platform: "Android", UserID: "666"}
		b := new(bytes.Buffer)
		err := json.NewEncoder(b).Encode(payload)
		if err != nil {
			panic(err)
		}

		client := route_client.NewHTTPClient("http://127.0.0.1:8080", 5, 1*time.Second)
		// action
		req, err := http.NewRequest(http.MethodPost, "http://127.0.0.1:8080/api/v1/devices", b)
		if err != nil {
			panic(err)
		}
		res, err := client.Do(req)
		if err != nil {
			panic(err)
		}

		defer func(Body io.ReadCloser) {
			err := Body.Close()
			if err != nil {
				t.Log(err)
			}
		}(res.Body)
		//assert

		if res.StatusCode != http.StatusOK {
			t.Errorf("Got %v, but want %v", res.StatusCode, http.StatusOK)
		}
		data, _ := ioutil.ReadAll(res.Body)
		if len(data) != 0 {
			t.Log(string(data))
		}
	})

	t.Run("Create device via client API", func(t *testing.T) {
		client := route_client.NewHTTPClient("http://127.0.0.1:8080", 5, 1*time.Second)
		device := route_client.CreateDeviceRequest{
			Platform: "Ubuntu",
			UserId:   "701",
		}
		ctx := context.TODO()
		id, _, _ := client.CreateDevice(ctx, device)
		t.Logf("New device is %d", id.DeviceId)
		assert.GreaterOrEqual(t, id.DeviceId, 0)
	})

	t.Run("List devices via client API", func(t *testing.T) {
		client := route_client.NewHTTPClient("http://127.0.0.1:8080", 5, 1*time.Second)
		opts := url.Values{}
		opts.Add("page", "1")
		opts.Add("perPage", "100")
		ctx := context.TODO()
		items, _, _ := client.ListDevices(ctx, opts)
		assert.GreaterOrEqual(t, len(items.Items), 1)
	})

	t.Run("Create device and check description client API", func(t *testing.T) {
		client := route_client.NewHTTPClient("http://127.0.0.1:8080", 5, 1*time.Second)
		platform, userId := "Ubuntu", strconv.Itoa(rand.Int())
		device := route_client.CreateDeviceRequest{
			Platform: platform,
			UserId:   userId,
		}
		ctx := context.TODO()
		id, _, _ := client.CreateDevice(ctx, device)
		t.Logf("New device is %d", id.DeviceId)
		assert.GreaterOrEqual(t, id.DeviceId, 0)

		description, _, _ := client.DescribeDevice(ctx, strconv.Itoa(id.DeviceId))
		assert.Equal(t, description.Value.ID, id.DeviceId)
		assert.Equal(t, description.Value.Platform, platform)
		assert.Equal(t, description.Value.UserID, userId)
	})

}
