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
adf=pd.read_csv('spotted-animals.csv')
df['latitude']=df['location'].apply(lambda r: float(r.split(',')[0]))
df['longitude']=df['location'].apply(lambda r: float(r.split(',')[1]))
df['date_time']=pd.to_datetime(df['date_time'])
df=df.drop('location', axis=1)
adf=adf.rename(columns={"name":"animal_name"})
adf=adf[['animal_name','species','capture_points']]
fdf=pd.merge(df,adf,on='animal_name',how='left')
fdf['rarity']=fdf['capture_points'].apply(lambda x:"Common" if x < 20 else "Rare" if x < 40 else "Exceptional")

#st.write(fdf)
#h: 328.32 x 420
# Chrome, popups not allowed

m = folium.Map(location=[54.546687,-3.881687],
               zoom_start=3, control_scale=True)


for i,row in fdf.iterrows():
    lines = ["Spottings:", f"Animal: {str(row['animal_name'])}",f"Rarity: {row['rarity']}",f"Count: {str(row['animal_count'])}", f"When: {row['date_time']}" ,f"Username: {str(row['username'])}",f"<br><img src='{str(row['image_url'])}' style='max-height:50px;'>" ]
    html_content = "<br>".join(lines)
    iframe = folium.IFrame(html=html_content)
    popup = folium.Popup(iframe, min_width=300, max_width=300)
    if row['rarity'] == 'Common':
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            popup=popup, 
            icon=folium.Icon(color='green',icon='glyphicon glyphicon-pushpin'),
            c=row['animal_name']
        ).add_to(m)
    elif row['rarity'] == 'Rare':
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            popup=popup,
            icon=folium.Icon(color='blue',icon='glyphicon glyphicon-bookmark'),
            c=row['animal_name']
        ).add_to(m)
        folium.Circle(
            location=[row['latitude'],row['longitude']],
            radius=250,
            stroke=False,
            fill=True,
            fill_opacity=0.6,
            opacity=1
        ).add_to(m)

    else:
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            popup=popup,
            icon=folium.Icon(color='red',icon='glyphicon glyphicon-star'),
            c=row['animal_name']
        ).add_to(m)        
        folium.Circle(
            location=[row['latitude'],row['longitude']],
            color='red',
            radius=500,
            stroke=False,
            fill=True,
            fill_opacity=0.6,
            opacity=1
        ).add_to(m)
st_data = st_folium(m, width=700,returned_objects=[])