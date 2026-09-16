# 📦 Model Simulasi Skema Kompensasi Kurir Last-Mile

> **Kalkulator & Simulator Interaktif Penentuan Upah Kurir Berkelanjutan di Indonesia:** Menyeimbangkan Produktivitas Antaran, Retensi Kurir (*Low Turnover*), dan Efisiensi Biaya (*Unit Economics* Perusahaan).

---

## 🚀 Gambaran Proyek

Proyek ini menyediakan model analitik dan dashboard interaktif untuk membandingkan 4 skema pengupahan kurir logistik (*last-mile delivery*):
1. **Skema Hibrida Berjenjang (*Hybrid Tiered*) [Pilihan Rekomendasi]** — Gaji Pokok Acuan + Insentif berjenjang jika tembus kuota dasar + Pengali Kualitas SLA (*First-Attempt Delivery Rate* / FADR).
2. **Skema Komisi Murni (*Pure Piece-Rate*)** — Sistem borongan tanpa upah dasar (rawan *turnover* tinggi saat musim sepi).
3. **Skema Gaji Tetap (*Fixed Flat Salary*)** — Upah tetap bulanan tanpa insentif volume (kurang memicu produktivitas saat beban padat, membebani perusahaan saat sepi).
4. **Skema Target Kuota Minimal (*Quota + Cliff Bonus*)** — Gaji pokok + bonus sekaligus jika melampaui ambang batas tertentu (rawan *slacking* & manipulasi status di sore hari).

Dashboard ini dirancang khusus dengan konteks ketenagakerjaan di Indonesia (PP No. 51/2023) dan didukung literatur ilmiah operasional (*Management Science*, *M&SOM*, *Quarterly Journal of Economics*).

### 🌟 Fitur Baru: Auto-Calculator UMK & Logistics Difficulty Index (LDI)
* **Database UMK Kabupaten/Kota:** Pilihan daerah terintegrasi dari DKI Jakarta, Jawa Barat (Kota Bekasi, Karawang, Bandung, dll.), Jawa Tengah, Jawa Timur, Banten, Sumatera, Bali, Kalimantan, Sulawesi, hingga Papua.
* **Faktor Kesulitan Lapangan (Multi-Index):**
  1. *Topografi Medan* (Datar: 1.00x, Berbukit: 1.10x, Pegunungan/Ekstrem: 1.25x)
  2. *Kerapatan Alamat & Jalan* (Rapi: 1.00x, Gang Sempit/Padat: 1.08x, Pedesaan/Jalan Rusak: 1.20x)
  3. *Kemacetan Lalu Lintas* (Lancar: 1.00x, Sedang: 1.05x, Macet Kronis: 1.15x)
* **Kalkulasi & Sinkronisasi Otomatis:**
  * Rekomendasi Gaji Pokok: $W_{bln} = UMK \times LDI$
  * Rekomendasi Kuota Dasar: $Q_{base} = \text{round}(50 / LDI)$
  * Sekali klik untuk langsung diterapkan ke simulator dan tabel laba rugi.

---

## 📂 Struktur File Repository

```text
├── index.html                   # Dashboard simulator interaktif (Single-file HTML + Tailwind CSS + Vanilla JS)
├── assets/
│   └── grafik_simulasi_kompensasi.png   # Grafik 4-panel visualisasi perbandingan skema
├── scripts/
│   ├── simulasi_kompensasi.py   # Script simulasi matematis kompensasi kurir
│   ├── simulasi_fleet.py        # Script simulasi keuangan hub skala 50 armada kurir
│   └── generate_charts.py       # Script penghasil grafik visualisasi matplotlib
└── README.md                    # Dokumentasi lengkap proyek
```

---

## 💻 Cara Menggunakan Dashboard

### 1. Buka Langsung di Browser
Cukup buka file `index.html` menggunakan browser modern (Google Chrome, Microsoft Edge, Safari, Firefox). 
Tidak membutuhkan server web khusus atau instalasi backend (dapat berjalan *offline* / *client-side*).

### 2. Jalankan Script Simulasi Python (Opsional)
Jika Anda ingin menjalankan simulasi komputasi numerik di terminal:
```bash
# Pastikan Python dan matplotlib terinstall
pip install matplotlib

# Jalankan simulasi kompensasi per kurir
python scripts/simulasi_kompensasi.py

# Jalankan simulasi keuangan armada hub cabang
python scripts/simulasi_fleet.py

# Buat ulang grafik perbandingan
python scripts/generate_charts.py
```

### 3. Deploy ke GitHub Pages (Gratis)
Karena file utama bernama `index.html`, Anda dapat langsung mengaktifkan **GitHub Pages** di repository Anda:
1. Masuk ke **Settings** > **Pages** di repository GitHub Anda.
2. Pilih branch `master` atau `main` dan folder `/ (root)`.
3. Klik **Save**. Dashboard Anda akan langsung live di internet (misal: `https://<username>.github.io/<repo-name>/`).

---

## 📐 Ringkasan Formulasi Utama

| Parameter / Variabel | Rumus / Nilai Acuan | Keterangan |
| :--- | :--- | :--- |
| **Gaji Pokok Harian** | $W_{hari} = \frac{W_{bln}}{25}$ | Berdasarkan 25 hari kerja efektif per bulan |
| **Beban Pokok per Paket** | $C_{base} = \frac{W_{hari}}{Q_{base}}$ | Ambang impas gaji pokok terhadap kuota dasar |
| **Beban per Paket (CpD)** | $CpD = \frac{Upah\_Harian}{Volume}$ | Biaya upah kurir per paket kiriman |
| **Laba Cabang** | $Laba = Gross\_Revenue - Total\_Cost$ | Revenue dikurangi upah kurir dan operasional gudang |

*(Dokumentasi matematis lengkap tersedia langsung pada Tab **"Rumus & Formulasi Model"** di dalam dashboard `index.html`).*

---

## 📚 Rujukan Ilmiah & Studi Lapangan

1. **Wang, Webster, & Rabinovich (2025)** — *Manufacturing & Service Operations Management (M&SOM)*, DOI: [10.1287/msom.2021.0367](https://doi.org/10.1287/msom.2021.0367)
2. **Arora, Choudhary, & Kireyev (2025)** — *Management Science*, DOI: [10.1287/mnsc.2023.01829](https://doi.org/10.1287/mnsc.2023.01829)
3. **Kesavan, Lambert, & Henly (2023)** — *Manufacturing & Service Operations Management (M&SOM)*, DOI: [10.1287/msom.2022.1147](https://doi.org/10.1287/msom.2022.1147)
4. **Camerer, Babcock, Loewenstein, & Thaler (1997)** — *Quarterly Journal of Economics*, DOI: [10.1162/003355397555244](https://doi.org/10.1162/003355397555244)
5. **Peraturan Pemerintah (PP) No. 51 Tahun 2023** — Database Peraturan BPK RI.

---

## 📄 Lisensi
MIT License. Bebas digunakan dan disesuaikan untuk kebutuhan operasional internal perusahaan logistik Anda.
