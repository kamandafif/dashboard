import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Dashboard Energi & Mobilitas Cerdas",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# 2. GENERATOR DATA SIMULASI TERINTEGRASI
# ==========================================
@st.cache_data
def generate_integrated_data():
    # Penentuan Rentang Waktu (30 Hari, interval 15 menit)
    rentang_waktu = pd.date_range(start="2026-08-01 00:00", end="2026-08-31 23:45", freq="15min")
    total_data = len(rentang_waktu)
    np.random.seed(42)  # Menjaga konsistensi data

    jam = rentang_waktu.hour

    # Beban mesin dasar + lonjakan pada jam kerja pabrik (08.00 - 17.00)
    beban_dasar = np.random.normal(loc=40, scale=5, size=total_data)
    fluktuasi_kerja = np.where((jam >= 8) & (jam <= 17), np.random.normal(loc=35, scale=8, size=total_data), 5)
    daya_mesin_kw = np.clip(beban_dasar + fluktuasi_kerja, a_min=20, a_max=100).round(2)

    # Produksi energi surya (aktif jam 06.00 - 18.00, puncak jam 12.00)
    faktor_siang = np.maximum(0, np.sin((jam - 6) * np.pi / 12))
    solar_power_kw = np.where((jam >= 6) & (jam <= 18), (faktor_siang * 30 + np.random.normal(0, 2, total_data)), 0)
    solar_power_kw = np.clip(solar_power_kw, a_min=0, a_max=35).round(2)

    # Estimasi emisi CO2 berdasarkan konsumsi bersih daya PLN (0.85 kg CO2/kWh)
    daya_bersih_pln = np.maximum(0, daya_mesin_kw - solar_power_kw)
    emisi_co2_kg = (daya_bersih_pln * (15 / 60) * 0.85).round(2)

    # Simulasi persentase baterai AGV (SoC %)
    agv_01_soc = np.clip(100 - ((rentang_waktu.day * 12 + jam * 3) % 80), 15, 100).round(1)
    agv_02_soc = np.clip(100 - ((rentang_waktu.day * 10 + jam * 4) % 85), 20, 100).round(1)
    agv_03_soc = np.clip(100 - ((rentang_waktu.day * 15 + jam * 2) % 75), 10, 100).round(1)

    # Status charging AGV (True jika baterai di bawah 25% atau jam istirahat)
    status_charging = (agv_01_soc < 25) | ((jam >= 12) & (jam <= 13))

    # Output produksi harian
    produksi_units = np.where((jam >= 8) & (jam <= 17), np.random.poisson(lam=15, size=total_data), 0)

    # Penggabungan ke Dataframe
    df = pd.DataFrame({
        'Timestamp': rentang_waktu,
        'Daya_Mesin_kW': daya_mesin_kw,
        'Solar_Power_kW': solar_power_kw,
        'Emisi_CO2_kg': emisi_co2_kg,
        'AGV_01_SoC': agv_01_soc,
        'AGV_02_SoC': agv_02_soc,
        'AGV_03_SoC': agv_03_soc,
        'Status_Charging_AGV': status_charging,
        'Production_Output_Units': produksi_units
    })
    return df

# Memuat Data
df = generate_integrated_data()

# ==========================================
# 3. SIDEBAR NAVIGASI DAN FILTER
# ==========================================
st.sidebar.title("Pusat Kendali Industri")
st.sidebar.markdown("---")

modul = st.sidebar.radio(
    "Pilih Modul Dashboard:",
    ["Overview KPI", "Analisis Energi & Emisi", "Fleet AGV / EV", "Smart Recommendation Engine", "Simulasi Skenario"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Data")

min_date = df['Timestamp'].dt.date.min()
max_date = df['Timestamp'].dt.date.max()

start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[(df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)]

# ==========================================
# 4. MODUL 1: OVERVIEW KPI
# ==========================================
if modul == "Overview KPI":
    st.title("⚡ Overview Kinerja Energi & Operasional")
    st.markdown("Ringkasan metrik utama operasional pabrik dan jejak karbon.")

    col1, col2, col3, col4 = st.columns(4)
    
    total_daya = filtered_df['Daya_Mesin_kW'].sum() / 4  # kWh (karena interval 15 menit)
    total_solar = filtered_df['Solar_Power_kW'].sum() / 4
    total_emisi = filtered_df['Emisi_CO2_kg'].sum()
    total_produksi = filtered_df['Production_Output_Units'].sum()

    col1.metric("Total Konsumsi Daya", f"{total_daya:,.1f} kWh")
    col2.metric("Produksi Energi Surya", f"{total_solar:,.1f} kWh", delta=f"{(total_solar/total_daya)*100:.1f}% Kontribusi")
    col3.metric("Total Emisi CO2", f"{total_emisi:,.1f} kg")
    col4.metric("Output Produksi", f"{total_produksi:,} Unit")

    st.markdown("---")
    
    st.subheader("Tren Konsumsi Daya vs Pasokan Panel Surya")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['Daya_Mesin_kW'], name='Beban Listrik (kW)', line=dict(color='firebrick', width=1.5)))
    fig.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['Solar_Power_kW'], name='Energi Surya (kW)', fill='tozeroy', line=dict(color='forestgreen', width=1)))
    fig.update_layout(xaxis_title="Waktu", yaxis_title="Daya (kW)", hovermode="x unified", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 5. MODUL 2: ANALISIS ENERGI & EMISI
# ==========================================
elif modul == "Analisis Energi & Emisi":
    st.title("🌱 Analisis Efisiensi Energi & Karbon")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Profil Emisi Karbon Harian (kg CO2)")
        df_emisi_harian = filtered_df.groupby(filtered_df['Timestamp'].dt.date)['Emisi_CO2_kg'].sum().reset_index()
        fig_emisi = px.bar(df_emisi_harian, x='Timestamp', y='Emisi_CO2_kg', color='Emisi_CO2_kg', color_continuous_scale='Reds')
        st.plotly_chart(fig_emisi, use_container_width=True)
        
    with col2:
        st.subheader("Proporsi Sumber Energi")
        total_daya = filtered_df['Daya_Mesin_kW'].sum() / 4
        total_solar = filtered_df['Solar_Power_kW'].sum() / 4
        daya_pln = max(0, total_daya - total_solar)
        fig_pie = px.pie(
            names=['Listrik PLN', 'Panel Surya'], 
            values=[daya_pln, total_solar], 
            hole=0.4,
            color_discrete_sequence=['#E74C3C', '#2ECC71']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# 6. MODUL 3: FLEET AGV / EV
# ==========================================
elif modul == "Fleet AGV / EV":
    st.title("🤖 Monitoring Armada AGV / EV Industri")
    
    st.subheader("Status Baterai Real-Time Terakhir (SoC %)")
    last_row = filtered_df.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Baterai AGV-01", f"{last_row['AGV_01_SoC']}%")
    col2.metric("Baterai AGV-02", f"{last_row['AGV_02_SoC']}%")
    col3.metric("Baterai AGV-03", f"{last_row['AGV_03_SoC']}%")
    
    st.markdown("---")
    st.subheader("Grafik Profil Baterai Armada")
    fig_bat = go.Figure()
    fig_bat.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['AGV_01_SoC'], name='AGV-01'))
    fig_bat.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['AGV_02_SoC'], name='AGV-02'))
    fig_bat.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['AGV_03_SoC'], name='AGV-03'))
    fig_bat.update_layout(yaxis_title="Persentase Baterai (%)", hovermode="x unified")
    st.plotly_chart(fig_bat, use_container_width=True)

# ==========================================
# 7. MODUL 4: SMART RECOMMENDATION ENGINE
# ==========================================
elif modul == "Smart Recommendation Engine":
    st.title("💡 Smart Recommendation Engine")
    st.markdown("Sistem analisis preskriptif untuk optimasi operasional dan pengurangan biaya puncak.")
    
    lonjakan_puncak = filtered_df[(filtered_df['Daya_Mesin_kW'] > 80) & (filtered_df['Status_Charging_AGV'] == True)]
    
    st.subheader("Rekomendasi Tindakan Otomatis")
    
    if len(lonjakan_puncak) > 0:
        st.warning(f"⚠️ **Deteksi Potensi Biaya Puncak:** Terdeteksi {len(lonjakan_puncak)} kali insiden pengisian daya AGV bersamaan saat beban listrik pabrik melebihi batas 80 kW.")
        
        st.info("""
        **Saran Perbaikan Otomatis:**
        1. **Reschedule Charging:** Alihkan jadwal pengisian daya AGV ke rentang jam 12.00 - 14.00 saat produksi *Solar Power* mencapai puncak.
        2. **Manajemen Beban Puncak:** Tunda pengisian baterai AGV-01 jika daya mesin utama sedang melebihi 85 kW.
        3. **Estimasi Hemat:** Pengalihan ini berpotensi menekan biaya tagihan listrik puncak hingga **12-15% per bulan**.
        """)
    else:
        st.success("✅ **Sistem Optimal:** Tidak terdeteksi adanya pertabrakan jadwal pengisian daya AGV dengan jam beban puncak pabrik.")

# ==========================================
# 8. MODUL 5: SIMULASI SKENARIO
# ==========================================
elif modul == "Simulasi Skenario":
    st.title("🎛️ Simulasi Skenario Efisiensi")
    st.markdown("Uji dampak kebijakan efisiensi energi terhadap penurunan emisi dan biaya.")
    
    target_solar = st.slider("Target Penambahan Kapasitas Solar Panel (%)", 0, 100, 20)
    
    total_solar = filtered_df['Solar_Power_kW'].sum() / 4
    total_emisi = filtered_df['Emisi_CO2_kg'].sum()
    
    solar_simulasi = total_solar * (1 + (target_solar / 100))
    emisi_terpangkas = (solar_simulasi - total_solar) * 0.85
    
    col1, col2 = st.columns(2)
    col1.metric("Proyeksi Produksi Energi Surya Baru", f"{solar_simulasi:,.1f} kWh")
    col2.metric("Estimasi Tambahan Reduksi CO2", f"{emisi_terpangkas:,.1f} kg CO2", delta=f"-{(emisi_terpangkas/total_emisi)*100:.1f}% Emisi")

    st.success(f"Dengan menaikkan kapasitas energi surya sebesar **{target_solar}%**, pabrik diperkirakan mampu mengurangi emisi karbon sebesar **{emisi_terpangkas:,.1f} kg CO2** pada rentang waktu yang dipilih.")