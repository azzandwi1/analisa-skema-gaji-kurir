import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Tambahkan direktori saat ini ke sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulasi_kompensasi import simulate_courier_day

# Set style matplotlib yang bersih dan elegan
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axs = plt.subplots(2, 2, figsize=(16, 12), dpi=150)
fig.suptitle('Simulasi Finansial & Produktivitas: Komparasi 4 Skema Kompensasi Kurir Last-Mile', fontsize=16, fontweight='bold', y=0.98)

volumes = np.linspace(35, 125, 60)
fleet_size = 50
days = 25
base_monthly = 3500000

# Fungsi pengambil metrik untuk array volume
def get_metrics_for_model(v_list, model_name):
    thp_monthly = []
    cpd_list = []
    margin_list = []
    net_profit_hub = []
    
    for v in v_list:
        res = simulate_courier_day(v, model=model_name, base_monthly=base_monthly, base_quota=50, ldi=1.0, days=days)
        thp_monthly.append(res['monthly_thp'] / 1e6)  # dalam Juta Rupiah
        cpd_list.append(res['cpd'])
        margin_list.append(res['margin_pct'])
        
        # Total laba hub bulanan untuk 50 kurir
        hub_profit_monthly = res['net_profit'] * fleet_size * days
        net_profit_hub.append(hub_profit_monthly / 1e6)  # dalam Juta Rupiah
        
    return np.array(thp_monthly), np.array(cpd_list), np.array(margin_list), np.array(net_profit_hub)

# Komputasi untuk 4 skema
thp_hyb, cpd_hyb, mar_hyb, prof_hyb = get_metrics_for_model(volumes, 'hybrid')
thp_pie, cpd_pie, mar_pie, prof_pie = get_metrics_for_model(volumes, 'piece_rate')
thp_fix, cpd_fix, mar_fix, prof_fix = get_metrics_for_model(volumes, 'fixed')
thp_qta, cpd_qta, mar_qta, prof_qta = get_metrics_for_model(volumes, 'quota')

# Definisi warna & format kurva
c_hyb, c_pie, c_fix, c_qta = '#10b981', '#f59e0b', '#3b82f6', '#8b5cf6'

# -------------------------------------------------------------
# PLOT 1: Kesejahteraan Kurir (Take-Home Pay Bulanan)
# -------------------------------------------------------------
ax1 = axs[0, 0]
ax1.plot(volumes, thp_hyb, color=c_hyb, linewidth=3, label='1. Hybrid Tiered (Rekomendasi)')
ax1.plot(volumes, thp_pie, color=c_pie, linewidth=2, linestyle='--', label='2. Piece-Rate (Komisi Murni)')
ax1.plot(volumes, thp_fix, color=c_fix, linewidth=2, linestyle=':', label='3. Fixed Flat (Gaji Tetap)')
ax1.plot(volumes, thp_qta, color=c_qta, linewidth=2, linestyle='-.', label='4. Quota (Cliff Bonus)')
ax1.axhline(y=3.5, color='#ef4444', linestyle='-.', alpha=0.8, label='Batas Acuan UMK (Rp 3.5 Jt)')
ax1.fill_between(volumes, 0, 3.5, color='#ef4444', alpha=0.08, label='Zona Resiko Turnover Tinggi')

ax1.set_title('1. Kesejahteraan Kurir: Take-Home Pay Bulanan (Juta Rp)', fontweight='bold', fontsize=12)
ax1.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax1.set_ylabel('Gaji Bersih Kurir (Juta Rupiah / Bulan)', fontsize=10)
ax1.set_ylim(2, 8.5)
ax1.legend(loc='upper left', frameon=True, fontsize=8.5)
ax1.grid(True, linestyle='--', alpha=0.6)

# -------------------------------------------------------------
# PLOT 2: Laba Bersih Cabang / Hub (Armada 50 Kurir)
# -------------------------------------------------------------
ax2 = axs[0, 1]
ax2.plot(volumes, prof_hyb, color=c_hyb, linewidth=3, label='1. Hybrid Tiered')
ax2.plot(volumes, prof_pie, color=c_pie, linewidth=2, linestyle='--', label='2. Piece-Rate')
ax2.plot(volumes, prof_fix, color=c_fix, linewidth=2, linestyle=':', label='3. Fixed Flat')
ax2.plot(volumes, prof_qta, color=c_qta, linewidth=2, linestyle='-.', label='4. Quota (Cliff Bonus)')

ax2.set_title('2. Laba Bersih Cabang / Bulan (Armada 50 Kurir)', fontweight='bold', fontsize=12)
ax2.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax2.set_ylabel('Net Profit Cabang (Juta Rupiah / Bulan)', fontsize=10)
ax2.legend(loc='upper left', frameon=True, fontsize=8.5)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.annotate('Pertumbuhan Laba Hub:\nRp 200Jt (V=50) -> Rp 540Jt (V=120)', xy=(110, 498), xytext=(62, 470),
            arrowprops=dict(facecolor=c_hyb, shrink=0.05, width=1.5, headwidth=8),
            fontweight='bold', color='#065f46', bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec=c_hyb))

# -------------------------------------------------------------
# PLOT 3: Cost per Delivery (Beban Tenaga Kerja per Paket)
# -------------------------------------------------------------
ax3 = axs[1, 0]
ax3.plot(volumes, cpd_hyb, color=c_hyb, linewidth=3, label='1. Hybrid Tiered (CpD Terkendali)')
ax3.plot(volumes, cpd_pie, color=c_pie, linewidth=2, linestyle='--', label='2. Piece-Rate (Flat Cost Rp 2.500)')
ax3.plot(volumes, cpd_fix, color=c_fix, linewidth=2, linestyle=':', label='3. Fixed Flat (Moral Hazard Risk)')
ax3.plot(volumes, cpd_qta, color=c_qta, linewidth=2, linestyle='-.', label='4. Quota (Cliff Step Effect)')

ax3.set_title('3. Biaya Tenaga Kerja per Paket (Cost per Delivery / CpD)', fontweight='bold', fontsize=12)
ax3.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax3.set_ylabel('Biaya Upah Kurir (Rupiah / Paket)', fontsize=10)
ax3.set_ylim(1000, 4500)
ax3.legend(loc='upper right', frameon=True, fontsize=8.5)
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.annotate('Efisiensi Skala Hybrid:\nCpD melandai stabil di Rp 2.380', xy=(80, 2380), xytext=(45, 1700),
            arrowprops=dict(facecolor=c_hyb, shrink=0.05, width=1.5, headwidth=8),
            fontweight='bold', color='#065f46', bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec=c_hyb))

# -------------------------------------------------------------
# PLOT 4: Profit Margin % Perusahaan
# -------------------------------------------------------------
ax4 = axs[1, 1]
ax4.plot(volumes, mar_hyb, color=c_hyb, linewidth=3, label='1. Hybrid Tiered (Margin Sehat 37-43%)')
ax4.plot(volumes, mar_pie, color=c_pie, linewidth=2, linestyle='--', label='2. Piece-Rate (Flat Margin 41.2%)')
ax4.plot(volumes, mar_fix, color=c_fix, linewidth=2, linestyle=':', label='3. Fixed Flat (Volatil)')
ax4.plot(volumes, mar_qta, color=c_qta, linewidth=2, linestyle='-.', label='4. Quota (Cliff Bonus)')
ax4.axhline(y=30, color='#64748b', linestyle=':', label='Target Margin Minimal (>30%)')

ax4.set_title('4. Ketahanan Margin Perusahaan (% Net Profit Margin)', fontweight='bold', fontsize=12)
ax4.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax4.set_ylabel('Net Profit Margin (%)', fontsize=10)
ax4.set_ylim(20, 60)
ax4.legend(loc='lower right', frameon=True, fontsize=8.5)
ax4.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Jalur penyimpanan dinamis relatif terhadap file skrip
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'grafik_simulasi_kompensasi.png')

plt.savefig(output_path, dpi=200, bbox_inches='tight')
print(f"Grafik 4 skema berhasil dibuat dan disimpan di:\n-> {output_path}")
