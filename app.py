import streamlit as st
from api import get_air_quality, search_station
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Air Quality Monitor",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:2rem;
}

div[data-testid="stMetric"]{
    background:#1E293B;
    border-radius:15px;
    padding:15px;
    border:1px solid #334155;
}
</style>
""", unsafe_allow_html=True)


def get_status(aqi):
    if aqi <= 50:
        return "🟢 Good", "Udara sangat baik."
    elif aqi <= 100:
        return "🟡 Moderate", "Udara cukup baik."
    elif aqi <= 150:
        return "🟠 Unhealthy for Sensitive Groups", "Kelompok sensitif sebaiknya mengurangi aktivitas luar."
    elif aqi <= 200:
        return "🔴 Unhealthy", "Gunakan masker saat berada di luar."
    elif aqi <= 300:
        return "🟣 Very Unhealthy", "Hindari aktivitas luar."
    else:
        return "⚫ Hazardous", "Tetap di dalam ruangan."


st.title("🌍 Air Quality Monitor")
st.caption("Realtime monitoring kualitas udara menggunakan AQICN API")

with st.sidebar:

    st.header("Pengaturan")

    keyword = st.text_input(
        "🔍 Cari Kota / Negara",
        value="jakarta"
    )

    stations = search_station(keyword)

    if len(stations) == 0:
        st.warning("Lokasi tidak ditemukan.")
        st.stop()

    selected = st.selectbox(
        "📍 Pilih Lokasi Monitoring",
        stations,
        format_func=lambda x: x["name"]
    )

    st.divider()
    st.caption("Powered by AQICN API")

data = get_air_quality(selected["url"])


if data:

    aqi = data["AQI"]

    status, rekom = get_status(aqi)

    st.subheader(status)

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("AQI",data["AQI"])
    col2.metric("PM2.5",data["PM2.5"])
    col3.metric("🌡️ Suhu",f'{data["Suhu"]} °C')
    col4.metric("💧 Humidity",f'{data["Kelembapan"]}%')

    col5,col6 = st.columns(2)

    col5.metric("🌬️ Angin",f'{data["Angin"]} m/s')
    col6.metric("🧭 Tekanan",f'{data["Tekanan"]} hPa')

    st.divider()

    st.subheader("💡 Rekomendasi")

    st.info(rekom)

    st.divider()

    st.subheader("📍 Informasi")

    st.write("**Lokasi :**",data["Kota"])
    st.write("**Polutan Dominan :**",data["Polutan"].upper())
    st.write("**Update :**",data["Update"])

    st.divider()

    st.subheader("🗺️ Lokasi Monitoring")

    map_df = pd.DataFrame({
        "lat":[data["Latitude"]],
        "lon":[data["Longitude"]]
    })

    st.map(map_df)

    st.divider()

    st.subheader("🌫️ Air Quality Index")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={"text":"AQI"},
        gauge={
            "axis":{"range":[0,300]},
            "steps":[
                {"range":[0,50],"color":"green"},
                {"range":[50,100],"color":"yellow"},
                {"range":[100,150],"color":"orange"},
                {"range":[150,200],"color":"red"},
                {"range":[200,300],"color":"purple"},
            ]
        }
    ))

    gauge.update_layout(
        template="plotly_dark",
        height=350
    )

    st.plotly_chart(gauge, width="stretch")

    st.divider()

    kiri, kanan = st.columns(2)

    with kiri:

        st.subheader("Forecast PM2.5")

        pm25 = pd.DataFrame(data["Forecast_PM25"])

        fig = px.line(
            pm25,
            x="day",
            y="avg",
            markers=True
        )

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig, width="stretch")

    with kanan:

        st.subheader("Forecast PM10")

        pm10 = pd.DataFrame(data["Forecast_PM10"])

        fig2 = px.line(
            pm10,
            x="day",
            y="avg",
            markers=True
        )

        fig2.update_layout(template="plotly_dark")

        st.plotly_chart(fig2, width="stretch")

else:

    st.error("Data tidak ditemukan.")