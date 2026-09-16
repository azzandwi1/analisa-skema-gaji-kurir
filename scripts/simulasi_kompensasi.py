"""
Simulasi Model Kompensasi Kurir: Hybrid Tiered vs Pure Piece-Rate vs Pure Fixed
Analisis Unit Economics, Margin Perusahaan, dan Take Home Pay Kurir saat Volume Bertambah.
"""

def simulate_courier_day(volume, model="hybrid", sla_score=0.98):
    # Asumsi Pendapatan Perusahaan (Last Mile Delivery Fee dari E-commerce/Klien)
    revenue_per_parcel = 8500  # Rp 8.500 per paket berhasil antar
    
    # Biaya operasional non-kurir (Sortir HUB, app tech, line-haul amortized per paket)
    hub_ops_per_parcel = 2500  # Rp 2.500 per paket
    
    # Tunjangan BBM riil per paket (makin banyak paket dalam cluster, cost per paket makin efisien)
    # Density effect: 40 paket = Rp 600/pkt, 100 paket = Rp 400/pkt
    fuel_allowance_per_parcel = max(350, 700 - (volume * 3.5))
    
    # 1. MODEL HYBRID (Rekomendasi)
    # Gaji Pokok Harian = Rp 140.000 (Setara UMR ~Rp 3,5jt - 3,8jt / 25 hari kerja)
    # Kuota dasar = 50 paket (tercover gaji pokok)
    # Tier 1 (51 - 80) = Rp 1.500 / pkt
    # Tier 2 (81 - 110) = Rp 2.200 / pkt
    # Tier 3 (> 110) = Rp 2.500 / pkt (capped at 130 max safe)
    if model == "hybrid":
        base_salary = 140000
        quota = 50
        
        # Hitung insentif bertingkat
        incentive = 0
        if volume > 50:
            tier1 = min(volume, 80) - 50
            incentive += tier1 * 1500
        if volume > 80:
            tier2 = min(volume, 110) - 80
            incentive += tier2 * 2200
        if volume > 110:
            tier3 = min(volume, 130) - 110
            incentive += tier3 * 2500
            
        # Quality Multiplier berdasarkan SLA
        # Jika SLA >= 0.96 -> 1.05x, 0.90 - 0.95 -> 1.0x, < 0.90 -> 0.8x
        if sla_score >= 0.96:
            quality_multiplier = 1.05
        elif sla_score >= 0.90:
            quality_multiplier = 1.00
        else:
            quality_multiplier = 0.80
            
        courier_pay = base_salary + (incentive * quality_multiplier) + (fuel_allowance_per_parcel * volume)
        
    # 2. MODEL PURE PIECE-RATE (Komisi Murni Tanpa Gaji Pokok)
    # Rata-rata industri: Rp 2.300/paket flat + BBM Rp 400/pkt
    elif model == "piece_rate":
        commission_per_parcel = 2300
        courier_pay = (commission_per_parcel + fuel_allowance_per_parcel) * volume
        
    # 3. MODEL PURE FIXED (Gaji Pokok Flat Tanpa Insentif)
    # Gaji harian Rp 180.000 + BBM Rp 400/pkt
    elif model == "fixed":
        base_salary = 180000
        courier_pay = base_salary + (fuel_allowance_per_parcel * volume)

    # Perhitungan Finansial Perusahaan
    gross_revenue = volume * revenue_per_parcel
    total_courier_cost = courier_pay
    total_hub_ops = volume * hub_ops_per_parcel
    total_company_cost = total_courier_cost + total_hub_ops
    net_profit = gross_revenue - total_company_cost
    
    cpd = total_courier_cost / volume if volume > 0 else 0
    profit_margin_pct = (net_profit / gross_revenue) * 100 if gross_revenue > 0 else 0
    
    return {
        "volume": volume,
        "model": model,
        "revenue": gross_revenue,
        "courier_pay": courier_pay,
        "cpd": cpd,
        "net_profit": net_profit,
        "margin_pct": profit_margin_pct,
        "monthly_thp": courier_pay * 25 # 25 hari kerja
    }

print(f"{'Volume':<8} | {'Model':<12} | {'Kurir THP/Hari':<15} | {'Kurir THP/Bln':<15} | {'Biaya Kurir/Pkt':<16} | {'Net Profit/Hari':<16} | {'Margin %':<8}")
print("-" * 100)

volumes = [40, 50, 70, 85, 100, 120]
for v in volumes:
    for m in ["hybrid", "piece_rate", "fixed"]:
        res = simulate_courier_day(v, model=m)
        print(f"{res['volume']:<8} | {res['model']:<12} | Rp {res['courier_pay']:>10,.0f} | Rp {res['monthly_thp']:>10,.0f} | Rp {res['cpd']:>11,.0f} | Rp {res['net_profit']:>11,.0f} | {res['margin_pct']:>6.1f}%")
    print("-" * 100)
