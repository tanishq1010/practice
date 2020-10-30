import requests
import pandas as pd
import json
from openpyxl import Workbook, load_workbook
from miscellaneous import *
import random


class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method, token):
        self.headers['embibe-token'] = token
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, child_id, board, grade, exam, goal, embibe_token, subject, home_data, df_negative_results,
             df_positive_results):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade,
            "onlyPractise": "true"
        }
        response1 = self.callAPI(
            f"/fiber_ms/v1/home/{subject}",
            json.dumps(payload),
            'POST', embibe_token)
        for item in response1.json():
            if item["content_section_type"] == "PRACTICEBANNER":
                hero_banner_checker(response1.json(), df_negative_results, df_positive_results,
                                    "negative_practice_results.csv", "positive_practice_results.csv", home_data,
                                    subject)

            if (item["content_section_type"] != "PRACTICEBANNER" and item["content_section_type"] != "SUBJECTS" and
                item[
                    "content_section_type"] != "CONTINUELEARNING" and item[
                    "content_section_type"] != "CONTINUELEARNING") and (
                    item["contentType"] != "Ad_banner" and item["contentType"] != "chapter"):
                section_name = item["section_name"]
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    length = data["length"]
                    currency = int(data["currency"])
                    id = data["id"]
                    a_string = id
                    split_string = a_string.split("/", 1)
                    id = split_string[0]
                    Type = data["type"]
                    subject_tagged = data["subject"]
                    thumb = data["thumb"]
                    # thumbnail=True
                    if thumb == "":
                        thumbnail = False
                    else:
                        thumbnail = True
                    if title == "" or description == "" or length == "" or length == 0 or currency < 0 or id == "" or Type == "":
                        length = minutes_converter(length)
                        df_negative_results.loc[len(df_negative_results)] = home_data + [length, Type, id, title,
                                                                                         section_name, currency,
                                                                                         subject, subject_tagged, "",
                                                                                         "", "", "",thumbnail]

                        df_negative_results.to_csv("negative_practice_results.csv", index=False)
                    else:
                        length = minutes_converter(length)
                        df_positive_results.loc[len(df_positive_results)] = home_data + [length, Type, id, title,
                                                                                         section_name, currency,
                                                                                         subject, subject_tagged, "",
                                                                                         "", "", "",thumbnail]

                        df_positive_results.to_csv("positive_practice_results.csv", index=False)

            if item["contentType"] == "chapter":
                section_name = item["section_name"]
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    # length = datta["duration"]
                    # currency = int(data["embium_coins"])
                    id = data["id"]
                    a_string = id
                    concept_count = data["concept_count"]
                    split_string = a_string.split("/", 1)
                    id = split_string[0]
                    Type = data["type"]
                    subject_tagged = data["subject"]
                    thumb=data["thumb"]
                    # thumbnail=True
                    if thumb=="":
                        thumbnail=False
                    else:
                        thumbnail=True
                    if title == "" or id == "" or Type == "" or description == "" or concept_count == "":
                        df_negative_results.loc[len(df_negative_results)] = home_data + ["", Type, id, title,
                                                                                         section_name, "", subject,
                                                                                         subject_tagged, "", "", "", "",thumbnail]


                        df_negative_results.to_csv("negative_practice_results.csv", index=False)
                    else:
                        df_positive_results.loc[len(df_positive_results)] = home_data + [concept_count, Type, id, title,
                                                                                         section_name, "", subject,
                                                                                         subject_tagged, "", "", "", "",thumbnail]


                        df_positive_results.to_csv("positive_practice_results.csv", index=False)

        # print(pd.read_csv("positive_learn_results.csv"))

        Learn = False
        for item in response1.json():

            if str(item["section_name"]) == str("Practice " + str(subject) + " Chapters From " + str(exam)):
                Learn = True
                break
        Books = False
        for item in response1.json():

            if str(item["section_name"]) == str("Books With Videos & Solutions - " + str(subject)):
                Books = True
                break

        # df_positive_results = pd.read_csv("positive_learn_results.csv")
        if Books == True and Learn == True:
            df_positive_results.loc[len(df_positive_results)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                             "INDIVIDUAL", "", "",
                                                                             subject, "", "", Books,Learn,""]

            df_positive_results.to_csv("positive_practice_results.csv", index=False)
        else:
            df_negative_results.loc[len(df_negative_results)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                             "INDIVIDUAL", "", "",
                                                                             subject, "", "",Books,Learn,""]

            df_negative_results.to_csv("negative_practice_results.csv", index=False)

        df11 = pd.read_csv("positive_practice_results.csv")
        df2 = pd.read_csv("positive_practice_results.csv")

        df1 = df11[df11['Exam'].str.contains(exam)]
        df2 = df1[df1['Exam'].str.contains(exam)]

        for ind in df2.index:
            df_new = df1.loc[df1['Id'] == df2["Id"][ind]]
            if len(df_new) > 0:
                df_new1 = df_new.loc[df_new["Section_name"] == df2["Section_name"][ind]]
                if len(df_new1) == 1:
                    df2["present only once"][ind] = str("yes")
                else:
                    df2["present only once"][ind] = str("no")

        df = pd.concat([df11, df2])

        df = df.dropna(axis=0, subset=['present only once'])
        # print(df)
        df.to_csv('positive_practice_results.csv', index=False)


def subject_data_extractor(child_id, board, grade, exam, goal, embibe_token, subject, home_data, df_negative_results,
                           df_positive_results):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token, subject, home_data, df_negative_results,
             df_positive_results)

# subject_data_extractor("", "", "", "", "",
#                        "yJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag",
#                        "Science")
