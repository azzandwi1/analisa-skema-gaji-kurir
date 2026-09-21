import sys
import os

# Pastikan direktori scripts ada di sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulasi_kompensasi import simulate_courier_day

def run_fleet_simulation(fleet_size=50, days=25, rev_per_parcel=8500, hub_ops=2500):
    print("=" * 125)
    print(f"SIMULASI KEUANGAN ARMADA HUB CABANG ({fleet_size} KURIR, {days} HARI KERJA BULANAN)")
    print(f"Tarif Ongkir: Rp {rev_per_parcel:,.0f}/pkt | Biaya Operasional Gudang/Sortir: Rp {hub_ops:,.0f}/pkt")
    print("=" * 125)
    
    # 1. Perbandingan Head-to-Head 4 Skema pada Volume Normal (80 Paket/Kurir/Hari)
    norm_v = 80
    total_norm_pkts = norm_v * fleet_size * days
    gross_omset = total_norm_pkts * rev_per_parcel
    
    print(f"\n[A] PERBANDINGAN 4 SKEMA PADA VOLUME NORMAL ({norm_v} PAKET / KURIR / HARI)")
    print(f"Total Pengiriman Hub: {total_norm_pkts:,.0f} Paket/Bulan | Omset Kotor Hub: Rp {gross_omset:,.0f}")
    print("-" * 125)
    header_a = f"{'Skema Kompensasi':<28} | {'THP Kurir/Bln':<15} | {'Beban Gaji Kurir':<18} | {'Biaya Gudang Hub':<18} | {'Net Profit Hub':<18} | {'Margin %':<8}"
    print(header_a)
    print("-" * 125)
    
    models = [
        ("hybrid", "1. Hybrid Tiered (Rekomendasi)"),
        ("piece_rate", "2. Piece-Rate (Komisi Murni)"),
        ("fixed", "3. Fixed Flat (Gaji Tetap)"),
        ("quota", "4. Quota (Bonus Tebing)")
    ]
    
    for m_key, m_label in models:
        res = simulate_courier_day(norm_v, model=m_key, days=days)
        total_payroll = res['monthly_thp'] * fleet_size
        total_hub_ops = norm_v * hub_ops * fleet_size * days
        net_profit = gross_omset - (total_payroll + total_hub_ops)
        margin = (net_profit / gross_omset) * 100
        print(f"{m_label:<28} | Rp {res['monthly_thp']:>10,.0f} | Rp {total_payroll:>14,.0f} | Rp {total_hub_ops:>14,.0f} | Rp {net_profit:>14,.0f} | {margin:>6.1f}%")
    print("-" * 125)

    # 2. Skalabilitas Skema Hibrida Saat Volume Berfluktuasi (40 s/d 120 Paket/Hari)
    print(f"\n[B] SKALABILITAS SKEMA HIBRIDA PADA BERBAGAI SKENARIO VOLUME (LOW TO PEAK SEASON)")
    print("-" * 125)
    header_b = f"{'Volume/Kurir/Hari':<20} | {'Total Paket/Bln':<16} | {'THP Kurir/Bln':<15} | {'Total Gaji Kurir':<18} | {'Net Profit Hub':<18} | {'Margin %':<8}"
    print(header_b)
    print("-" * 125)
    
    volumes = [40, 50, 65, 80, 95, 110, 120]
    for v in volumes:
        res = simulate_courier_day(v, model="hybrid", days=days)
        total_pkts = v * fleet_size * days
        omset = total_pkts * rev_per_parcel
        total_payroll = res['monthly_thp'] * fleet_size
        net_profit = res['net_profit'] * fleet_size * days
        margin = (net_profit / omset) * 100 if omset > 0 else 0
        
        status = "(Sepi / Aman)" if v <= 50 else ("(Normal)" if v <= 80 else "(Padat / Peak)")
        v_str = f"{v} pkt {status}"
        print(f"{v_str:<20} | {total_pkts:>12,d} pkt | Rp {res['monthly_thp']:>10,.0f} | Rp {total_payroll:>14,.0f} | Rp {net_profit:>14,.0f} | {margin:>6.1f}%")
    print("-" * 125)

if __name__ == "__main__":
    run_fleet_simulation()
