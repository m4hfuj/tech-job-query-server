from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
import time
import requests
# import sys
import pandas as pd


from data.utils.jobclassifier import JobClassifier
from data.utils.firebase import insert_data_bdjobs


columns = [
    "job_title", "job_domain", "job_url", "company_name", "deadline", "published", 
    "vacancy", "location", "age", "salary", "experience", "education", 
    "skills", "workplace", "employment_status", "gender", "job_location", 
    "benefits", "company_address", "company_website"
]

class BDJobsScrapper:
    """
    A class to scrape job listings from the BDJobs website and store them in a MySQL database.
    
    Attributes:
        pages (list): A list of page numbers to scrape.
        df (DataFrame): A Pandas DataFrame to store scraped data.
        row_id (int): A counter for row IDs in the DataFrame.
        conn: MySQL database connection object.
        cursor: MySQL database cursor object.
        data_insert_query (str): SQL query to insert data into the database.
    """
    def __init__(self):
        """
        Initializes BDJobsScrapper with default values and sets up MySQL connection.
        """
        self.pages = [1]
        # self.driver = webdriver.Chrome()
        # self.df = pd.DataFrame(columns=["job_title", "job_url", "company_name", "deadline", "published", "vacancy", "location", "age", "salary", "experience", "education", "skills", "workplace", "employment_status", "gender", "job_location", "benefits", "company_address", "company_website"])
        self.row_id = 0

        ## MySQL Setup
        # self.table_name = "ITJobsBigTable"
        # self.conn = self.make_mysql_connection('job_query_db')
        # print("Connected to job_query_db...")
        # # self.conn = None
        # try:
        #     self.cursor = self.conn.cursor()
        #     self.create_table_query_job()
        #     self.data_insert_query = f"""
        #         INSERT INTO {self.table_name} (job_title,job_domain, job_url, company_name, deadline, published, vacancy, location, age, salary, experience, education, skills, workplace, employment_status, gender, job_location, benefits, company_address, company_website)
        #         VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #     """
                # VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        # except Exception as e:
        #     print(f'{e}')
        #     exit()

        self.classifier = JobClassifier()
        print("classifier llm connection successful...")

    # Debug

    ## QUERIES
    # def make_mysql_connection(self, db_name):
    #     """
    #     Establishes a connection to the MySQL database.

    #     Returns:
    #         MySQL connection object: Connection to the MySQL database.
    #     """
    #     try:
    #         # conn = sqlite3.connect("sqlite.db")
    #         conn = mysql.connector.connect(
    #             host="localhost",
    #             user="root",
    #             password="",
    #             database=db_name
    #         )
    #         print("Connection Successful")            
    #         return conn
    #     except Exception as e:
    #         print(e)
              
    
    # def create_table_query_job(self):
    #     try:
    #         query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ( "
    #         query += "id INT AUTO_INCREMENT PRIMARY KEY, "
    #         for col in columns:
    #             if col == "job_url":
    #                 query += col + " VARCHAR(255) UNIQUE, "
    #             # elif col == "skills":
    #             #     query += col + " VARCHAR(512), "
    #             else:
    #                 query += col + " VARCHAR(512), "
    #         query = query[:-2]
    #         query += " );"
            
    #         # print(query)
    #         self.cursor.execute(query)
    #         print("Table Access Successful")
    #     except Exception as e:
    #         print(e)

    ## Scrapper Method and INSERT to mysql goes inside
    def scrap_from_page(self, page_no):
        page_url = f"https://jobs.bdjobs.com/jobsearch.asp?txtsearch=&fcat=8&qOT=0&iCat=0&Country=0&qPosted=0&qDeadline=0&Newspaper=0&qJobNature=0&qJobLevel=0&qExp=0&qAge=0&hidOrder=%27%27&pg={page_no}&rpp=50&hidJobSearch=JobSearch&MPostings=&ver=&strFlid_fvalue=&strFilterName=&hClickLog=1&hPopUpVal=1"

        driver = webdriver.Chrome()
        driver.get(page_url)
        time.sleep(7)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        jobListings = soup.find_all("div", class_="col-md-12")

        for job in jobListings:
            job_title = job.find("div", class_="job-title-text")
            if job_title:
                job_url = "https://jobs.bdjobs.com/"+ job_title.find("a")["href"]
                
                results = self.scrap_single_job(job_url)
                print("Job no:", self.row_id," - Job title:", job_title.text.strip()," - Job Domain:", results['job_domain'],  " - Job URL: ", job_url)
                self.row_id += 1

                ## Insert into MySQL
                try:
                    # self.cursor.execute(self.data_insert_query, results)
                    # self.conn.commit()
                    # print()
                    # print("Insertion Successfull.")
                    insert_data_bdjobs(results)
                    print("record inserted.")
                    # print()
                except Exception as e:
                    print(f"Exception {e}")
            
            print("-----------------------------------------------------------------------------------------------------")

    def scrap_single_job(self, job_url):
        job_details = requests.get(job_url)
        job_details_soup = BeautifulSoup(job_details.text, 'html.parser')

        ## all variable
        job_title = None
        company_name = None
        deadline = None
        
        vacancy = None
        location = None
        age = None
        salary = None
        experience = None
        published = None
        
        education = None
        skills = None
        
        workplace = None
        employment_status = None
        gender = None
        job_location = None
        benefits = None
        
        company_address = None
        company_website = None

        job_title = job_details_soup.find("h2", class_="jtitle").text.strip()
        company_name = job_details_soup.find("h2", class_="cname").text.strip()
        deadline = job_details_soup.find("span", class_="headcont").text.strip().split(":")[-1].strip()
        # Summary: vacancy, age, location, salary, experience, publish
        temp = {"vacancy":None,"location":None,"age":None,"salary":None,"experience":None,"published":None}
        summary_soup = job_details_soup.find("ul", class_="summery__items")
        summary_items = summary_soup.find_all("li")
        for i in summary_items:
            i = i.text.strip().split(":")
            field = i[0].strip().lower()
            value = i[1].strip()
            temp[field] = value
        vacancy = temp["vacancy"]
        location = temp["location"]
        age = temp["age"]
        salary = temp["salary"]
        experience = temp["experience"]
        published = temp["published"]
        # education
        # education = job_details_soup.find("div", class_="col-sm-12 mb-3").text.strip().split("\n")
        # education = [i for i in education if i.strip()][1:]
        education = []
        try:
            if job_details_soup.find("h5").text.strip() == "Education":
                education = job_details_soup.find("div", class_="col-sm-12 mb-3").find_all("li")
                education = [i.text.strip() for i in education]
        except:
            print('No h5 available')
        education = str(education)
        # skills
        skills = []
        skills_soup = job_details_soup.find_all("button", class_="skill")
        for skill in skills_soup:
            skills.append(skill.text.strip())
        skills = str(skills)
        # Workplace, Employment Status, Job Location, Gender
        temp = {"workplace":None,"employment_status":None,"job_location":None,"gender":None,"benefits":None}
        wejg = job_details_soup.find_all("div", class_="col-sm-12 mb-3")[2:]
        for i in wejg:
            field = i.find("h4")
            if field:
                field = field.text.strip().lower().replace(" ", "_").replace("compensation_&_other_", "")
            value = i.find("p")
            if value:
                value = value.text.strip()
            else:
                value = i.find_all("li")
                value = [i.text.strip() for i in value] 
            temp[field] = value
        workplace = str(temp["workplace"])
        employment_status = str(temp["employment_status"])
        gender = str(temp["gender"])
        job_location = str(temp["job_location"])
        benefits = str(temp["benefits"])
        # company_address, company_website
        temp = {"company_address":None, "company_website":None}
        company_data = job_details_soup.find("div", class_="jobcontent compinfo").find("div", class_="col-sm-12")
        for field, value in zip(company_data.find_all("h5"), company_data.find_all("p")):
            field = "company_"+field.text.strip().lower().replace(":","")
            value = value.text.strip()
            temp[field] = value
        company_address = temp["company_address"]
        company_website = temp["company_website"]

        job_domain = self.classifier.classify(job_title)

        return {
            "job_title": job_title,
            "job_domain": job_domain,
            "job_url": job_url,
            "company_name": company_name,
            "deadline": deadline,
            "published": published,
            "vacancy": vacancy,
            "location": location,
            "age": age,
            "salary": salary,
            "experience": experience,
            "education": education,
            "skills": skills,
            "workplace": workplace,
            "employment_status": employment_status,
            "gender": gender,
            "job_location": job_location,
            "benefits": benefits,
            "company_address": company_address,
            "company_website": company_website
        }


    def scrap(self):
        for page_no in self.pages:
            print("Reading from ", page_no)
            self.scrap_from_page(page_no)


scrapper = BDJobsScrapper()
scrapper.pages = [3,4,5,6,7,8,9,10]
scrapper.scrap()
