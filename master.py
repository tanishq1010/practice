from goal_exam_extractor import goal_exam_grade_extractor
from home_data_extractor import home_data
import pandas as pd

from login_sign_up import *

from miscellaneous import *
# from home_data_continue_learning import home_data



def for_all_exam_goal(goal_exam_grade):
    for ind in goal_exam_grade.index:
        print(goal_exam_grade["Goal"][ind], goal_exam_grade["Exam_name"][ind])
        # signup_data=Signup()
        # login_data=login(signup_data[0],"embibe1234")
        # # child_data=add_user(signup_data[1],login_data[0])
        # embibe_token=login_data[1]
        # child_id=signup_data[1]
        home_data(3721404, goal_exam_grade["Goal"][ind], goal_exam_grade["Grade"][ind],
                  goal_exam_grade["Exam_name"][ind],
                  goal_exam_grade["Goal"][ind],'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM3MjE0MDQsImVtYWlsIjoiMzYxNTU5NF8xNjAyNzgzNzQ2QGVtYmliZS11c2VyLmNvbSJ9.QYI2fB25BRp4c8KNkHIKSOSYLvxARKIDGxJXstk5OMqmlZiQ-E2kult1tDHHKP7eNtNnh4-upBdjmFQeM8CkVw')
        # break


if __name__ == '__main__':

    df_negative_results_all_subjects = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                             'Duration/Concept cpunt', 'Type', 'Id', "Title", 'Section_name',
                                                             'Embium_counts', "Subject", "Subject_tagged",
                                                             "present in subject", "Correctly present in CG","Book Section Present","Learn Section Present","Thumbnail present"])
    df_positive_results_all_subjects = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                             'Duration/Concept cpunt', 'Type', 'Id', "Title", 'Section_name',
                                                             'Embium_counts', "Subject", "Subject_tagged",
                                                             "present in subject", "Correctly present in CG","Book Section Present","Learn Section Present","Thumbnail present"])
    df_negative_results_all_subjects.to_csv("negative_practice_results_all_subjects.csv", index=False)
    df_positive_results_all_subjects.to_csv("positive_practice_results_all_subjects.csv", index=False)
    df_negative_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Duration/Concept cpunt', 'Type', 'Id', "Title", 'Section_name',
                                                'Embium_counts', "Subject", "Subject_tagged", "present only once",
                                                "Correctly present in CG","Book Section Present","Learn Section Present","Thumbnail present"])
    df_positive_results = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",
                                                'Duration/Concept cpunt', 'Type', 'Id', "Title", 'Section_name',
                                                'Embium_counts', "Subject", "Subject_tagged", "present only once",
                                                "Correctly present in CG","Book Section Present","Learn Section Present","Thumbnail present"])
    df_negative_results.to_csv("negative_practice_results.csv", index=False)
    df_positive_results.to_csv("positive_practice_results.csv", index=False)

    goal_exam_grade = goal_exam_grade_extractor()
    for_all_exam_goal(goal_exam_grade)

    # print("\n\n COMPARING")
    comparator("positive_practice_results_all_subjects.csv", "positive_practice_results.csv")
    video_book_validation(pd.read_csv("positive_practice_results_all_subjects.csv"),"positive_practice_results_all_subjects.csv")





    # df = pd.DataFrame(columns=['Child_ID', 'Exam', 'Goal', "Grade",'Type', 'Id', "Title", "Subject", "Subject_tagged"])
    # df.to_csv("continue_learning.csv")

    # df1=pd.read_csv("actual_continue_learning.csv")
    # home_data()
    # df2=pd.read_csv("continue_learning.csv")

    # for ind in df1.index:
    #     list1 = [""] * len(df1)
    #     df1["present in api"] = list1
    #     df_new=df2.loc[df2["Id"]==df1["Id"][ind]]
    #     if len(df_new)==1:
    #         df1["present in api"][ind]="yes"
    #     else:
    #         df1["present in api"][ind] = "no"
    #     df1.to_csv("actual_continue_learning.csv",index=False)
