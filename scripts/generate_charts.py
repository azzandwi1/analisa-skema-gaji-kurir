import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axs = plt.subplots(2, 2, figsize=(15, 11), dpi=150)
fig.suptitle('Simulasi Finansial & Produktivitas: Skema Kompensasi Kurir Last-Mile', fontsize=16, fontweight='bold', y=0.98)

volumes = np.linspace(35, 125, 50)
revenue_per_parcel = 8500
hub_ops = 2500
base_salary = 140000

# Arrays for metrics
def get_metrics(v_list, model='hybrid'):
    thp_monthly = []
    cpd_list = []
    margin_list = []
    net_profit_hub = []
    
    for v in v_list:
        fuel = max(350, 700 - (v * 3.5))
        if model == 'hybrid':
            inc = 0
            if v > 50:
                inc += (min(v, 80) - 50) * 1500
            if v > 80:
                inc += (min(v, 110) - 80) * 2200
            if v > 110:
                inc += (min(v, 130) - 110) * 2500
            courier_pay = base_salary + (inc * 1.05) + (fuel * v)
        elif model == 'piece_rate':
            courier_pay = (2300 + fuel) * v
        elif model == 'fixed':
            courier_pay = 180000 + (fuel * v)
            
        thp = courier_pay * 25
        cpd = courier_pay / v
        rev = v * revenue_per_parcel
        cost = courier_pay + (v * hub_ops)
        profit = rev - cost
        margin = (profit / rev) * 100
        
        # Hub with 50 couriers per month
        hub_profit = profit * 50 * 25
        
        thp_monthly.append(thp / 1e6) # in Millions
        cpd_list.append(cpd)
        margin_list.append(margin)
        net_profit_hub.append(hub_profit / 1e6) # in Millions
        
    return np.array(thp_monthly), np.array(cpd_list), np.array(margin_list), np.array(net_profit_hub)

# Compute for all 3 models
thp_hyb, cpd_hyb, mar_hyb, prof_hyb = get_metrics(volumes, 'hybrid')
thp_pie, cpd_pie, mar_pie, prof_pie = get_metrics(volumes, 'piece_rate')
thp_fix, cpd_fix, mar_fix, prof_fix = get_metrics(volumes, 'fixed')

# 1. Plot 1: Take-Home Pay Kurir (Kesejahteraan & Turnover)
ax1 = axs[0, 0]
ax1.plot(volumes, thp_hyb, color='#10b981', linewidth=3, label='Hybrid Tiered (Rekomendasi)')
ax1.plot(volumes, thp_pie, color='#f59e0b', linewidth=2, linestyle='--', label='Piece-Rate (Murni Komisi)')
ax1.plot(volumes, thp_fix, color='#6366f1', linewidth=2, linestyle=':', label='Fixed Flat (Gaji Tetap)')
ax1.axhline(y=3.5, color='#ef4444', linestyle='-.', alpha=0.8, label='Batas Rata-rata UMR (Rp 3.5 Jt)')
ax1.fill_between(volumes, 0, 3.5, color='#ef4444', alpha=0.08, label='Zona Resiko Turnover Tinggi')
ax1.set_title('1. Kesejahteraan Kurir: Take-Home Pay Bulanan (Jt Rupiah)', fontweight='bold', fontsize=12)
ax1.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax1.set_ylabel('Gaji Bersih (Juta Rupiah / Bulan)', fontsize=10)
ax1.set_ylim(2, 9)
ax1.legend(loc='upper left', frameon=True, fontsize=8.5)
ax1.grid(True, linestyle='--', alpha=0.6)

# 2. Plot 2: Total Laba Bersih Cabang / Hub (50 Kurir)
ax2 = axs[0, 1]
ax2.plot(volumes, prof_hyb, color='#10b981', linewidth=3, label='Hybrid Tiered')
ax2.plot(volumes, prof_pie, color='#f59e0b', linewidth=2, linestyle='--', label='Piece-Rate')
ax2.plot(volumes, prof_fix, color='#6366f1', linewidth=2, linestyle=':', label='Fixed Flat')
ax2.set_title('2. Laba Bersih Cabang / Bulan (Armada 50 Kurir)', fontweight='bold', fontsize=12)
ax2.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax2.set_ylabel('Net Profit Hub (Juta Rupiah / Bulan)', fontsize=10)
ax2.legend(loc='upper left', frameon=True, fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.6)
# Anotasi kenaikan profit
ax2.annotate('Laba naik ~300%\n(Rp 167Jt -> Rp 494Jt)', xy=(110, 450), xytext=(65, 420),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=8),
            fontweight='bold', color='#065f46', bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec="#10b981"))

# 3. Plot 3: Cost per Delivery (Beban Tenaga Kerja per Paket)
ax3 = axs[1, 0]
ax3.plot(volumes, cpd_hyb, color='#10b981', linewidth=3, label='Hybrid Tiered (CpD Efisien)')
ax3.plot(volumes, cpd_pie, color='#f59e0b', linewidth=2, linestyle='--', label='Piece-Rate (Flat Cost)')
ax3.plot(volumes, cpd_fix, color='#6366f1', linewidth=2, linestyle=':', label='Fixed Flat (Moral Hazard Risk)')
ax3.set_title('3. Unit Cost: Biaya Kurir per Paket (CpD)', fontweight='bold', fontsize=12)
ax3.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax3.set_ylabel('Biaya Tenaga Kerja (Rupiah / Paket)', fontsize=10)
ax3.legend(loc='upper right', frameon=True, fontsize=9)
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.annotate('Dilusi Biaya Tetap:\nCpD turun dari Rp 4.060 -> Rp 2.680', xy=(75, 2850), xytext=(50, 3600),
            arrowprops=dict(facecolor='#10b981', shrink=0.05, width=1.5, headwidth=8),
            fontweight='bold', color='#065f46', bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec="#10b981"))

# 4. Plot 4: Profit Margin % Perusahaan
ax4 = axs[1, 1]
ax4.plot(volumes, mar_hyb, color='#10b981', linewidth=3, label='Hybrid Tiered (Margin Stabil 37-39%)')
ax4.plot(volumes, mar_pie, color='#f59e0b', linewidth=2, linestyle='--', label='Piece-Rate')
ax4.plot(volumes, mar_fix, color='#6366f1', linewidth=2, linestyle=':', label='Fixed Flat')
ax4.axhline(y=30, color='#64748b', linestyle=':', label='Target Margin Sehat (>30%)')
ax4.set_title('4. Ketahanan Margin Perusahaan (% Net Profit Margin)', fontweight='bold', fontsize=12)
ax4.set_xlabel('Volume Paket / Kurir / Hari', fontsize=10)
ax4.set_ylabel('Net Profit Margin (%)', fontsize=10)
ax4.set_ylim(0, 55)
ax4.legend(loc='lower right', frameon=True, fontsize=9)
ax4.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
output_path = r'C:\Users\azzan\.gemini\antigravity\brain\c847091a-a325-4dd0-a6e3-59593bb5b699\grafik_simulasi_kompensasi.png'
plt.savefig(output_path, dpi=200, bbox_inches='tight')
print("Grafik berhasil disimpan di:", output_path)
