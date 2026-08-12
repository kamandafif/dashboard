import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Penentuan Rentang Waktu (30 Hari, interval 15 menit)
rentang_waktu = pd.date_range(start="2026-08-01 00:00", end="2026-08-31 23:45", freq="15min")
total_data = len(rentang_waktu)
np.random.seed(42)  # Menjaga konsistensi data

# 2. Pembentukan Variabel Energi & Operasional
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

# 3. Penggabungan ke Dataframe
df_pabrik = pd.DataFrame({
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

# 4. Ekspor ke File CSV
nama_file = "data_pabrik_simulasi.csv"
df_pabrik.to_csv(nama_file, index=False)
print(f"Data berhasil digenerate dan disimpan dalam file: {nama_file}")