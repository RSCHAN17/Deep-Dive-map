import pandas as pd
import streamlit as st
import numpy as np
import random
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
for j,line in fdf.iterrows():
    if line['rarity'] == 'Rare':
        line['latitude'] +=  (2*(random.random()) - 1) * 0.00158
        line['longitude'] += (2*(random.random()) - 1) * 0.00158
    elif line['rarity'] == 'Exceptional':
        line['latitude'] +=  2 * (2*(random.random()) - 1) * 0.00158
        line['longitude'] += 2 * (2*(random.random()) - 1) * 0.00158

m = folium.Map(location=[53.055437,3.524313],
               zoom_start=4.5, control_scale=True)

for i,row in fdf.iterrows():

    
    lines = [f"Animal: {str(row['animal_name'])}",f"Rarity: {row['rarity']}",f"Count: {str(row['animal_count'])}", f"When: {row['date_time']}" ,f"Username: {str(row['username'])}",f"<img src='{str(row['image_url'])}' style='max-height:80px;'>" ]
    clean_date = str(row['date_time'])[:-9]
    html_content = f"""
    <link href="https://fonts.googleapis.com/css2?family=Jockey+One&family=Roboto+Slab:wght@100..900&display=swap"
        rel="stylesheet">
    <div style="
        font-family: 'Roboto Slab', sans-serif;
        width:220px;
        background-color: #A5C89E;
        padding: 10px;
        border-radius: 12px;
        color: #36656B;
    ">

        <div style="
            display: flex;
            align-items: baseline;
            gap:8px;
            margin-bottom:6px;
        ">
            <div style="
                font-family: 'Jockey One', serif;
                font-size: 18px;
            ">
                {row['animal_name']}
            </div>

            <div style="
            font-size: 14px;
        ">
            {row['rarity']}
        </div>
    </div>

    <div style="
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        margin-bottom: 4px;
    ">
        <div>Count: {row['animal_count']}</div>
        <div>{clean_date}</div>
        
    </div>

    <div style="
        font-size:12px;
        margin-bottom: 8px;
    ">
        Spotted by: {row['username']}
    </div>

    <div style="text-align: center;">
        <img src="{row['image_url']}"
            style="
                width:100px;
                border-radius:15px;
                ">
            </div>

        </div>
        """

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



st_data = st_folium(m,width=600,height=800,returned_objects=[])
