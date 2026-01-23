import datetime
import json
import pandas as pd
import streamlit as st
import requests


username='dev'
name='Sika deer'
num=3
location='///here.here.here'
image_url='test_url'
now = pd.to_datetime(datetime.datetime.now())
now = now.replace(microsecond=0)
now = now.isoformat()
url_post = "https://spotting-api.onrender.com/spottings/new"
post_data = {"date_time":now, "username":username, "animal_name":name, "animal_count":num, "location":location, "image_url":image_url}
post_response = requests.post(url_post,json=post_data)
post_response_json = post_response.json()
st.write(post_response_json)
st.write("Submitted spot!")