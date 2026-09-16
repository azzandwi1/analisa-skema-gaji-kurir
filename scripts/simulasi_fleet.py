import sys
import os

# Tambahkan path scratch ke sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulasi_kompensasi import simulate_courier_day

print("=== SIMULASI FLEET (50 KURIR) SELAMA 1 BULAN (25 HARI KERJA) ===")
header = f"{'Skenario Paket/Hari':<22} | {'Total Paket/Bln':<15} | {'Omset (Gross)':<18} | {'Total Gaji Kurir':<18} | {'Net Profit Hub':<18} | {'Margin %':<8}"
print(header)
print("-" * len(header))

for v in [40, 50, 75, 90, 105, 120]:
    res = simulate_courier_day(v, model='hybrid', sla_score=0.98)
    total_pkts = v * 50 * 25
    omset = res['revenue'] * 50 * 25
    courier_cost = res['courier_pay'] * 50 * 25
    net_profit = res['net_profit'] * 50 * 25
    margin = (net_profit / omset) * 100
    kurir_thp = res['monthly_thp']
    
    print(f"{v} pkt/kurir/hari ({kurir_thp/1e6:.1f}jt) | {total_pkts:>11,d} pkt | Rp {omset:>14,.0f} | Rp {courier_cost:>14,.0f} | Rp {net_profit:>14,.0f} | {margin:>6.1f}%")
