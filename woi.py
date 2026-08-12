import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="DSS Energi & Mobilitas Cerdas",
    page_icon="⚡",
    layout="wide"
)

# 2. Generator Data Simulasi
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

# 3. Sidebar (Persis Seperti Kiri Gambar)
st.sidebar.subheader("⚙️ Parameter Operasional")
jam_shift = st.sidebar.number_input("Jam Kerja Per Shift (Jam)", value=8)
istirahat = st.sidebar.number_input("Waktu Istirahat (Menit)", value=60)

jam_efektif = (jam_shift * 60) - istirahat
st.sidebar.info(f"⏱️ **Jam Kerja Efektif Tersedia:**\n\n**{jam_efektif} menit/shift**")

st.sidebar.subheader("🎯 Threshold & Batas (%)")
batas_underload = st.sidebar.number_input("Batas Maksimal Underload (%)", value=85.0)
batas_overload = st.sidebar.number_input("Batas Minimal Overload (%)", value=110.0)

st.sidebar.subheader("📁 Sumber Data")
sumber_data = st.sidebar.radio("Pilih Sumber Data:", ["Gunakan Data Dummy (Default)", "Unggah File CSV/Excel"])

# 4. Header Utama Dashboard
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>Sistem Pendukung Keputusan Efisiensi Energi & Mobilitas Cerdas</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Metode: Decision Support System (DSS) & Prescriptive Analytics | Powered by Streamlit</p>", unsafe_allow_html=True)
st.write("")

# 5. Navigasi Baris Tab Horizontal (Sesuai Atas Gambar)
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Data Input & Telemetri", 
    "📈 Visualisasi Energi & AGV", 
    "⚖️ Analisis Efisiensi & Emisi", 
    "💡 Rekomendasi DSS"
])

# 6. Konten Tab 1 (Tampilan Tabel & Metrik Utama di Bawahnya)
with tab1:
    st.subheader("Tabel Telemetri Daya dan Status Armada AGV")
    
    # Tampilkan Dataframe/Tabel Interaktif
    st.dataframe(df.head(10), use_container_width=True)
    
    st.write("")
    # Metrik Ringkasan di Bawah Tabel (Sesuai Gambar)
    m1, m2, m3 = st.columns(3)
    
    total_daya = df['Daya_Mesin_kW'].sum() / 4
    total_solar = df['Solar_Power_kW'].sum() / 4
    total_emisi = df['Emisi_CO2_kg'].sum()
    
    m1.metric("Total Konsumsi Daya", f"{total_daya:,.2f} kWh")
    m2.metric("Kontribusi Solar Panel", f"{(total_solar/total_daya)*100:.2f}%")
    m3.metric("Total Emisi CO2 Terhitung", f"{total_emisi:,.2f} kg")

# 7. Konten Tab Lainnya
with tab2:
    st.subheader("Grafik Profil Beban Listrik vs Pasokan Surya")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Timestamp'][:500], y=df['Daya_Mesin_kW'][:500], name='Beban Mesin (kW)', line=dict(color='firebrick')))
    fig.add_trace(go.Scatter(x=df['Timestamp'][:500], y=df['Solar_Power_kW'][:500], name='Solar Power (kW)', fill='tozeroy', line=dict(color='forestgreen')))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Proporsi Emisi Karbon")
    fig_pie = px.pie(names=['Listrik PLN', 'Solar Panel'], values=[total_daya - total_solar, total_solar], hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with tab4:
    st.subheader("Hasil Analisis Preskriptif DSS")
    st.warning("⚠️ Terdeteksi pengisian daya AGV bersamaan dengan jam beban puncak listrik pabrik.")
    st.info("💡 **Saran:** Alihkan jadwal pengisian daya ke jam 12.00 - 14.00 untuk menghemat biaya beban puncak.")