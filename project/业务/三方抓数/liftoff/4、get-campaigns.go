package main

import (
	"context"
	"encoding/base64"
	"encoding/json"
	glog "github.com/mao888/mao-glog"
	"gopkg.in/resty.v1"
	"time"
)

type LiftoffCampaignsRes struct {
	TrackerType        string      `json:"tracker_type"`
	MinOsVersion       *string     `json:"min_os_version"`
	Name               string      `json:"name"`
	AppId              string      `json:"app_id"`
	State              string      `json:"state"`
	CampaignType       string      `json:"campaign_type"`
	Id                 string      `json:"id"`
	MaxOsVersion       interface{} `json:"max_os_version"`
	StateLastChangedAt *time.Time  `json:"state_last_changed_at"`
}

func main() {
	ctx := context.Background()
	var (
		apiKey          = "bacfa09c4f"
		apiSecret       = "U1NUhwT2c1s0GRPka9DmZg=="
		basicLiftoffUrl = "https://data.liftoff.io/api/v1/campaigns"
	)
	// 拼接client_id和secret，并转换为字节数组
	data := []byte(apiKey + ":" + apiSecret)
	// 使用base64进行编码
	encoded := base64.StdEncoding.EncodeToString(data)
	authorization := "Basic " + encoded

	resp, err := resty.New().SetRetryCount(3).R().
		SetHeaders(map[string]string{
			"Authorization": authorization,
		}).Get(basicLiftoffUrl)
	if err != nil {
		glog.Errorf(ctx, "Post err:%s", err)
		return
	}
	//glog.Infof(ctx, "resp:%s", string(resp.Body()))

	var res []LiftoffCampaignsRes
	err = json.Unmarshal(resp.Body(), &res)
	if err != nil {
		glog.Errorf(ctx, "Unmarshal err:%s", err)
		return
	}
	glog.Infof(ctx, "res的长度:%d", len(res))

	// Id 和 Name 转成一个map
	campaigns := make(map[string]string)
	for _, v := range res {
		campaigns[v.Id] = v.Name
	}
	glog.Infof(ctx, "campaigns map的长度:%v", len(campaigns))
}
