import os
import csv
import json
import string
import random
import requests
import sys

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

    def Extract_All_Practice(self,goal,exam):
        
        goal_ids = {"CBSE" : "5ec5867a0c88fe5860961943",  # CBSE
                    "Medical" : "5f17177ee61885046e5db8d0",  # Medical
                    "Engineering" : "5f17102be61885046e5d9780",  # Engineering
                    "Banking" : "5ec586770c88fe586096193e",  # Banking
                    "Insurance" : "5f520569429ee9ee0e8c1b04",
                    "Defence": "5f5206b031562a10f6a592ff",
                    "SSC": "5f5207e158ae126dab8a370e",
                    "Railways" : "5f52048858ae126dab8a36cd",
                    "Teaching" : "5eb7ced0c20bf39d163d763c",
                }
        print("Getting response from API")
        response1 = self.callAPI(
            f'/fiber_app/learning_maps/filters/{goal_ids[goal]}/{goal}/{exam}',
            "{}", 'GET')
        # print(f'/fiber_app/learning_maps/filters/{goal_ids[goal]}/{goal}/{exam}')
        home_data = []
        try:
            for subject in response1.json()["Subject"]:
                response2 = self.callAPI(
                    f'/fiber_app/learning_maps/filters/{goal_ids[goal]}/{goal}/{exam}/{subject["name"]}',
                     "{}", 'GET')
                try:
                    for unit in response2.json()["Unit"]:
                        response3 = self.callAPI(
                            f'/fiber_app/learning_maps/filters/{goal_ids[goal]}/{goal}/{exam}/{subject["name"]}/{unit["name"]}',
                            "{}", 'GET')
                        try:
                            for chapter in response3.json()["Chapter"]:
                                # print(chapter["learnpath_name"])
                                home_data.append([goal,exam,chapter["_id"],chapter["learnpath_name"].upper()])

                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
                
        
        df = pd.DataFrame(home_data, columns=['Goal',"Exam","Id","Learnpath_Name"])
            
        return df

    # def check_prefix_sub_str_in_string(self,sub_str,txt):
    #     split_words = txt.split(" ")

    #     for word in split_words:
    #         if word == sub_str:
    #             return True

    #     return False

    # def check_prefix_sub_str_in_lm(self,sub_str,txt):
    #     split_words = txt.split("--")

    #     for word in split_words:
    #         if sub_str in word:
    #             return True

    #     return False

    # def get_practice_by_sub_string(self,query,df):
    #     # return df[df['Video_Title'].str.contains(sub_str)]

    #     df_new = pd.DataFrame(columns=df.columns.values)
    #     for ind in df.index:
    #         if self.check_prefix_sub_str_in_lm(query,df["Learnpath_Name"][ind]):
    #             df_new=pd.concat([df.loc[df.index == ind],df_new]).drop_duplicates()
    #     # print("\n\n",df_new)
    #     return df_new


def remove_space(string): 
    return string.replace(" ", "") 

def practice_results_from_db(exam,goal,ID):
    src = Source()
    
    if os.path.exists(goal +"_"+ remove_space(str(exam)) + "_cg_practice_data.csv" ):
        print("\tFile: "+  goal +"_" +remove_space(str(exam)) + "_cg_practice_data.csv found. Reading....")
        df = pd.read_csv(goal +"_"+ remove_space(str(exam)) + "_cg_practice_data.csv")
        df=df.loc[df['Id'].str.contains(ID)]
        if len(df) == 0:
            return "NA"

        if len(df[df['Exam'].str.contains(exam)]) > 0:
            return "Yes"
        else:
            return "No"

    else:
        print("\tFile: "+ goal +"_" +remove_space(str(exam)) + "_cg_practice_data.csv not found.")
        df = src.Extract_All_Practice(goal,exam)
        df.to_csv(goal +"_"+ remove_space(str(exam)) + "_cg_practice_data.csv")
        df = pd.read_csv(goal +"_"+ remove_space(str(exam)) + "_cg_practice_data.csv")
        
        df=df.loc[df['Id'].str.contains(ID)]
        if len(df) == 0:
            return "NA"

        if len(df[df['Exam'].str.contains(exam)]) > 0:
            return "Yes"
        else:
            return "No"
        

    # # print(df)
    # df_ans = pd.DataFrame(columns=df.columns.values)
    # # for query in query_set:
    #     # print(query)
    # df_new = src.get_practice_by_sub_string(query_set[0],df)
    # df_ans = pd.concat([df_ans,df_new]).drop_duplicates()

    # return df_ans

# practice_results_from_db("10th CBSE","MATH","CBSE")