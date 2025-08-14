import streamlit as st
import plotly.graph_objects as go
from utils.fetch_openmeteo import get_historical_rainfall, get_coordinates


st.set_page_config(page_title="Rainfall Comparison Dashboard 🌦️")
st.title("Rainfall Comparison Dashboard 🌦️")

st.markdown("""
This dashboard compares monthly rainfall trends over two years for any city.  
Low rainfall periods may indicate potential wildfire risk.
""")

# City Input
st.markdown('<label style="font-weight:700; font-size:18px;">City:</label>', unsafe_allow_html=True)
city = st.text_input("", placeholder="Enter city name", label_visibility="collapsed")

if city:
    # Get coordinates
    latitude, longitude, province, country = get_coordinates(city)
    
    if latitude is None or longitude is None:
        st.warning("City not found. Please enter a valid city name.")
    else:
        # Fetch 2023 and 2024 rainfall data
        rainfall_2024 = get_historical_rainfall(
            start_date="2024-01-01", end_date="2024-12-31",
            latitude=latitude, longitude=longitude
        )
        rainfall_2023 = get_historical_rainfall(
            start_date="2023-01-01", end_date="2023-12-31",
            latitude=latitude, longitude=longitude
        )

        # Aggregate by Month
        def monthly_sum(df):
            df['month'] = df['time'].dt.strftime('%b')
            months_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            monthly = df.groupby('month')['rainfall_mm'].sum().reindex(months_order).reset_index()
            return monthly

        monthly_2024 = monthly_sum(rainfall_2024)
        monthly_2023 = monthly_sum(rainfall_2023)

        # Plot Line Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_2024['month'],
            y=monthly_2024['rainfall_mm'],
            mode='lines+markers',
            name='2024',
            line=dict(color='red')
        ))

        fig.add_trace(go.Scatter(
            x=monthly_2023['month'],
            y=monthly_2023['rainfall_mm'],
            mode='lines+markers',
            name='2023',
            line=dict(color='blue')
        ))

        fig.update_layout(
            title=f'Monthly Rainfall Comparison for {city.capitalize()}, {province}, {country}: 2023 vs 2024',
            xaxis_title='Month',
            yaxis_title='Rainfall (mm)',
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Advisory Note
        st.markdown(f"""
            ⚠️ Notice how rainfall in 2024 compares with 2023 for {city.capitalize()}, {province}, {country}.  
        """)

        # Data Source
        st.markdown("---")
        st.markdown("**Data Source:** [Open-Meteo](https://open-meteo.com), [OpenStreetMap](https://www.openstreetmap.org/)")
