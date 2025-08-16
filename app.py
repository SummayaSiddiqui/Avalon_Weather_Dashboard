import streamlit as st
import plotly.graph_objects as go
from utils.fetch_openmeteo import get_historical_rainfall, get_coordinates
import datetime

st.set_page_config(page_title="Rainfall Comparison Dashboard 🌦️")
st.title("Rainfall Comparison Dashboard 🌦️")

st.markdown("""
This dashboard compares monthly rainfall trends over two years for any city.  
Low rainfall periods may indicate potential wildfire risk.
""")

# --- Date Picker ---
today = datetime.date.today()

start_date = st.date_input(
    "Select Start Date",
    value=datetime.date(today.year - 1, 7, 1),
    max_value=today
)

# Compute end date automatically (1 year after start, max today)
one_year_later = start_date + datetime.timedelta(days=365)
end_date = min(one_year_later, today)

st.date_input(
    "End Date (auto-calculated)",
    value=end_date,
    max_value=today,
    disabled=True
)

st.write(f"Selected range: {start_date} → {end_date}")
# Automatically compute comparison period (previous year)
comp_start = start_date.replace(year=start_date.year - 1)
comp_end = end_date.replace(year=end_date.year - 1)

st.write(f"Comparing with: {comp_start} → {comp_end}")

# --- City Input ---
st.markdown('<label style="font-weight:700; font-size:18px;">City:</label>', unsafe_allow_html=True)
city = st.text_input("", placeholder="Enter city name", label_visibility="collapsed")

if city:
    latitude, longitude, province, country = get_coordinates(city)
    
    if latitude is None or longitude is None:
        st.warning("City not found. Please enter a valid city name.")
    else:
        # Fetch rainfall data for both periods
        rainfall_current = get_historical_rainfall(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            latitude=latitude, longitude=longitude
        )

        rainfall_prev = get_historical_rainfall(
            start_date=comp_start.strftime('%Y-%m-%d'),
            end_date=comp_end.strftime('%Y-%m-%d'),
            latitude=latitude, longitude=longitude
        )

        # --- Show total rainfall ---
        if not rainfall_current.empty and not rainfall_prev.empty:
            total_current = rainfall_current['rainfall_mm'].sum()
            total_prev = rainfall_prev['rainfall_mm'].sum()

            st.write(f"💧 Total Rainfall from {start_date} → {end_date}: **{total_current:.1f} mm**")
            st.write(f"💧 Total Rainfall from {comp_start} → {comp_end}: **{total_prev:.1f} mm**")

        # Aggregate by Month
        def monthly_sum_dynamic(df, start_date, end_date):
            df['month'] = df['time'].dt.strftime('%b')
            df['year'] = df['time'].dt.year
            # Filter only dates in the selected range
            df = df[(df['time'].dt.date >= start_date) & (df['time'].dt.date <= end_date)]
            # Keep months in order based on first month of range
            months_order = df['time'].dt.strftime('%b').unique().tolist()
            monthly = df.groupby('month')['rainfall_mm'].sum().reindex(months_order).reset_index()
            return monthly

        monthly_current = monthly_sum_dynamic(rainfall_current, start_date, end_date)
        monthly_prev = monthly_sum_dynamic(rainfall_prev, comp_start, comp_end)

        # Plot Line Chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=monthly_prev['month'],
            y=monthly_prev['rainfall_mm'],
            mode='lines+markers',
            name=f"{'Previous Year'}",  # Previous year
            line=dict(color='blue')
        ))

        fig.add_trace(go.Scatter(
            x=monthly_current['month'],
            y=monthly_current['rainfall_mm'],
            mode='lines+markers',
            name=f"{'Recent Year'}",  # Recent year
            line=dict(color='red')
        ))

        fig.update_layout(
            title=f'Monthly Rainfall Comparison for {city.capitalize()}, {province}, {country}: {comp_start.year} vs {start_date.year}',
            xaxis_title='Month',
            yaxis_title='Rainfall (mm)',
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Advisory Note
        st.markdown(f"""
            ⚠️ Notice how rainfall in {start_date.year} compares with {comp_start.year} for {city.capitalize()}, {province}, {country}.  
        """)

        # Data Source
        st.markdown("---")
        st.markdown("**Data Source:** [Open-Meteo](https://open-meteo.com), [OpenStreetMap](https://www.openstreetmap.org/)")
