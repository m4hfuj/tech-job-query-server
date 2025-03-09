# app.py
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd


cred = credentials.Certificate("/etc/secrets/credentials.json")
firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://job-list-c5296-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


def insert_data_bdjobs(data):
    # db.reference("/jobs").push().set(data)
    url = data['job_url'].split("id")[1][1:]
    db.reference(f"/bdjobs/{url}").set(data)
    print("Successfull!!")


def get_data_bdjobs():
    data = db.reference("/bdjobs").get()
    # return data
    # data = get_data()

    # Convert data into a DataFrame
    if data:
        # Extract keys and values into a DataFrame
        df = pd.DataFrame(data.values())
        # print(df)
        return df
    
    else:
        print("No data found!")

