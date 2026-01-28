import pandas as pd
import streamlit as st
import numpy as np
import datetime
import requests
import json
import folium
from streamlit_folium import st_folium

from folium.plugins import TagFilterButton
from xyzservices.lib import TileProvider

req = requests.get('https://spotting-api.onrender.com/spottings')
data = req.json()
df=pd.DataFrame(data)

adf=pd.read_csv('spotted-animals.csv')
df['latitude']=df['location'].apply(lambda r: float(r.split(',')[0]))
df['longitude']=df['location'].apply(lambda r: float(r.split(',')[1]))
df['date_time']=pd.to_datetime(df['date_time'])
df=df.drop('location', axis=1)
adf=adf.rename(columns={"name":"animal_name"})
adf=adf[['animal_name','species','capture_points','type']]
fdf=pd.merge(df,adf,on='animal_name',how='left')
fdf['rarity']=fdf['capture_points'].apply(lambda x:"Common" if x < 20 else "Rare" if x < 40 else "Exceptional")


#h: 328.32 x 420
# Chrome, popups not allowed



provider = TileProvider.from_qms("OpenTopoMap")

f = folium.Figure(width=700, height=700)
m = folium.Map(location=[53.755437,3.524313],
               zoom_start=4.5, control_scale=True).add_to(f)


for i,row in fdf.iterrows():
    lines = [f"Animal: {str(row['animal_name'])}",f"Rarity: {row['rarity']}",f"Count: {str(row['animal_count'])}", f"When: {row['date_time']}" ,f"Username: {str(row['username'])}",f"<img src='{str(row['image_url'])}' style='max-height:80px;'>" ]
    html_content = "<br>".join(lines)
    iframe = folium.IFrame(html=html_content)
    popup = folium.Popup(iframe, min_width=275, max_width=275)
    if row['rarity'] == 'Common':
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            tags=[row['type'],row['rarity']],
            popup=popup,
            icon=folium.Icon(color='darkgreen',icon='glyphicon glyphicon-pushpin'),
            c=row['animal_name']

        ).add_to(m)
    elif row['rarity'] == 'Rare':
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            tags=[row['type'],row['rarity']],
            popup=popup,
            icon=folium.Icon(color='darkblue',icon='glyphicon glyphicon-bookmark'),
            c=row['animal_name']
        ).add_to(m)
        folium.Circle(
            location=[row['latitude'],row['longitude']],
            radius=250,
            color='darkblue',
            stroke=False,
            fill=True,
            fill_opacity=0.6,
            opacity=1
        ).add_to(m)

    else:
        folium.Marker(
            location=[row['latitude'],row['longitude']],
            tags=[row['type'],row['rarity']],
            popup=popup,
            icon=folium.Icon(color='darkpurple',icon='glyphicon glyphicon-star'),
            c=row['animal_name']
        ).add_to(m)        
        folium.Circle(
            location=[row['latitude'],row['longitude']],
            color='purple',
            radius=500,
            stroke=False,
            fill=True,
            fill_opacity=0.6,
            opacity=1
        ).add_to(m)

TagFilterButton(list(adf.type.unique())).add_to(m) 
TagFilterButton(list(fdf.rarity.unique())).add_to(m) 

folium.TileLayer(provider).add_to(m)

st_data = st_folium(m,width=700,returned_objects=[])
