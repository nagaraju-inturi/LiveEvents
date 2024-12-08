from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import ipaddress
from eventPlanner import eventSchedule

def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

def is_local_ip(ip_address):
    """Check if an IP address is a local (private) address."""

    try:
        ip = ipaddress.ip_address(ip_address)
    except ValueError:
        return False

    return ip.is_private

import streamlit as st
from events import getEvents
from ip2city import get_location_by_ip
from geo import getLatLong
from weather import getTemperature
import json
import datetime
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.title('_:blue[Live Events Search]_ ')
client_ip = get_remote_ip()
# if local or private ip then assign city to Detroit.

if is_local_ip(client_ip):
    location = {"city": "Detroit", 'country': 'United States', 'zipcode': '48243'}
else:
    location = get_location_by_ip(client_ip)

# st.markdown(f"The remote ip is {get_remote_ip()}")
keywords = st.text_input("Keyword to search", "Harry Potter")
city = st.text_input("City", location['city'])
zipcode = st.text_input("Zip Code", "")
# current_time = datetime.datetime.now()
# formatted_time = current_time.strftime("%Y-%m-%d")
evdate = st.date_input("Event date:", datetime.datetime.today(), format="YYYY-MM-DD")
if st.button("Search"):
    latlong = getLatLong(city)
    temperature_df = getTemperature(latlong)
    st.line_chart(temperature_df, x="date", y="temperature")
    schedule = eventSchedule(city, keywords, evdate.strftime("%Y-%m-%d"))
    st.header("Five day plan in " + city + ":", divider=True)
    for line in schedule:
        line = line.replace("\n", "")
        if line.isdigit():
            continue
        st.markdown("- " + line)
    events = getEvents(keywords, city, zipcode, evdate.strftime("%Y-%m-%d"), '0')
    if events and len(events) > 0:
      # st.write(json.dumps(events))
      df = pd.DataFrame(events)
      df_sorted = df.sort_values(by='date')
      # Display DataFrame using st.dataframe()
      st.dataframe(df_sorted, hide_index=True)
      # Display DataFrame using st.table()
      # st.table(df_sorted)  
    else:
      st.write("No data for " + keywords + " on or after " + evdate.strftime("%Y-%m-%d"))
    