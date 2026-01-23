import pandas as pd
import streamlit as st

from numpy.random import default_rng as rng
import datetime
import requests
import json
import folium
from streamlit_folium import st_folium, folium_static

req = requests.get('https://spotting-api.onrender.com/spottings')
data = req.json()
df=pd.DataFrame(data)
df['latitude']=df['location'].apply(lambda r: float(r.split(',')[0]))
df['longitude']=df['location'].apply(lambda r: float(r.split(',')[1]))
df=df.drop('location', axis=1)

m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()],
               zoom_start=3, control_scale=True)

for i,row in df.iterrows():
    iframe = folium.IFrame(f"""Spotting:Animal: {str(row["animal_name"])}

""")
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Marker(location=[row['latitude'],row['longitude']],
                  popup = popup, c=row['animal_name']).add_to(m)
    
st_data = folium_static(m, width=700)