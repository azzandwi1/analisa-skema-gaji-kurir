import os
import json
import re

print("=== VERIFIKASI INTEGRASI DATA WILAYAH & SCRIPT ===")

# 1. Verifikasi file assets/region_data.js
js_path = os.path.join("assets", "region_data.js")
assert os.path.exists(js_path), f"File {js_path} tidak ditemukan!"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Ekstrak objek JSON dari JS
m = re.search(r'const REGION_DATA = (\{.*\});', js_content, re.DOTALL)
assert m, "Objek REGION_DATA tidak ditemukan di assets/region_data.js!"
data = json.loads(m.group(1))

regions = list(data.keys())
print(f"[OK] Total Region: {len(regions)} -> {regions}")
assert "JABODETABEK" in regions, "Region JABODETABEK harus ada!"
assert "BALI" in regions, "Region BALI harus ada!"
assert "JAWA" in regions, "Region JAWA harus ada!"

kab_count = sum(len(data[r]) for r in regions)
print(f"[OK] Total Kabupaten/Kota: {kab_count}")

kec_count = sum(len(data[r][k]) for r in regions for k in data[r])
print(f"[OK] Total Kecamatan: {kec_count}")
assert kec_count >= 7000, f"Jumlah kecamatan kurang ({kec_count})!"

# Contoh cek nilai UMK spesifik
kuta_selatan = data["BALI"]["BADUNG"]["KUTA SELATAN"]
print(f"[OK] Sampel UMK Kuta Selatan: Rp {kuta_selatan:,}")
assert kuta_selatan == 3075627, f"Nilai UMK Kuta Selatan tidak cocok: {kuta_selatan}"

bekasi_barat = data["JABODETABEK"]["BEKASI"]["BEKASI BARAT"]
print(f"[OK] Sampel UMK Bekasi Barat: Rp {bekasi_barat:,}")
assert bekasi_barat == 4952695, f"Nilai UMK Bekasi Barat tidak cocok: {bekasi_barat}"

# 2. Verifikasi index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

assert 'src="assets/region_data.js"' in html, "Script region_data.js belum di-load di index.html!"
assert 'id="selRegion"' in html, "Elemen selRegion tidak ada di index.html!"
assert 'id="selRegency"' in html, "Elemen selRegency tidak ada di index.html!"
assert 'id="selDistrict"' in html, "Elemen selDistrict tidak ada di index.html!"
assert 'id="txtActiveKecamatan"' in html, "Elemen txtActiveKecamatan tidak ada di index.html!"
assert 'initRegionCalculator()' in html, "initRegionCalculator() tidak dipanggil di index.html!"

# 3. Verifikasi Tab Komparasi Payroll (tab-compare)
assert 'id="btn-tab-compare"' in html, "Tombol btn-tab-compare tidak ada di index.html!"
assert 'id="tab-compare"' in html, "Container tab-compare tidak ada di index.html!"
assert 'id="canvasCompareMonthly"' in html, "Canvas canvasCompareMonthly tidak ada di index.html!"
assert 'id="canvasCompareCpK"' in html, "Canvas canvasCompareCpK tidak ada di index.html!"
assert 'id="kpiValNewPayroll"' in html, "Elemen kpiValNewPayroll tidak ada di index.html!"
assert 'id="kpiValSavings"' in html, "Elemen kpiValSavings tidak ada di index.html!"
assert 'id="tblRowNewJun"' in html, "Elemen tblRowNewJun tidak ada di index.html!"
assert 'id="tblRowNewJul"' in html, "Elemen tblRowNewJul tidak ada di index.html!"
assert 'id="tblRowNewAug"' in html, "Elemen tblRowNewAug tidak ada di index.html!"
assert 'id="tblFooterNew"' in html, "Elemen tblFooterNew tidak ada di index.html!"
assert 'setCompareScenario(' in html, "Fungsi setCompareScenario tidak ada di index.html!"
assert 'initCompareCharts()' in html, "Pemanggilan initCompareCharts() tidak ada di index.html!"

print("[OK] Tab Komparasi Payroll 3 Bulan & Elemen Interaktif Terverifikasi Lengkap!")

print("\nSEMUA VERIFIKASI INTEGRASI DATA WILAYAH & TAB KOMPARASI BERHASIL DENGAN SEMPURNA!")

