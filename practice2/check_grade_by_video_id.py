import os
import csv
import json
import string
import random
import requests
import sys
import ast
import pandas as pd


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Authorization': '048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D',
            'Content-Type': 'application/json',
        }
        self.host = 'https://content-demo.embibe.com'

    def callAPI(self, url, payload, method):
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def Extract_All_Videos(self):
        
        print("Getting response from API")
        response1 = self.callAPI(
            '/learning_objects?where={%22status%22:%22Published%22,%22type%22:%22Video%22}&embed=true&max_results=12000',
            "{}", 'GET')

        # sheet = wb["Sheet"]
        home_data = []
        for item in response1.json()["_items"]:
            try:
                home_data.append([item["id"],str(item["title"]).upper(),str(item["content"]["grades"]).upper()])
                print(item["title"])
                print("\t",item["content"]["grades"])
            except Exception as e:
                print(e)
        
        df = pd.DataFrame(home_data, columns=['Video_ID',"Video_Title","Grades"])
            

        df.to_csv('all_videos.csv',index=False)


def check_grade_by_video_id(video_id,grade):
    src = Source()
    
    if not os.path.exists("all_videos.csv"):
        print("\t\t\tall_videos.csv not found. creating new one")
        src.Extract_All_Videos()

    df = pd.read_csv("all_videos.csv")

    df = df.loc[df["Video_ID"]==int(video_id)]
    df2 = df.loc[df["Video_ID"]==str(video_id)]

    df = pd.concat([df,df2]).drop_duplicates().reset_index()

    if len(df) == 0:
        return "NA"
    else:
        if len(df[df['Grades'].str.contains(grade)]) > 0:
            return "Yes"
        else:
            return "No"