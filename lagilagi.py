import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="DSS Energi & Mobilitas Cerdas",
    page_icon="⚡",
    layout="wide"
)

# 2. Generator Data Simulasi Energi & AGV
@st.cache_data
def generate_data():
    rentang_waktu = pd.date_range(start="2026-08-01 00:00", end="2026-08-31 23:45", freq="15min")
    total_data = len(rentang_waktu)
    np.random.seed(42)

    jam = rentang_waktu.hour
    beban_dasar = np.random.normal(loc=40, scale=5, size=total_data)
    fluktuasi_kerja = np.where((jam >= 8) & (jam <= 17), np.random.normal(loc=35, scale=8, size=total_data), 5)
    daya_mesin_kw = np.clip(beban_dasar + fluktuasi_kerja, a_min=20, a_max=100).round(2)

    faktor_siang = np.maximum(0, np.sin((jam - 6) * np.pi / 12))
    solar_power_kw = np.where((jam >= 6) & (jam <= 18), (faktor_siang * 30 + np.random.normal(0, 2, total_data)), 0)
    solar_power_kw = np.clip(solar_power_kw, a_min=0, a_max=35).round(2)

    daya_bersih_pln = np.maximum(0, daya_mesin_kw - solar_power_kw)
    emisi_co2_kg = (daya_bersih_pln * (15 / 60) * 0.85).round(2)

    agv_01_soc = np.clip(100 - ((rentang_waktu.day * 12 + jam * 3) % 80), 15, 100).round(1)
    agv_02_soc = np.clip(100 - ((rentang_waktu.day * 10 + jam * 4) % 85), 20, 100).round(1)
    agv_03_soc = np.clip(100 - ((rentang_waktu.day * 15 + jam * 2) % 75), 10, 100).round(1)
    status_charging = (agv_01_soc < 25) | ((jam >= 12) & (jam <= 13))

    return pd.DataFrame({
        'Timestamp': rentang_waktu,
        'Daya_Mesin_kW': daya_mesin_kw,
        'Solar_Power_kW': solar_power_kw,
        'Emisi_CO2_kg': emisi_co2_kg,
        'AGV_01_SoC': agv_01_soc,
        'AGV_02_SoC': agv_02_soc,
        'AGV_03_SoC': agv_03_soc,
        'Status_Charging_AGV': status_charging
    })

df = generate_data()

# 3. SIDEBAR PARAMETER OPERASIONAL ENERGI
st.sidebar.subheader("⚙️ Parameter Operasional Energi")
kapasitas_solar = st.sidebar.number_input("Kapasitas Solar Panel (kWp)", value=35)
target_efisiensi = st.sidebar.number_input("Target Reduksi Emisi (%)", value=15)

st.sidebar.info(f"⚡ **Batas Beban Puncak Pabrik:**\n\n**80.0 kW / Jam**")

st.sidebar.subheader("🎯 Threshold & Batas Baterai (%)")
min_soc = st.sidebar.number_input("Batas Minimal Baterai AGV (%)", value=20.0)
max_soc = st.sidebar.number_input("Target Charge Baterai AGV (%)", value=90.0)

st.sidebar.subheader("📁 Sumber Data")
sumber_data = st.sidebar.radio("Pilih Sumber Data:", ["Gunakan Data Dummy (Default)", "Unggah File CSV/Excel"])

# 4. HEADER UTAMA DASHBOARD
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Sistem Pendukung Keputusan Efisiensi Energi & Mobilitas Cerdas</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Optimasi Konsumsi Daya Pabrik, Energi Surya, dan Pengisian Daya AGV | Powered by Streamlit</p>", unsafe_allow_html=True)
st.write("")

# 5. TAB NAVIGASI HORIZONTAL
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Data Telemetri Energi", 
    "📈 Visualisasi Daya & AGV", 
    "🌱 Analisis Karbon & Efisiensi", 
    "💡 Rekomendasi DSS"
])

# 6. KONTEN TAB 1: DATA TELEMETRI
with tab1:
    st.subheader("Tabel Telemetri Konsumsi Daya dan Status Baterai AGV")
    
    st.dataframe(df.head(10), use_container_width=True)
    
    st.write("")
    m1, m2, m3 = st.columns(3)
    
    total_daya = df['Daya_Mesin_kW'].sum() / 4
    total_solar = df['Solar_Power_kW'].sum() / 4
    total_emisi = df['Emisi_CO2_kg'].sum()
    
    m1.metric("Total Konsumsi Daya", f"{total_daya:,.2f} kWh")
    m2.metric("Kontribusi Energi Surya", f"{(total_solar/total_daya)*100:.2f}%")
    m3.metric("Total Emisi CO2 Terhitung", f"{total_emisi:,.2f} kg")

# 7. KONTEN TAB 2: VISUALISASI
with tab2:
    st.subheader("Grafik Profil Beban Listrik vs Pasokan Panel Surya")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Timestamp'][:500], y=df['Daya_Mesin_kW'][:500], name='Beban Mesin (kW)', line=dict(color='firebrick')))
    fig.add_trace(go.Scatter(x=df['Timestamp'][:500], y=df['Solar_Power_kW'][:500], name='Solar Power (kW)', fill='tozeroy', line=dict(color='forestgreen')))
    st.plotly_chart(fig, use_container_width=True)

# 8. KONTEN TAB 3: EMISI
with tab3:
    st.subheader("Proporsi Sumber Energi Pabrik")
    fig_pie = px.pie(names=['Listrik PLN', 'Panel Surya'], values=[total_daya - total_solar, total_solar], hole=0.4, color_discrete_sequence=['#E74C3C', '#2ECC71'])
    st.plotly_chart(fig_pie, use_container_width=True)

# 9. KONTEN TAB 4: REKOMENDASI DSS
with tab4:
    st.subheader("Hasil Analisis Preskriptif & Rekomendasi DSS")
    
    lonjakan = df[(df['Daya_Mesin_kW'] > 80) & (df['Status_Charging_AGV'] == True)]
    if len(lonjakan) > 0:
        st.warning(f"⚠️ **Peringatan Beban Puncak:** Terdeteksi {len(lonjakan)} kali pengisian daya AGV bersamaan saat beban listrik pabrik melebihi 80 kW.")
        st.info("💡 **Saran Otomatis Sistem:** Alihkan jadwal pengisian daya AGV ke rentang jam 12.00 - 14.00 saat produksi Panel Surya mencapai puncaknya.")
    else:
        st.success("✅ **Kondisi Optimal:** Pengisian daya AGV berjalan efisien tanpa memicu beban puncak.")