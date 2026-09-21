"""
Simulasi Model Kompensasi Kurir: Hybrid Tiered vs Pure Piece-Rate vs Pure Fixed vs Target Quota (Cliff Bonus)
Analisis Unit Economics, Margin Perusahaan, dan Take Home Pay Kurir saat Volume Bertambah.
Tersinkronisasi penuh dengan model matematis pada dashboard web (index.html).
"""

def simulate_courier_day(
    volume,
    model="hybrid",
    base_monthly=3500000,
    base_quota=50,
    ldi=1.00,
    sla_score=0.97,
    use_sla=True,
    revenue_per_parcel=8500,
    hub_ops_per_parcel=2500,
    include_fuel=False,
    days=25
):
    """
    Menghitung kompensasi harian & bulanan seorang kurir serta unit economics cabang.
    
    Parameter:
    - volume: Jumlah paket berhasil antar per hari
    - model: 'hybrid', 'piece_rate', 'fixed', atau 'quota'
    - base_monthly: Acuan gaji pokok bulanan (Rp)
    - base_quota: Kuota paket dasar penutup gaji pokok (paket/hari)
    - ldi: Logistics Difficulty Index (faktor kesulitan topografi, infra, traffic)
    - sla_score: Skor keberhasilan antar FADR (0.80 - 1.00)
    - use_sla: Boolean apakah pengali kualitas SLA aktif
    - revenue_per_parcel: Pendapatan ongkir yang diterima cabang per paket (Rp)
    - hub_ops_per_parcel: Biaya sortir & operasional gudang hub per paket (Rp)
    - include_fuel: Boolean apakah tunjangan bahan bakar dimasukkan ke upah kurir (default: False = upah murni)
    - days: Jumlah hari kerja efektif per bulan (default: 25)
    """
    base_daily = base_monthly / days
    
    # 1. Parameter Adaptif LDI (Logistics Difficulty Index)
    t1_span = max(8, round(30 / ldi))
    t2_span = max(8, round(25 / ldi))
    t1_max = base_quota + t1_span
    t2_max = t1_max + t2_span
    
    t1_rate = round(1600 * ldi)
    t2_rate = round(2200 * ldi)
    t3_rate = round(2500 * ldi)
    pie_rate = round(2500 * ldi)
    
    # 2. SLA Quality Multiplier
    sla_mult = 1.00
    if use_sla:
        if sla_score >= 0.96:
            sla_mult = 1.05
        elif sla_score >= 0.90:
            sla_mult = 1.00
        else:
            sla_mult = 0.80
            
    # 3. Perhitungan Upah Berdasarkan Skema
    if model == "hybrid":
        # Gaji pokok + bonus berjenjang progresif + pengali SLA
        incentive = 0
        if volume > base_quota:
            incentive += (min(volume, t1_max) - base_quota) * t1_rate
        if volume > t1_max:
            incentive += (min(volume, t2_max) - t1_max) * t2_rate
        if volume > t2_max:
            incentive += (volume - t2_max) * t3_rate
        daily_pay = base_daily + (incentive * sla_mult)
        
    elif model == "piece_rate":
        # Komisi murni per paket (tanpa gaji pokok)
        daily_pay = pie_rate * volume
        
    elif model == "fixed":
        # Gaji tetap flat per hari (tanpa insentif volume)
        daily_pay = base_daily
        
    elif model == "quota":
        # Target kuota minimal (gaji pokok + cliff bonus jika tembus ambang)
        qta_span = max(5, round(15 / ldi))
        qta_threshold = base_quota + qta_span
        bonus = 0
        if volume >= qta_threshold:
            bonus = (volume - base_quota) * t1_rate
        daily_pay = base_daily + bonus
        
    else:
        raise ValueError(f"Model '{model}' tidak dikenal. Pilih: 'hybrid', 'piece_rate', 'fixed', atau 'quota'.")
        
    # Komponen Tunjangan BBM (Opsional jika ingin dihitung gabung)
    fuel_per_parcel = max(350, 700 - (volume * 3.5)) if include_fuel else 0
    daily_pay += fuel_per_parcel * volume
    
    # Perhitungan Finansial & Unit Economics
    monthly_thp = daily_pay * days
    cpd = daily_pay / volume if volume > 0 else 0
    gross_revenue = volume * revenue_per_parcel
    hub_ops_cost = volume * hub_ops_per_parcel
    total_hub_cost = daily_pay + hub_ops_cost
    net_profit = gross_revenue - total_hub_cost
    margin_pct = (net_profit / gross_revenue) * 100 if gross_revenue > 0 else 0
    
    return {
        "volume": volume,
        "model": model,
        "daily_pay": daily_pay,
        "monthly_thp": monthly_thp,
        "cpd": cpd,
        "revenue": gross_revenue,
        "total_cost": total_hub_cost,
        "net_profit": net_profit,
        "margin_pct": margin_pct,
        "t1_max": t1_max,
        "t2_max": t2_max,
        "t1_rate": t1_rate,
        "t2_rate": t2_rate,
        "t3_rate": t3_rate,
        "pie_rate": pie_rate
    }

if __name__ == "__main__":
    print("=" * 115)
    print("SIMULASI KOMPENSASI KURIR (4 SKEMA) - ACUAN UMK RP 3.5 JT (KUOTA 50 PKT/HARI, LDI 1.0x, SLA 97%)")
    print("=" * 115)
    header = f"{'Volume':<8} | {'Model':<14} | {'Upah Harian':<16} | {'THP Kurir/Bln':<16} | {'Biaya/Pkt (CpD)':<16} | {'Net Profit/Hari':<16} | {'Margin %':<8}"
    print(header)
    print("-" * 115)
    
    volumes = [40, 50, 70, 80, 100, 120]
    models = ["hybrid", "piece_rate", "fixed", "quota"]
    
    for v in volumes:
        for m in models:
            res = simulate_courier_day(v, model=m, base_monthly=3500000, base_quota=50, ldi=1.00, sla_score=0.97)
            print(f"{res['volume']:<8} | {res['model']:<14} | Rp {res['daily_pay']:>11,.0f} | Rp {res['monthly_thp']:>11,.0f} | Rp {res['cpd']:>11,.0f} | Rp {res['net_profit']:>11,.0f} | {res['margin_pct']:>6.1f}%")
        print("-" * 115)
