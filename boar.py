Microsoft Windows [Version 10.0.26200.8875]
(c) Microsoft Corporation. All rights reserved.

C:\Users\HP>pip install plotly
Collecting plotly
  Downloading plotly-6.9.0-py3-none-any.whl.metadata (9.0 kB)
Requirement already satisfied: narwhals>=1.15.1 in .\AppData\Local\Programs\Python\Python314\Lib\site-packages (from plotly) (2.21.2)
Requirement already satisfied: packaging in .\AppData\Local\Programs\Python\Python314\Lib\site-packages (from plotly) (26.2)
Downloading plotly-6.9.0-py3-none-any.whl (9.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 9.9/9.9 MB 3.1 MB/s  0:00:03
Installing collected packages: plotly
Successfully installed plotly-6.9.0

[notice] A new release of pip is available: 26.1.1 -> 26.2.1
[notice] To update, run: python.exe -m pip install --upgrade pip

C:\Users\HP>sssssdimport streamlit as st
'sssssdimport' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>import pandas as pd
'import' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>import plotly.express as px
'import' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>import plotly.graph_objects as go
'import' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP># 1. Konfigurasi Halaman Dashboard
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>st.set_page_config(
'st.set_page_config' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    page_title="Dashboard Energi & Mobilitas Cerdas",
'page_title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    page_icon="⚡",
'page_icon' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    layout="wide"
'layout' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>)
C:\Users\HP>
C:\Users\HP># 2. Fungsi Memuat Data
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>@st.cache_data
'st.cache_data' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>def load_data():
'def' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    df = pd.read_csv("data_pabrik_simulasi.csv")
'df' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
'df['Timestamp']' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    return df
'return' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>try:
'try:' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    df = load_data()
'df' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>except FileNotFoundError:
'except' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.error("File 'data_pabrik_simulasi.csv' tidak ditemukan. Jalankan skrip generator data terlebih dahulu.")
'st.error' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.stop()
'st.stop' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP># 3. Sidebar: Navigasi dan Filter
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>st.sidebar.title("Pusat Kendali Industri")
'st.sidebar.title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>st.sidebar.markdown("---")
'st.sidebar.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>modul = st.sidebar.radio(
'modul' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    "Pilih Modul:",
'"Pilih Modul:"' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    ["Overview KPI", "Analisis Energi & Emisi", "Fleet AGV / EV", "Smart Recommendation Engine", "Simulasi Skenario"]
'["Overview KPI"' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>)
C:\Users\HP>
C:\Users\HP>st.sidebar.markdown("---")
'st.sidebar.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>st.sidebar.subheader("Filter Data")
'st.sidebar.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>min_date = df['Timestamp'].dt.date.min()
'min_date' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>max_date = df['Timestamp'].dt.date.max()
'max_date' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>start_date, end_date = st.sidebar.date_input(
'start_date' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    "Rentang Tanggal:",
'"Rentang Tanggal:"' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    value=[min_date, max_date],
'value' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    min_value=min_date,
'min_value' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    max_value=max_date
'max_value' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>)
C:\Users\HP>
C:\Users\HP># Filter Dataframe berdasarkan tanggal pilihan
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>filtered_df = df[(df['Timestamp'].dt.date >= start_date) & (df['Timestamp'].dt.date <= end_date)]
] was unexpected at this time.

C:\Users\HP>
C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># MODUL 1: OVERVIEW KPI
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>if modul == "Overview KPI":
The syntax of the command is incorrect.

C:\Users\HP>    st.title("⚡ Overview Kinerja Energi & Operasional")
'st.title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.markdown("Ringkasan metrik utama operasional pabrik dan jejak karbon.")
'st.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    col1, col2, col3, col4 = st.columns(4)
'col1' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    total_daya = filtered_df['Daya_Mesin_kW'].sum() / 4  # kWh (karena interval 15 menit)
'total_daya' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    total_solar = filtered_df['Solar_Power_kW'].sum() / 4
'total_solar' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    total_emisi = filtered_df['Emisi_CO2_kg'].sum()
'total_emisi' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    total_produksi = filtered_df['Production_Output_Units'].sum()
'total_produksi' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    col1.metric("Total Konsumsi Daya", f"{total_daya:,.1f} kWh")
'col1.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col2.metric("Produksi Energi Surya", f"{total_solar:,.1f} kWh", delta=f"{(total_solar/total_daya)*100:.1f}% Kontribusi")
'col2.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col3.metric("Total Emisi CO2", f"{total_emisi:,.1f} kg")
'col3.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col4.metric("Output Produksi", f"{total_produksi:,} Unit")
'col4.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    st.markdown("---")
'st.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    st.subheader("Tren Konsumsi Daya vs Pasokan Panel Surya")
'st.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig = go.Figure()
'fig' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['Daya_Mesin_kW'], name='Beban Listrik (kW)', line=dict(color='firebrick', width=1.5)))
'fig.add_trace' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['Solar_Power_kW'], name='Energi Surya (kW)', fill='tozeroy', line=dict(color='forestgreen', width=1)))
'fig.add_trace' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig.update_layout(xaxis_title="Waktu", yaxis_title="Daya (kW)", hovermode="x unified", margin=dict(l=20, r=20, t=30, b=20))
'fig.update_layout' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.plotly_chart(fig, use_container_width=True)
'st.plotly_chart' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># MODUL 2: ANALISIS ENERGI & EMISI
'#' is not recognized as an internal or external command,
operable program or batch file.
'EMISI' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>elif modul == "Analisis Energi & Emisi":
'elif' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.title("🌱 Analisis Efisiensi Energi & Karbon")
'st.title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    col1, col2 = st.columns([2, 1])
'col1' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    with col1:
'with' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        st.subheader("Profil Emisi Karbon Harian (kg CO2)")
'st.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        df_emisi_harian = filtered_df.groupby(filtered_df['Timestamp'].dt.date)['Emisi_CO2_kg'].sum().reset_index()
'df_emisi_harian' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        fig_emisi = px.bar(df_emisi_harian, x='Timestamp', y='Emisi_CO2_kg', color='Emisi_CO2_kg', color_continuous_scale='Reds')
'fig_emisi' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        st.plotly_chart(fig_emisi, use_container_width=True)
'st.plotly_chart' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    with col2:
'with' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        st.subheader("Proporsi Sumber Energi")
'st.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        daya_pln = max(0, total_daya - total_solar)
'daya_pln' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        fig_pie = px.pie(
'fig_pie' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>            names=['Listrik PLN', 'Panel Surya'],
'names' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>            values=[daya_pln, total_solar],
'values' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>            hole=0.4,
'hole' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>            color_discrete_sequence=['#E74C3C', '#2ECC71']
'color_discrete_sequence' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        )
C:\Users\HP>        st.plotly_chart(fig_pie, use_container_width=True)
'st.plotly_chart' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># MODUL 3: FLEET AGV / EV
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>elif modul == "Fleet AGV / EV":
'elif' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.title("🤖 Monitoring Armada AGV / EV Industri")
'st.title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    st.subheader("Status Baterai Real-Time Terakhir (SoC %)")
'st.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    last_row = filtered_df.iloc[-1]
'last_row' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    col1, col2, col3 = st.columns(3)
'col1' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col1.metric("Baterai AGV-01", f"{last_row['AGV_01_SoC']}%")
'col1.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col2.metric("Baterai AGV-02", f"{last_row['AGV_02_SoC']}%")
'col2.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col3.metric("Baterai AGV-03", f"{last_row['AGV_03_SoC']}%")
'col3.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    st.markdown("---")
'st.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.subheader("Grafik Profil Baterai Armada")
'st.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig_bat = go.Figure()
'fig_bat' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig_bat.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['AGV_01_SoC'], name='AGV-01'))
'fig_bat.add_trace' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig_bat.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['AGV_02_SoC'], name='AGV-02'))
'fig_bat.add_trace' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig_bat.add_trace(go.Scatter(x=filtered_df['Timestamp'], y=filtered_df['AGV_03_SoC'], name='AGV-03'))
'fig_bat.add_trace' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    fig_bat.update_layout(yaxis_title="Persentase Baterai (%)", hovermode="x unified")
'fig_bat.update_layout' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.plotly_chart(fig_bat, use_container_width=True)
'st.plotly_chart' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># MODUL 4: SMART RECOMMENDATION ENGINE
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>elif modul == "Smart Recommendation Engine":
'elif' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.title("💡 Smart Recommendation Engine")
'st.title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.markdown("Sistem analisis preskriptif untuk optimasi operasional dan pengurangan biaya puncak.")
'st.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    # Deteksi kondisi pemborosan/peringatan
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    lonjakan_puncak = filtered_df[(filtered_df['Daya_Mesin_kW'] > 80) & (filtered_df['Status_Charging_AGV']== True)]
] was unexpected at this time.

C:\Users\HP>
C:\Users\HP>    st.subheader("Rekomendasi Tindakan Otomatis")
'st.subheader' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    if len(lonjakan_puncak) > 0:
> was unexpected at this time.
C:\Users\HP>        st.warning(f"⚠️ **Deteksi Potensi Biaya Puncak:** Terdeteksi {len(lonjakan_puncak)} kali insiden pengisian daya AGV bersamaan saat beban listrik pabrik melebihi batas 80 kW.")
'st.warning' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>        st.info("""
'st.info' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        **Saran Perbaikan Otomatis:**
'**Saran' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        1. **Reschedule Charging:** Alihkan jadwal pengisian daya AGV ke rentang jam 12.00 - 14.00 saat produksi *Solar Power* mencapai puncak.
'1.' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        2. **Manajemen Beban Puncak:** Tunda pengisian baterai AGV-01 jika daya mesin utama sedang melebihi85 kW.
'2.' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        3. **Estimasi Hemat:** Pengalihan ini berpotensi menekan biaya tagihan listrik puncak hingga **12-15% per bulan**.
'3.' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        """)
'""")' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    else:
'else:' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>        st.success("✅ **Sistem Optimal:** Tidak terdeteksi adanya pertabrakan jadwal pengisian daya AGV dengan jam beban puncak pabrik.")
'st.success' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># MODUL 5: SIMULASI SKENARIO
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP># ==========================================
'#' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>elif modul == "Simulasi Skenario":
'elif' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.title("🎛️ Simulasi Skenario Efisiensi")
'st.title' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    st.markdown("Uji dampak kebijakan efisiensi energi terhadap penurunan emisi dan biaya.")
'st.markdown' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    target_solar = st.slider("Target Penambahan Kapasitas Solar Panel (%)", 0, 100, 20)
'target_solar' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    solar_simulasi = total_solar * (1 + (target_solar / 100))
'solar_simulasi' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    emisi_terpangkas = (solar_simulasi - total_solar) * 0.85
'emisi_terpangkas' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    col1, col2 = st.columns(2)
'col1' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col1.metric("Proyeksi Produksi Energi Surya Baru", f"{solar_simulasi:,.1f} kWh")
'col1.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>    col2.metric("Estimasi Tambahan Reduksi CO2", f"{emisi_terpangkas:,.1f} kg CO2", delta=f"-{(emisi_terpangkas/total_emisi)*100:.1f}% Emisi")
'col2.metric' is not recognized as an internal or external command,
operable program or batch file.

C:\Users\HP>
C:\Users\HP>    st.success(f"Dengan menaikkan kapasitas energi surya sebesar **{target_solar}%**, pabrik diperkirakan mampu mengurangi emisi karbon sebesar **{emisi_terpangkas:,.1f} kg CO2** pada rentang waktu yang dipilih.")h
