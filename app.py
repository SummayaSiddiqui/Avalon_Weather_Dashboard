import streamlit as st
import pandas as pd
from utils.fetch_openmeteo import get_historical_rainfall
import plotly.graph_objects as go

st.set_page_config(page_title="Avalon Peninsula Rainfall Dashboard 🌦️")
st.title("Avalon Peninsula Rainfall Dashboard 🌦️")

st.markdown("""
This dashboard shows historical rainfall trends for the Avalon Peninsula.
Low rainfall may contribute to unusual wildfires in the region.
""")

# Fetch 2024 and 2025 rainfall
rainfall_2025 = get_historical_rainfall(start_date="2025-07-01", end_date="2025-08-14")
rainfall_2024 = get_historical_rainfall(start_date="2024-07-01", end_date="2024-08-14")

# Extract month-day for X-axis
rainfall_2025['day'] = rainfall_2025['time'].dt.strftime('%b-%d')
rainfall_2024['day'] = rainfall_2024['time'].dt.strftime('%b-%d')

# Plot rainfall chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=rainfall_2025['day'],
    y=rainfall_2025['rainfall_mm'],
    mode='lines+markers',
    name='2025',
    line=dict(color='red')
))

fig.add_trace(go.Scatter(
    x=rainfall_2024['day'],
    y=rainfall_2024['rainfall_mm'],
    mode='lines+markers',
    name='2024',
    line=dict(color='blue')
))

fig.update_layout(
    title='Rainfall Trend Comparison: July 1 – Aug 14',
    xaxis_title='Date',
    yaxis_title='Rainfall (mm)',
    hovermode='x unified'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("⚠️ Notice how 2025 rainfall is far below last year's levels, highlighting potential wildfire risks.")
st.markdown("---")
st.markdown("**Data Source:** [Open-Meteo](https://open-meteo.com)")
