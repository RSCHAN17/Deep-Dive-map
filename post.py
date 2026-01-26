import datetime
import json
import pandas as pd
import streamlit as st
import requests
import tempfile
import base64
import os

uploaded_file = st.file_uploader(
    "Upload image", type=["jpg", "png","HEIC"])
if uploaded_file:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    # Path to your image
    image_path = path

    # Getting the Base64 string
    base64_image = encode_image(image_path)

    username='developer'
    name='Harvest mouse'
    num=1
    location='52.515937,-2.842187'
    image_url=f"data:image;base64,{base64_image}"
    now = pd.to_datetime(datetime.datetime.now())
    now = now.replace(microsecond=0)
    now = now.isoformat()
    url_post = "https://spotting-api.onrender.com/spottings/new"
    post_data = {"date_time":now, "username":username, "animal_name":name, "animal_count":num, "location":location, "image_url":image_url}
    post_response = requests.post(url_post,json=post_data)
    post_response_json = post_response.json()
    st.write(post_response_json)
    st.write("Submitted spot!")