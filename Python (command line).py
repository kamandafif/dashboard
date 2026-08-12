Python 2.7.1 (r271:86832, Nov 27 2010, 18:30:46) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import pandas as pd
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named pandas
>>> import numpy as np
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named numpy
>>> from datetime import datetime, timedelta
>>>
>>> # 1. Penentuan Rentang Waktu (30 Hari, interval 15 menit)
... rentang_waktu = pd.date_range(start="2026-08-01 00:00", end="2026-08-31 23:45", freq="15min")
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'pd' is not defined
>>> total_data = len(rentang_waktu)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'rentang_waktu' is not defined
>>> np.random.seed(42)  # Menjaga konsistensi data
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>>
>>> # 2. Pembentukan Variabel Energi & Operasional
...  jam = rentang_waktu.hour
  File "<stdin>", line 2
    jam = rentang_waktu.hour
    ^
IndentationError: unexpected indent
>>>
>>> # Beban mesin dasar + lonjakan pada jam kerja pabrik (08.00 - 17.00)
... beban_dasar = np.random.normal(loc=40, scale=5, size=total_data)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'np' is not defined
>>> fluktuasi_kerja = np.where((jam >= 8) & (jam <= 17), np.random.normal(loc=35, scale=8, size=total_data), 5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>> daya_mesin_kw = np.clip(beban_dasar + fluktuasi_kerja, a_min=20, a_max=100).round(2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>>
>>> # Produksi energi surya (aktif jam 06.00 - 18.00, puncak jam 12.00)
... faktor_siang = np.maximum(0, np.sin((jam - 6) * np.pi / 12))
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'np' is not defined
>>> solar_power_kw = np.where((jam >= 6) & (jam <= 18), (faktor_siang * 30 + np.random.normal(0, 2, total_data)), 0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>> solar_power_kw = np.clip(solar_power_kw, a_min=0, a_max=35).round(2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>>
>>> # Estimasi emisi CO2 berdasarkan konsumsi bersih daya PLN (0.85 kg CO2/kWh)
... daya_bersih_pln = np.maximum(0, daya_mesin_kw - solar_power_kw)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'np' is not defined
>>> emisi_co2_kg = (daya_bersih_pln * (15 / 60) * 0.85).round(2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'daya_bersih_pln' is not defined
>>>
>>> # Simulasi persentase baterai AGV (SoC %)
... agv_01_soc = np.clip(100 - ((rentang_waktu.day * 12 + jam * 3) % 80), 15, 100).round(1)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'np' is not defined
>>> agv_02_soc = np.clip(100 - ((rentang_waktu.day * 10 + jam * 4) % 85), 20, 100).round(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>> agv_03_soc = np.clip(100 - ((rentang_waktu.day * 15 + jam * 2) % 75), 10, 100).round(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'np' is not defined
>>>
>>> # Status charging AGV (True jika baterai di bawah 25% atau jam istirahat)
... status_charging = (agv_01_soc < 25) | ((jam >= 12) & (jam <= 13))
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'agv_01_soc' is not defined
>>>
>>> # Output produksi harian
... produksi_units = np.where((jam >= 8) & (jam <= 17), np.random.poisson(lam=15, size=total_data), 0)
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'np' is not defined
>>>
>>> # 3. Penggabungan ke Dataframe
... df_pabrik = pd.DataFrame({
...     'Timestamp': rentang_waktu,
...     'Daya_Mesin_kW': daya_mesin_kw,
...     'Solar_Power_kW': solar_power_kw,
...     'Emisi_CO2_kg': emisi_co2_kg,
...     'AGV_01_SoC': agv_01_soc,
...     'AGV_02_SoC': agv_02_soc,
...     'AGV_03_SoC': agv_03_soc,
...     'Status_Charging_AGV': status_charging,
...     'Production_Output_Units': produksi_units
... })
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
NameError: name 'pd' is not defined
>>>
>>> # 4. Ekspor ke File CSV
... nama_file = "data_pabrik_simulasi.csv"
>>> df_pabrik.to_csv(nama_file, index=False)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'df_pabrik' is not defined
>>> print(f"Data berhasil digenerate dan disimpan dalam file: {nama_file}")
  File "<stdin>", line 1
    print(f"Data berhasil digenerate dan disimpan dalam file: {nama_file}")
                                                                         ^
SyntaxError: invalid syntax
>>>
>>>
