import streamlit as st
from pymongo import MongoClient
import time

today = time.strftime("%d-%m-%y")


@st.cache_resource
def init_connection():
    username = st.secrets["mongo"]["username"]
    password = st.secrets["mongo"]["password"]
    uri = f"mongodb+srv://{username}:{password}@cluster0.2jzeen1.mongodb.net/?retryWrites=true&w=majority"
    return MongoClient(uri)


@st.cache_data(ttl=150)
def get_data(option_):
    db = client.main
    items_ = db.logs.find({
        "date": {"$eq": today},
        "process_name": {"$nin": ["MemCompression", "dllhost.exe"]},
        "computer": option_
    }).sort('memory', -1)
    return list(items_)


@st.cache_data(ttl=150)
def get_options():
    db = client.main
    options_ = db.logs.distinct("computer", {"date": today})
    return tuple(options_)


client = init_connection()

st.header(f"Today's :blue[{today}] activity", divider='rainbow')

options = get_options()
option = st.selectbox('Choose PC:', options)

button = st.button("Update data")
if button:
    get_data(option)

items = get_data(option)

st.subheader("***Program - Minutes***")

if items:
    for item in items:
        st.write(item['process_name'], "-", item['minutes'])
else:
    st.write("Nothing for today")
