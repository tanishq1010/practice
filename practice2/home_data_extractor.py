import requests
import pandas as pd
import json
import random
from openpyxl import Workbook, load_workbook
from miscellaneous import *
from subject_data_extractor import subject_data_extractor



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
    def callAPI2(self, url, payload, method, token):
        self.headers['Authorization'] = token
        response = requests.request(method,  url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, child_id, board, grade, exam, goal, embibe_token):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade,
            "fetch_all_content":'true'
        }
        response1 = self.callAPI(
            f"/fiber_ms/v1/home/practise",
            json.dumps(payload),
            'POST', embibe_token)
        home_data={'CBSE':'5ec5867a0c88fe5860961943','Engineering':'5f17102be61885046e5d9780','Banking':'5ec586770c88fe586096193e','Medical':'5f17177ee61885046e5db8d0','Insurance':'5f520569429ee9ee0e8c1b04','Defence':'5f5206b031562a10f6a592ff','SSC':'5f5207e158ae126dab8a370e','Railways':'5f52048858ae126dab8a36cd','Teaching':'5eb7ced0c20bf39d163d763c'}
        response2=self.callAPI2("https://content-demo.embibe.com/fiber_app/learning_maps/filters/"+str(home_data[goal])+"/"+str(goal)+"/"+str(exam),'{}','GET','048f38be-1b07-4b21-8f24-eac727dce217:gSEkC3dqDcIv1bbOk78UD9owjn7ins8D')
        LIST=[]
        for item in response2.json()["Subject"]:
            subject=item["name"]
            LIST.append(subject)
        
        LIST.sort()
        # print(LIST)
        LIST2=[]
        for item in response1.json():
             if item["content_section_type"] == "SUBJECTS":
              for data in item["content"]:
                if data["subject"] == "All Subjects":
                    continue
                else:
                    LIST2.append(data['subject'])
        
        LIST2.sort()
        # print(LIST2)
        all_subjects_present=False
        if LIST==LIST2:
            all_subjects_present=True
        print(all_subjects_present)

        

        count=0
        book_count=0
        practice_count=0
        
        for item in response1.json():
         
         practice='EMBIBE_PRACTISE'
         books='BOOKS'
         
         if item['content_section_type']=="SUBJECTS":
            for data in item["content"]:
                count+=1
         if item['content_section_type'].find(practice)==0:
            practice_count+=1
         if item['content_section_type'].find(books)==0:
            book_count+=1
        practice_count=practice_count+1
        # print(count,practice_count,book_count)



        df_positive_results_all_subjects = pd.read_csv("positive_practice_results_all_subjects.csv")
        df_negative_results_all_subjects = pd.read_csv("negative_practice_results_all_subjects.csv")



        df_positive_results = pd.read_csv("positive_practice_results.csv")
        df_negative_results = pd.read_csv("negative_practice_results.csv")

        for item in response1.json():
            home_data = [child_id, exam, goal,grade]
            if item["content_section_type"] == "PRACTICEBANNER":
                hero_banner_checker(response1.json(), df_negative_results_all_subjects,
                                    df_positive_results_all_subjects, "negative_practice_results_all_subjects.csv",
                                    "positive_practice_results_all_subjects.csv", home_data, "All Subjects")


            if item["content_section_type"] == "SUBJECTS":
                for data in item["content"]:
                    if data["subject"] == "All Subjects":
                        continue
                    else:
                       try:
                           subject_data_extractor(child_id, board, grade, exam, goal, embibe_token, data["subject"],
                                               home_data, df_negative_results, df_positive_results)
                       except Exception as e:
                           print(e)


            if (item["content_section_type"] != "PRACTICEBANNER" and item["content_section_type"] != "CONTINUELEARNING" and item["content_section_type"] != "SUBJECTS" and item[
                "content_section_type"] != "CONTINUELEARNING") and (
                    item["contentType"] != "Ad_banner" and item["contentType"] != "chapter" and item["section_name"] != "Books With Videos & Solutions" and item["content_section_type"]!="EMBIBEPRACTICE"):
                section_name = item["section_name"]
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    length = data["length"]
                    currency = int(data["currency"])
                    id = data["id"]
                    a_string = id
                    split_string = a_string.split("/", 1)
                    id= split_string[0]
                    Type = data["type"]
                    subject_tagged = data["subject"]
                    thumb = data["thumb"]
                    # thumbnail=True
                    if thumb == "":
                        thumbnail = False
                    else:
                        thumbnail = True
                    if title == "" or description == "" or length == "" or length == 0 or currency < 0 or id == "" or Type == "":
                        length=minutes_converter(length)
                        df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + [length, Type, id, title,section_name,currency,"All Subjects", subject_tagged,"","","","",thumbnail]
                        df_negative_results_all_subjects.to_csv("negative_practice_results_all_subjects.csv", index=False)
                    else:
                        length=minutes_converter(length)
                        df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + [length, Type, id, title,section_name,currency,"All Subjects", subject_tagged,"","","","",thumbnail]
                        df_positive_results_all_subjects.to_csv("positive_practice_results_all_subjects.csv", index=False)

            if (item["contentType"] == "chapter")and item["content_section_type"]!="EMBIBEPRACTICE":
                section_name = item["section_name"]
                for data in item["content"]:
                    title = data["title"]
                    description = data["description"]
                    # length = datta["duration"]
                    # currency = int(data["embium_coins"])
                    id = data["id"]
                    a_string = id
                    split_string = a_string.split("/", 1)
                    id= split_string[0]
                    concept_count=data["concept_count"]
                    Type = data["type"]
                    subject_tagged = data["subject"]
                    thumb = data["thumb"]
                    # thumbnail=True
                    if thumb == "":
                        thumbnail = False
                    else:
                        thumbnail = True
                    if title == "" or id == "" or Type == ""or description=="" or concept_count<0:
                        df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", Type, id, title,section_name,"","All Subjects", subject_tagged,"","","","",thumbnail]
                        df_negative_results_all_subjects.to_csv("negative_practice_results_all_subjects.csv", index=False)
                    else:
                        df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + [concept_count, Type, id, title,section_name,"","All Subjects", subject_tagged,"","","","",thumbnail]
                        df_positive_results_all_subjects.to_csv("positive_practice_results_all_subjects.csv", index=False)

        home_data = [child_id, exam, goal,grade]

        Books = False
        # for item in response1.json():
        if count==book_count:
                Books = True
                # break
        Learn = False
        # for item in response1.json():
            
        if count==practice_count:
                Learn = True
                # break


        # df_positive_results = pd.read_csv("positive_learn_results.csv")
        if Books == True and Learn == True :
            df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All carousals present", "", "",
                                                                                         "All subject", "", "",Books,Learn,""]

            df_positive_results_all_subjects.to_csv("positive_practice_results_all_subjects.csv", index=False)
        else:
            df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All carousals presentL", "", "",
                                                                                         "All subject", "", "",Books,Learn,""]

            df_negative_results_all_subjects.to_csv("negative_practice_results_all_subjects.csv", index=False)

        if all_subjects_present==True:
            df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All subjet Tags present", "", "",
                                                                                         "All subjet Tags present", "yes all subjects are present in UI", "","","",""]
            # df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
            #                                                                              "All subjet Tags present", "", "",
            #                                                                              "All subjet Tags present", "yes all subjects are present in UI", "","", ""]
                                                                                        

            df_positive_results_all_subjects.to_csv("positive_practice_results_all_subjects.csv", index=False)
        else:
            df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", "", random.randint(0, 1000000), "",
                                                                                         "All subjet Tags present", "", "",
                                                                                         "All subjet Tags present", "no all subjects are not present in UI", "","","",""]
                                                                                         

            df_negative_results_all_subjects.to_csv("negative_practice_results_all_subjects.csv", index=False)


def home_data(child_id, board, grade, exam, goal, embibe_token):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token)


# home_data("", "", "", "", "",
#           "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag")
