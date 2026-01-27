import datetime
import json
import pandas as pd
import streamlit as st
import requests
import tempfile
import base64
import os

css = """
<style>
    div[data-testid="stForm"] {
        background-color: #A5C89E !important;
    }
</style>
"""



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

    with st.form(key="spot_submission", clear_on_submit=True ,):
        
        st.write("Submit spotting")
        username=st.text_input(label='username')
        st.write("Submit spotting")
        name=st.text_input(label='Animal Name')
        num=st.number_input(label='Number')
        location=st.text_input(label='Location')
        image_url=f"data:image;base64,{base64_image}"
        now = pd.to_datetime(datetime.datetime.now())
        now = now.replace(microsecond=0)
        now = now.isoformat()
        submitted = st.form_submit_button("Submit")
        if submitted:
            url_post = "https://spotting-api.onrender.com/spottings/new"
            post_data = {"date_time":now, "username":username, "animal_name":name, "animal_count":int(num), "location":location, "image_url":image_url}
            post_response = requests.post(url_post,json=post_data)
            post_response_json = post_response.json()
            st.write(post_response_json)
            st.write("Submitted spot!")
st.write(css,unsafe_allow_html=True)
