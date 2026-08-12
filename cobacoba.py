"""
Dashboard Interaktif Terintegrasi — Manajemen Efisiensi Energi
dan Mobilitas Cerdas pada Lingkungan Industri Berkelanjutan.

Sumber data : data_pabrik_simulasi.csv (data sintetis, Proof of Concept)
Framework   : Streamlit + Plotly
"""

import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# 1. KONFIGURASI HALAMAN & PARAMETER GLOBAL
# =========================================================
st.set_page_config(
    page_title="Dashboard Energi & Mobilitas Cerdas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

DAYA_CHARGING_PER_UNIT_KW = 4.5   # asumsi daya pengisian tiap unit AGV
TARIF_WBP = 1650                  # Rp/kWh, ilustrasi tarif Waktu Beban Puncak
TARIF_LUAR_WBP = 1035             # Rp/kWh, ilustrasi tarif di luar WBP


# =========================================================
# 2. PEMUATAN DATA
# =========================================================
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data_pabrik_simulasi.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Berkas 'data_pabrik_simulasi.csv' tidak ditemukan. "
        "Jalankan generate_dataset.py terlebih dahulu, atau unggah berkas "
        "tersebut ke direktori yang sama dengan app.py."
    )
    st.stop()

# Deteksi otomatis kolom SOC dan status pengisian AGV agar jumlah unit fleksibel
kolom_soc = sorted(c for c in df.columns if re.match(r"AGV_\d+_SoC$", c))
kolom_charging = sorted(c for c in df.columns if re.match(r"AGV_\d+_Charging$", c))
daftar_unit_agv = [re.search(r"AGV_(\d+)_SoC", c).group(1) for c in kolom_soc]
n_agv = len(daftar_unit_agv)

kolom_wajib = {"Timestamp", "Daya_Mesin_kW", "Solar_Power_kW", "Emisi_CO2_kg"}
kolom_hilang = kolom_wajib - set(df.columns)
if kolom_hilang:
    st.error(f"Kolom berikut tidak ditemukan pada dataset: {', '.join(sorted(kolom_hilang))}")
    st.stop()

if "Beban_Total_kW" not in df.columns:
    df["Beban_Total_kW"] = df["Daya_Mesin_kW"] + df.get("Status_Charging_AGV", 0) * DAYA_CHARGING_PER_UNIT_KW

if "WBP_Period" not in df.columns:
    jam = df["Timestamp"].dt.hour + df["Timestamp"].dt.minute / 60
    df["WBP_Period"] = (jam >= 17) & (jam < 22)


def rata_rata_interval_jam(seri_timestamp: pd.Series) -> float:
    """Menduga resolusi data (dalam jam) dari selisih antar-timestamp."""
    if len(seri_timestamp) < 2:
        return 0.25
    delta = seri_timestamp.sort_values().diff().dropna().median()
    return max(delta.total_seconds() / 3600, 1e-6)


DT_JAM = rata_rata_interval_jam(df["Timestamp"])


# =========================================================
# 3. SIDEBAR — NAVIGASI, FILTER, DAN PENGATURAN
# =========================================================
st.sidebar.title("Pusat Kendali Industri")
st.sidebar.markdown("---")

modul = st.sidebar.radio(
    "Pilih modul",
    ["Overview KPI", "Analisis Energi & Emisi", "Fleet AGV / EV",
     "Smart Recommendation Engine", "Simulasi Skenario"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Filter Tanggal")

tanggal_min = df["Timestamp"].dt.date.min()
tanggal_max = df["Timestamp"].dt.date.max()

pilihan_tanggal = st.sidebar.date_input(
    "Rentang tanggal",
    value=(tanggal_min, tanggal_max),
    min_value=tanggal_min,
    max_value=tanggal_max,
)

# date_input mengembalikan tanggal tunggal saat pengguna baru memilih satu titik;
# ditangani di sini agar aplikasi tidak berhenti dengan error.
if isinstance(pilihan_tanggal, (list, tuple)) and len(pilihan_tanggal) == 2:
    tanggal_awal, tanggal_akhir = pilihan_tanggal
else:
    tanggal_awal = tanggal_akhir = pilihan_tanggal if not isinstance(pilihan_tanggal, (list, tuple)) else pilihan_tanggal[0]

df_terfilter = df[
    (df["Timestamp"].dt.date >= tanggal_awal) & (df["Timestamp"].dt.date <= tanggal_akhir)
].copy()

st.sidebar.markdown("---")
with st.sidebar.expander("Pengaturan Lanjutan"):
    kapasitas_kontrak = st.number_input(
        "Kapasitas kontrak daya (kW)", min_value=10, max_value=2000, value=100, step=10,
    )
    ambang_peringatan = st.slider("Ambang peringatan (% kapasitas)", 50, 100, 80) / 100
    ambang_kritis = st.slider("Ambang kritis (% kapasitas)", 50, 100, 90) / 100
    faktor_emisi = st.number_input(
        "Faktor emisi grid (kg CO2e/kWh)", min_value=0.1, max_value=1.5, value=0.85, step=0.01,
    )

st.sidebar.caption(f"Sumber data: simulasi sintetis · {n_agv} unit AGV terdeteksi")

if df_terfilter.empty:
    st.warning("Tidak ada data pada rentang tanggal yang dipilih. Silakan ubah filter.")
    st.stop()

# ---- KPI global, dihitung sekali agar tersedia di seluruh modul ----
total_daya = df_terfilter["Daya_Mesin_kW"].sum() * DT_JAM
total_solar = df_terfilter["Solar_Power_kW"].sum() * DT_JAM
total_beban = df_terfilter["Beban_Total_kW"].sum() * DT_JAM if "Beban_Total_kW" in df_terfilter else total_daya
total_emisi = df_terfilter["Emisi_CO2_kg"].sum()
total_produksi = df_terfilter["Production_Output_Units"].sum() if "Production_Output_Units" in df_terfilter else None
kontribusi_solar_pct = (total_solar / total_daya * 100) if total_daya > 0 else 0.0
daya_pln = max(0.0, total_beban - total_solar)


# =========================================================
# MODUL 1 — OVERVIEW KPI
# =========================================================
if modul == "Overview KPI":
    st.title("⚡ Overview Kinerja Energi & Operasional")
    st.caption(
        f"Periode aktif: {tanggal_awal.strftime('%d %b %Y')} – {tanggal_akhir.strftime('%d %b %Y')} "
        f"({df_terfilter['Timestamp'].dt.date.nunique()} hari)"
    )

    kolom = st.columns(4) if total_produksi is not None else st.columns(3)
    kolom[0].metric("Total Konsumsi Daya", f"{total_daya:,.1f} kWh")
    kolom[1].metric(
        "Produksi Energi Surya", f"{total_solar:,.1f} kWh",
        delta=f"{kontribusi_solar_pct:.1f}% kontribusi",
    )
    kolom[2].metric("Total Emisi CO2", f"{total_emisi:,.1f} kg")
    if total_produksi is not None:
        kolom[3].metric("Output Produksi", f"{total_produksi:,.0f} unit")

    st.markdown("---")
    st.subheader("Tren Konsumsi Daya Mesin vs Pasokan Panel Surya")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_terfilter["Timestamp"], y=df_terfilter["Daya_Mesin_kW"],
        name="Beban Mesin Produksi", line=dict(color="#b91c1c", width=1.4),
    ))
    fig.add_trace(go.Scatter(
        x=df_terfilter["Timestamp"], y=df_terfilter["Solar_Power_kW"],
        name="Pasokan Panel Surya", fill="tozeroy",
        line=dict(color="#15803d", width=1), fillcolor="rgba(21,128,61,0.15)",
    ))
    fig.update_layout(
        xaxis_title="Waktu", yaxis_title="Daya (kW)", hovermode="x unified",
        margin=dict(l=20, r=20, t=30, b=20), height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

    if total_produksi is not None and total_daya > 0:
        intensitas_energi = total_daya / total_produksi if total_produksi > 0 else 0
        st.info(
            f"Intensitas energi produksi pada periode ini tercatat **{intensitas_energi:.3f} kWh per unit output**, "
            f"dengan kontribusi energi surya menekan sebagian konsumsi dari jaringan listrik utama."
        )


# =========================================================
# MODUL 2 — ANALISIS ENERGI & EMISI
# =========================================================
elif modul == "Analisis Energi & Emisi":
    st.title("🌱 Analisis Efisiensi Energi & Karbon")

    kolom_kiri, kolom_kanan = st.columns([2, 1])

    with kolom_kiri:
        st.subheader("Profil Emisi Karbon Harian")
        emisi_harian = (
            df_terfilter.groupby(df_terfilter["Timestamp"].dt.date)["Emisi_CO2_kg"]
            .sum().reset_index()
        )
        emisi_harian.columns = ["Tanggal", "Emisi_CO2_kg"]
        fig_emisi = px.bar(
            emisi_harian, x="Tanggal", y="Emisi_CO2_kg",
            labels={"Emisi_CO2_kg": "Emisi CO2 (kg)"},
            color="Emisi_CO2_kg", color_continuous_scale="Reds",
        )
        fig_emisi.update_layout(margin=dict(t=20, b=20), height=380, coloraxis_showscale=False)
        st.plotly_chart(fig_emisi, use_container_width=True)

    with kolom_kanan:
        st.subheader("Proporsi Sumber Energi")
        fig_pie = px.pie(
            names=["Listrik PLN", "Panel Surya"],
            values=[daya_pln, total_solar],
            hole=0.45,
            color_discrete_sequence=["#dc2626", "#16a34a"],
        )
        fig_pie.update_traces(textinfo="label+percent")
        fig_pie.update_layout(margin=dict(t=20, b=20), height=380, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("Beban Total Fasilitas terhadap Kapasitas Kontrak")
    fig_beban = go.Figure()
    fig_beban.add_trace(go.Scatter(
        x=df_terfilter["Timestamp"], y=df_terfilter["Beban_Total_kW"],
        name="Beban Total Fasilitas", line=dict(color="#1d4ed8", width=1.3),
    ))
    fig_beban.add_hline(
        y=kapasitas_kontrak, line_dash="dash", line_color="crimson",
        annotation_text="Kapasitas kontrak", annotation_position="top left",
    )
    fig_beban.update_layout(
        xaxis_title="Waktu", yaxis_title="Daya (kW)", height=360,
        margin=dict(t=20, b=20), hovermode="x unified",
    )
    st.plotly_chart(fig_beban, use_container_width=True)

    st.info(
        f"Total emisi karbon pada periode terpilih mencapai **{total_emisi:,.1f} kg CO2e** "
        f"(setara {total_emisi/1000:.2f} ton), dengan kontribusi panel surya menekan konsumsi "
        f"jaringan listrik utama sebesar **{kontribusi_solar_pct:.1f}%**."
    )


# =========================================================
# MODUL 3 — FLEET AGV / EV
# =========================================================
elif modul == "Fleet AGV / EV":
    st.title("🤖 Monitoring Armada AGV / EV Industri")

    if n_agv == 0:
        st.warning("Tidak ditemukan kolom data AGV (pola nama kolom: AGV_XX_SoC) pada dataset.")
    else:
        st.subheader("Status Baterai Terkini (SOC)")
        baris_terakhir = df_terfilter.iloc[-1]
        kolom_metrik = st.columns(min(n_agv, 6))

        AMBANG_KRITIS_SOC, AMBANG_RENDAH_SOC = 20, 60

        for i, unit in enumerate(daftar_unit_agv):
            nilai_soc = baris_terakhir[f"AGV_{unit}_SoC"]
            if nilai_soc <= AMBANG_KRITIS_SOC:
                label_delta, warna_delta = "Kritis", "inverse"
            elif nilai_soc < AMBANG_RENDAH_SOC:
                label_delta, warna_delta = "Rendah", "off"
            else:
                label_delta, warna_delta = "Aman", "normal"
            kolom_metrik[i % len(kolom_metrik)].metric(
                f"Baterai AGV-{unit}", f"{nilai_soc:.0f}%", delta=label_delta, delta_color=warna_delta,
            )

        st.caption(f"Data ditampilkan pada titik waktu terakhir: {baris_terakhir['Timestamp']}")

        st.markdown("---")
        st.subheader("Grafik Profil Baterai Armada")

        unit_terpilih = st.multiselect(
            "Pilih unit AGV yang ditampilkan",
            daftar_unit_agv, default=daftar_unit_agv,
            format_func=lambda x: f"AGV-{x}",
        )

        if unit_terpilih:
            fig_bat = go.Figure()
            for unit in unit_terpilih:
                fig_bat.add_trace(go.Scatter(
                    x=df_terfilter["Timestamp"], y=df_terfilter[f"AGV_{unit}_SoC"],
                    name=f"AGV-{unit}", mode="lines",
                ))
            fig_bat.add_hrect(
                y0=0, y1=AMBANG_KRITIS_SOC, fillcolor="rgba(220,38,38,0.08)", line_width=0,
                annotation_text="Zona kritis", annotation_position="bottom left",
            )
            fig_bat.update_layout(
                yaxis_title="Persentase Baterai (%)", yaxis_range=[0, 100],
                hovermode="x unified", height=420, margin=dict(t=20, b=20),
            )
            st.plotly_chart(fig_bat, use_container_width=True)
        else:
            st.warning("Pilih minimal satu unit AGV untuk menampilkan grafik.")

        if "Status_Charging_AGV" in df_terfilter.columns:
            st.markdown("---")
            st.subheader("Jumlah Unit Mengisi Daya Sepanjang Waktu")
            fig_charging = px.line(
                df_terfilter, x="Timestamp", y="Status_Charging_AGV",
                labels={"Status_Charging_AGV": "Jumlah unit mengisi daya"},
            )
            fig_charging.update_traces(line_color="#7c3aed")
            fig_charging.update_layout(margin=dict(t=20, b=20), height=300)
            st.plotly_chart(fig_charging, use_container_width=True)


# =========================================================
# MODUL 4 — SMART RECOMMENDATION ENGINE
# =========================================================
elif modul == "Smart Recommendation Engine":
    st.title("💡 Smart Recommendation Engine")
    st.markdown("Sistem analitik preskriptif untuk optimasi jadwal pengisian AGV dan reduksi biaya beban puncak.")

    df_terfilter["rasio_beban"] = df_terfilter["Beban_Total_kW"] / kapasitas_kontrak
    ada_agv_mengisi = df_terfilter.get("Status_Charging_AGV", 0) > 0

    def klasifikasi(row):
        if row.rasio_beban >= ambang_kritis and row.WBP_Period:
            return "KRITIS"
        if row.rasio_beban >= ambang_peringatan and row.WBP_Period:
            return "PERINGATAN"
        if row.rasio_beban >= ambang_peringatan and not row.WBP_Period:
            return "WASPADA"
        return "NORMAL"

    df_terfilter["status_beban"] = df_terfilter.apply(klasifikasi, axis=1)
    lonjakan_puncak = df_terfilter[
        df_terfilter["status_beban"].isin(["PERINGATAN", "KRITIS"]) & ada_agv_mengisi
    ]

    st.subheader("Rekomendasi Tindakan Otomatis")

    if len(lonjakan_puncak) > 0:
        n_kritis = (lonjakan_puncak["status_beban"] == "KRITIS").sum()
        n_peringatan = (lonjakan_puncak["status_beban"] == "PERINGATAN").sum()

        st.warning(
            f"⚠️ **Deteksi Potensi Biaya Puncak:** Terdeteksi **{len(lonjakan_puncak)} interval** "
            f"pengisian daya AGV bersamaan saat beban fasilitas berada di atas "
            f"{ambang_peringatan*100:.0f}% kapasitas kontrak pada periode WBP "
            f"({n_kritis} interval berstatus kritis, {n_peringatan} peringatan)."
        )

        contoh = lonjakan_puncak.sort_values("Beban_Total_kW", ascending=False).iloc[0]
        st.markdown(
            f"**Contoh kejadian dengan beban tertinggi:** {contoh['Timestamp']} — "
            f"beban total {contoh['Beban_Total_kW']:.1f} kW "
            f"({contoh['rasio_beban']*100:.1f}% kapasitas kontrak), "
            f"{int(contoh.get('Status_Charging_AGV', 0))} unit AGV sedang mengisi daya."
        )

        # --- Estimasi penghematan biaya, dihitung dari data, bukan angka tetap ---
        energi_agv_saat_wbp = (
            df_terfilter.loc[df_terfilter["WBP_Period"], "Status_Charging_AGV"]
            * DAYA_CHARGING_PER_UNIT_KW * DT_JAM
        ).sum()
        biaya_sebelum = energi_agv_saat_wbp * TARIF_WBP
        biaya_sesudah = energi_agv_saat_wbp * TARIF_LUAR_WBP
        penghematan = biaya_sebelum - biaya_sesudah
        penghematan_pct = (penghematan / biaya_sebelum * 100) if biaya_sebelum > 0 else 0

        st.info(
            "**Saran perbaikan otomatis:**\n\n"
            "1. **Jadwalkan ulang pengisian AGV** ke luar periode WBP (17.00–22.00), "
            "memanfaatkan kapasitas jaringan yang tersedia pada jam beban rendah.\n"
            "2. **Prioritaskan unit dengan SOC di atas ambang aman** untuk menunda pengisian "
            "terlebih dahulu, sementara unit dengan SOC kritis tetap diisi segera.\n"
            f"3. **Estimasi penghematan:** mengalihkan seluruh pengisian AGV yang saat ini "
            f"berlangsung pada WBP (tarif Rp {TARIF_WBP:,}/kWh) ke luar WBP "
            f"(tarif Rp {TARIF_LUAR_WBP:,}/kWh) berpotensi menghemat "
            f"**Rp {penghematan:,.0f}** ({penghematan_pct:.1f}%) pada periode data terpilih."
        )

        kolom1, kolom2, kolom3 = st.columns(3)
        kolom1.metric("Energi AGV Terisi saat WBP", f"{energi_agv_saat_wbp:,.1f} kWh")
        kolom2.metric("Biaya Saat Ini", f"Rp {biaya_sebelum:,.0f}")
        kolom3.metric("Potensi Penghematan", f"Rp {penghematan:,.0f}", f"-{penghematan_pct:.1f}%")
    else:
        st.success(
            "✅ **Sistem Optimal:** Tidak terdeteksi jadwal pengisian daya AGV yang "
            "bertumpuk dengan beban puncak fasilitas pada periode WBP."
        )

    st.markdown("---")
    st.markdown("#### Uji Cepat Logika Rekomendasi")
    st.caption("Masukkan parameter untuk melihat keluaran sistem terhadap kondisi tertentu.")

    kolom_a, kolom_b, kolom_c = st.columns(3)
    beban_uji = kolom_a.slider("Beban total (kW)", 0, int(kapasitas_kontrak * 1.3), int(kapasitas_kontrak * 0.9))
    wbp_uji = kolom_b.toggle("Simulasikan periode WBP", value=True)
    agv_mengisi_uji = kolom_c.checkbox("AGV sedang mengisi daya", value=True)

    rasio_uji = beban_uji / kapasitas_kontrak
    if rasio_uji >= ambang_kritis and wbp_uji:
        status_uji = "KRITIS"
    elif rasio_uji >= ambang_peringatan and wbp_uji:
        status_uji = "PERINGATAN"
    elif rasio_uji >= ambang_peringatan:
        status_uji = "WASPADA"
    else:
        status_uji = "NORMAL"

    st.write(f"**Status beban:** {status_uji} ({rasio_uji*100:.1f}% kapasitas kontrak)")
    if status_uji in ("KRITIS", "PERINGATAN") and agv_mengisi_uji:
        st.error("Rekomendasi: tunda pengisian AGV non-kritis, jadwalkan ulang ke luar periode WBP.")
    elif status_uji == "WASPADA":
        st.warning("Rekomendasi: pantau tren beban; belum memerlukan tindakan korektif segera.")
    else:
        st.info("Rekomendasi: tidak ada tindakan diperlukan, kondisi dalam batas aman.")


# =========================================================
# MODUL 5 — SIMULASI SKENARIO
# =========================================================
elif modul == "Simulasi Skenario":
    st.title("🎛️ Simulasi Skenario Efisiensi")
    st.markdown("Uji dampak kebijakan efisiensi energi terhadap penurunan emisi dan konsumsi jaringan listrik.")

    kolom1, kolom2 = st.columns(2)
    with kolom1:
        target_solar = st.slider("Penambahan kapasitas panel surya (%)", 0, 150, 20, 5)
    with kolom2:
        pergeseran_agv = st.slider("Pengalihan pengisian AGV keluar dari WBP (%)", 0, 100, 0, 5)

    solar_simulasi = total_solar * (1 + target_solar / 100)

    if "Status_Charging_AGV" in df_terfilter.columns:
        energi_agv_wbp_asal = (
            df_terfilter.loc[df_terfilter["WBP_Period"], "Status_Charging_AGV"]
            * DAYA_CHARGING_PER_UNIT_KW * DT_JAM
        ).sum()
        energi_dialihkan = energi_agv_wbp_asal * (pergeseran_agv / 100)
    else:
        energi_dialihkan = 0.0

    konsumsi_grid_simulasi = max(0.0, total_beban - solar_simulasi - energi_dialihkan * 0)
    # Pengalihan AGV tidak mengubah total energi, namun memindahkan waktu konsumsi;
    # dampaknya pada emisi berasal dari penambahan kapasitas PV, ditampilkan terpisah.
    konsumsi_neto_simulasi = max(0.0, total_beban - solar_simulasi)
    emisi_simulasi = konsumsi_neto_simulasi * faktor_emisi
    emisi_terpangkas = total_emisi - emisi_simulasi
    emisi_terpangkas_pct = (emisi_terpangkas / total_emisi * 100) if total_emisi > 0 else 0

    kolom3, kolom4 = st.columns(2)
    kolom3.metric("Proyeksi Produksi Energi Surya", f"{solar_simulasi:,.1f} kWh", f"+{target_solar}%")
    kolom4.metric(
        "Estimasi Perubahan Emisi CO2", f"{emisi_simulasi:,.1f} kg",
        f"-{emisi_terpangkas_pct:.1f}%" if emisi_terpangkas >= 0 else f"+{abs(emisi_terpangkas_pct):.1f}%",
    )

    fig_banding = go.Figure(go.Bar(
        x=["Kondisi Awal", "Hasil Simulasi"],
        y=[total_emisi, emisi_simulasi],
        marker_color=["#94a3b8", "#15803d"],
        text=[f"{total_emisi:,.0f} kg", f"{emisi_simulasi:,.0f} kg"],
        textposition="outside",
    ))
    fig_banding.update_layout(yaxis_title="Total Emisi CO2 (kg)", height=380, margin=dict(t=20, b=20))
    st.plotly_chart(fig_banding, use_container_width=True)

    if energi_dialihkan > 0:
        st.caption(
            f"Simulasi turut mengasumsikan {pergeseran_agv}% dari {energi_agv_wbp_asal:,.1f} kWh "
            f"energi pengisian AGV pada WBP ({energi_dialihkan:,.1f} kWh) dijadwalkan ulang ke luar "
            f"periode tersebut — perhitungan dampak biayanya tersedia pada modul Smart Recommendation Engine."
        )

    if emisi_terpangkas > 0:
        st.success(
            f"Dengan menaikkan kapasitas energi surya sebesar **{target_solar}%**, pabrik diperkirakan "
            f"mampu menekan emisi karbon sebesar **{emisi_terpangkas:,.1f} kg CO2** "
            f"({emisi_terpangkas_pct:.1f}%) pada periode data terpilih."
        )
    elif emisi_terpangkas < 0:
        st.warning(
            f"Kombinasi parameter saat ini justru meningkatkan estimasi emisi sebesar "
            f"**{abs(emisi_terpangkas):,.1f} kg CO2**, kemungkinan akibat faktor emisi grid "
            f"yang dinaikkan melebihi kondisi dasar."
        )
    else:
        st.info("Parameter saat ini tidak menghasilkan perubahan signifikan terhadap emisi.")


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.caption(
    "Dashboard ini merupakan Proof of Concept berbasis data simulasi (sintetis) "
    "dan belum divalidasi terhadap kondisi operasional pabrik riil."
)