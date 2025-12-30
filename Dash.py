import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import requests
import re
from urllib.parse import urlparse

def extract_entry_id(team_link_or_id: str) -> int:
    if re.match(r'^https?://', team_link_or_id):
        path = urlparse(team_link_or_id).path
        m = re.search(r'/entry/(\d+)', path)
        if not m:
            raise ValueError("Cannot find entry ID in URL")
        return int(m.group(1))
    if re.match(r'^\d+$', team_link_or_id.strip()):
        return int(team_link_or_id.strip())
    raise ValueError("Invalid team id or link")

def get_team_name(entry_id: int):
    url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/"
    data = requests.get(url).json()
    name = data.get("player_first_name") +" "+ data.get("player_last_name")
    return name

def get_gw_points(entry_id: int, gw_max=14):
    url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/history/"
    history = requests.get(url).json()
    gw_map = {i["event"]: i["points"] for i in history["current"]}
    return [gw_map.get(gw, None) for gw in range(1, gw_max+1)]
def latest_gw():

    url="https://fantasy.premierleague.com/api/entry/4146443/"
    latest_gw=requests.get(url).json()
    return int(latest_gw['current_event'])
df1=pd.DataFrame()
team_links = ["https://fantasy.premierleague.com/entry/4146443",
              "https://fantasy.premierleague.com/entry/7460437",
              "https://fantasy.premierleague.com/entry/275918",
              "https://fantasy.premierleague.com/entry/1912555",
              "https://fantasy.premierleague.com/entry/4975715"]


def dataintialize():
    df=pd.DataFrame()
    x=latest_gw()
    for team_link in team_links:
        entry_id = extract_entry_id(team_link)
        team_name = get_team_name(entry_id)
        points_list = get_gw_points(entry_id,x)
        df1 = pd.DataFrame({team_name: points_list})
        df=pd.concat([df,df1],axis=1)
    return x,df

st.title("Welcome to 5awal counter and last 5awal detector")

if st.button("🔄 Refresh"):
    st.rerun()

x, df1 = dataintialize()

fic = {}
for i in range(x):
    team = df1.loc[i].idxmin()
    fic[team] = fic.get(team, 0) + 1

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(fic.keys(), fic.values(), edgecolor="black")

last_5awal = df1.iloc[x-1].idxmin()

ax.set_title(
    f"The most 5awal till gameweek {x} "
)

ax.set_xlabel("Team name")
ax.set_ylabel("Number of times lowest score")
plt.xticks(rotation=45)

st.pyplot(fig)
st.title(f"and the latest 5awal is {last_5awal}")
df2=df1.copy()
df2.index = [f"GW{i+1}" for i in range(len(df2))]
st.dataframe(df2)

