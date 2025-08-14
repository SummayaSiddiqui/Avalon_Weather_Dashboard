import streamlit as st
from utils.fetch_openmeteo import get_historical_rainfall

st.set_page_config(page_title="Avalon Peninsula Rainfall Dashboard 🌦️")
st.title("Avalon Peninsula Rainfall Dashboard 🌦️")

st.markdown("""
This dashboard shows historical rainfall trends for the Avalon Peninsula.
Low rainfall may contribute to unusual wildfires in the region.
""")

# Fetch 2025 rainfall
rainfall_2025 = get_historical_rainfall(start_date="2025-07-01", end_date="2025-08-14")

# Plot rainfall chart
st.subheader("Rainfall Trend (July 1 – Aug 14, 2025)")
st.line_chart(rainfall_2025.set_index('time')['rainfall_mm'])