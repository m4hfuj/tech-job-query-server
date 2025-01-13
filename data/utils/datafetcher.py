import re
import ast
import numpy as np
import pandas as pd
from collections import Counter
# import pickle
import warnings
# import sqlite3
# import mysql.connector

from .firebase import *

warnings.filterwarnings("ignore")



# def get_dataframe():
#     # conn = sqlite3.connect('sqlite.db')
#     conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="job_query_db"
#         )
#     cursor = conn.cursor()
#             # job_title, 
#     cursor.execute("""
#         SELECT
#             job_title,
#             job_domain,
#             STR_TO_DATE(published, '%e %M %Y') AS published, 
#             STR_TO_DATE(deadline, '%e %M %Y') AS deadline,
#             education, 
#             skills 
#         FROM ITJobsBigTable
#         WHERE STR_TO_DATE(deadline, '%e %M %Y') > CURDATE()
#         ORDER BY deadline ASC;
#     """)

#     # WHERE strftime(date_created) between strftime('2013-01-01') and strftime('2013-01-08')
#     results = cursor.fetchall()
#     # print(results)

#     df = pd.DataFrame(results, columns=['job_title','job_domain', 'published', 'deadline', 'education', 'skills'])
#     # df = pd.DataFrame(results, columns=['published', 'deadline', 'education', 'skills'])
#     cursor.close()
#     conn.close()
#     # df.to_csv('data.csv')
#     # df = _get_job_labels(df)
#     return df



def _get_education_data(education):
    edu_lst = []
    for edu in education:
        if isinstance(edu, list):
            for e in edu:
                edu_lst.append(e.strip().lower())
    
    freq = Counter(edu_lst)
    
    edu_dict = {
        'Bachelors': 0,
        'Masters': 0,
        'Diploma': 0,
        'Others': 0
    }
    
    for k in freq:
        key = k
        value = freq[k]
    
        if ("cse" in key or "computer" in key or "master") and ("msc" in key or "m.sc" in key or "m.s.c" in key or "master" in key) and not ("mba" in key):
            edu_dict['Masters'] += value
            
        elif ("cse" in key or "computer" in key or "bachelor") and ("bsc" in key or "b.sc" in key or "b.s.c" in key or "bachelor" in key) and not ("bba" in key or "marketing" in key):
            edu_dict['Bachelors'] += value
    
        elif ("diploma" in key):
            edu_dict['Diploma'] += value
            
        else:
            edu_dict['Others'] += value

    edu = pd.DataFrame(list(edu_dict.items()), columns=['Skill', 'Count'])
    edu['Value'] = (edu["Count"]) / sum(edu["Count"]) * 100

    return edu[["Skill", "Value"]]


class DataFetcher:
    def __init__(self, job_class="All Technical Jobs"):
        self.job_class = job_class

        print("Initial job_class-", job_class)

        # self.conn =  mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="",
        #     database="job_query_db"
        # )

        self.df = self.get_dataframe(self.job_class)

        self.languages = list(set([
            'javascript', 'python', 'java', 'csharp', 'cplusplus', 'c', 'typescript', 'html', 'css', 'php',
            'swift', 'objective-c', 'dart', 'flutter', 'kotlin', 'sql', 'bash',
            'ruby on rails', 'matlab', 'dart', 'python', 'php', 'mysql',
            'flutter', 'kotlin', 'objective-c',
            'rust', 'go', 'scala', 'ruby', 'perl', 'php', 'haskell', 'lua', 'typescript', 'bash', 
            'shell scripting', 'assembly language', 'r', 'cobol', 'dart', 'kotlin', 'swift', 'objective-c', 
            'groovy', 'matlab', 'visual basic', 'fortran', 'lisp', 'clojure', 'scheme', 'powershell', 'elm', 
            'erlang', 'ocaml', 'fsharp', 'coffeescript', 'julia', 'php', 'mysql', 'html', 'css'
        ]))
        
        self.frameworks = list(set([
            'pytorch', 'tensorflow', 'postgresql', 'react native', 'react', 'aspnet', 
            'reactjs', 'angular', 'nodejs', 'expressjs', 'flutter', 'bootstrap', 'nextjs',
            'laravel', 'vuejs', 'net', 'net core', 'aspnet', 'aspnet core', 'aspnet mvc',
            'mern', 'django', 'django web framework', 'flask', 'redux', 'tailwind css',
            'redux framework', 'celery', 'django web framework', 'rxjs',
            'laravel framework', 'django', 'django web framework', 'flask',  'mongodb', 'mongoose',
            'vuejs', 'angular', 'spring', 'django', 'flask', 'rails', 'expressjs', 'laravel', 
            'meteorjs', 'symfony', 'emberjs', 'backbonejs', 'aurelia', 'knockoutjs', 'meteor', 'ruby on rails', 
            'codeigniter',  'aspnet mvc', 'aspnet core', 'play framework', 'laravel', 'cakephp', 'yii', 
            'sailsjs', 'nestjs', 'koajs', 'phoenix', 'spark', 'grails', 'struts', 'dropwizard', 'vertx', 'hapijs', 
            'loopback', 'polka', 'rocket', 'actix', 'flask', 'fastapi', 'django rest framework', 'sinatra', 'padrino',
            'ruby on rails'
        ]))
        
        # if job_class:
        #     self.df = self.df[self.df['job_domain'] == job_class]
        
        self.text = self.get_text()



    def get_dataframe(self, job_class="All Technical Jobs"):
        results = get_data()
        # print(results)

        print("Job class-", job_class)
        # print(results)

        df = results[['job_title','job_domain', 'published', 'deadline', 'education', 'skills']]
        # cursor.close()

        # print(df)

        if job_class == "All Technical Jobs":
            return df
        else:
            return df[df['job_domain'] == job_class]



    def get_text(self):
        skill_string = ""
        for skill_row in self.df['skills']:
            skill_row = ast.literal_eval(skill_row)
            for skill in skill_row:
                skill_string += skill.lower()+" "
        skill_string = skill_string.replace(".", "")
        skill_string = skill_string.replace("(", "")
        skill_string = skill_string.replace(")", "")
        skill_string = skill_string.replace("|", "")
        skill_string = skill_string.replace("/", "")
        skill_string = skill_string.replace(":", "")
        skill_string = skill_string.replace("&", "")
        skill_string = skill_string.replace("mysql", "sql")
        skill_string = skill_string.replace("#", "sharp")
        skill_string = skill_string.replace("+", "plus")
        skill_string = skill_string.replace("reactjs", "react")
        return skill_string


    def get_languages(self):
        language_pattern = r'\b(?:' + ("|").join(self.languages) + r')\b'
        language_count = Counter(re.findall(language_pattern, self.text, flags=re.IGNORECASE))
        # return language_count
        df = self._transform(language_count)
        # print(df)
        return df


    def get_frameworks(self):
        framework_pattern = r'\b(?:' + "react native|ruby on rails|" + ("|").join(self.frameworks) + r')\b'
        framework_count = Counter(re.findall(framework_pattern, self.text, flags=re.IGNORECASE))
        df = self._transform(framework_count)
        # print(df)
        return df


    def get_education(self):
        # self.df["education"]
        education_df = self.df["education"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)

        education_data = _get_education_data(education_df)
        data = {
            'Category': list(education_data["Skill"]),
            'Value': list(education_data["Value"]),
        }
        return data


    def _transform(self, freq):
        df = pd.DataFrame({
            'Category': freq.keys(),
            'Value': freq.values(),
        }).sort_values(by='Value', ascending=False)
        # print(df)

        df['Value'] = (df["Value"]) / sum(df["Value"]) * 100
        df = df.sort_values(by='Value', ascending=False).head(10)

        return df
