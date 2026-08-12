import streamlit as st

# Contoh kondisi berdasarkan data real-time/sintetis
beban_listrik_kw = 85.0  # misal beban sedang tinggi
status_charging_agv = True
jam_sekarang = 13

st.subheader("💡 Smart Recommendations (Prescriptive Analytics)")

if beban_listrik_kw > 80.0 and status_charging_agv and (12 <= jam_sekarang <= 15):
    st.warning("""
    **Rekomendasi Optimasi:**
    Terdeteksi lonjakan beban listrik saat pengisian daya AGV di jam puncak. 
    Disarankan untuk **menghentikan sementara charging AGV-01 & AGV-02** hingga pukul 15.30.
    - **Potensi Penghematan:** ~12% biaya energi harian.
    - **Reduksi Emisi:** Memaksimalkan penggunaan solar panel saat terik.
    """)
else:
    st.success("Sistem berjalan optimal. Tidak ada tindakan korektif yang diperlukan saat ini.")