"""
Unit Test & Verifikasi Numerik Model Kompensasi Kurir.
Memvalidasi kesesuaian formula matematika Python terhadap hasil komputasi web simulator (index.html).
"""

import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from simulasi_kompensasi import simulate_courier_day

class TestCompensationSimulation(unittest.TestCase):
    
    def setUp(self):
        self.base_monthly = 3500000
        self.base_quota = 50
        self.days = 25
        self.base_daily = self.base_monthly / self.days  # 140,000
        self.rev = 8500
        self.hub_ops = 2500
        
    def test_baseline_quota_boundary(self):
        """Uji saat volume tepat di kuota dasar (50 paket)"""
        v = 50
        res_hyb = simulate_courier_day(v, model="hybrid", base_monthly=self.base_monthly, base_quota=self.base_quota)
        res_fix = simulate_courier_day(v, model="fixed", base_monthly=self.base_monthly, base_quota=self.base_quota)
        res_qta = simulate_courier_day(v, model="quota", base_monthly=self.base_monthly, base_quota=self.base_quota)
        
        # Pada volume = 50, hybrid, fixed, dan quota harus sama persis dengan gaji pokok harian
        self.assertEqual(res_hyb["daily_pay"], 140000)
        self.assertEqual(res_hyb["monthly_thp"], 3500000)
        self.assertEqual(res_fix["daily_pay"], 140000)
        self.assertEqual(res_qta["daily_pay"], 140000)
        
        # Biaya kurir per paket (CpD) = 140.000 / 50 = Rp 2.800
        self.assertEqual(res_hyb["cpd"], 2800)
        
    def test_low_volume_safety_net(self):
        """Uji jaring pengaman saat volume sepi (40 paket)"""
        v = 40
        res_hyb = simulate_courier_day(v, model="hybrid", base_monthly=self.base_monthly, base_quota=self.base_quota)
        res_pie = simulate_courier_day(v, model="piece_rate", base_monthly=self.base_monthly, base_quota=self.base_quota)
        
        # Hybrid melindungi kurir tetap mendapat Rp 3.5 Jt / bulan
        self.assertEqual(res_hyb["monthly_thp"], 3500000)
        
        # Piece-rate anjlok ke 40 * 2500 * 25 = Rp 2.5 Jt (di bawah UMR)
        self.assertEqual(res_pie["monthly_thp"], 2500000)
        self.assertTrue(res_pie["monthly_thp"] < res_hyb["monthly_thp"])
        
    def test_normal_volume_tiering(self):
        """Uji tiering progresif pada volume normal (80 paket) dengan SLA 97% (pengali 1.05x)"""
        v = 80
        # Tier 1 span = 30 paket (51 s/d 80), rate = Rp 1.600
        # Insentif = 30 * 1600 = 48.000
        # Dengan SLA 97% -> pengali 1.05 -> 48.000 * 1.05 = 50.400
        # Upah harian = 140.000 + 50.400 = 190.400
        # THP Bulanan = 190.400 * 25 = 4.760.000
        res_hyb = simulate_courier_day(v, model="hybrid", base_monthly=self.base_monthly, base_quota=self.base_quota, sla_score=0.97)
        self.assertEqual(res_hyb["daily_pay"], 190400)
        self.assertEqual(res_hyb["monthly_thp"], 4760000)
        self.assertEqual(res_hyb["cpd"], 190400 / 80)
        
        # Quota model pada V=80: ambang = 50 + 15 = 65. V=80 >= 65 -> bonus = (80 - 50) * 1600 = 48.000
        # Upah harian quota = 140.000 + 48.000 = 188.000
        res_qta = simulate_courier_day(v, model="quota", base_monthly=self.base_monthly, base_quota=self.base_quota)
        self.assertEqual(res_qta["daily_pay"], 188000)
        self.assertEqual(res_qta["monthly_thp"], 4700000)
        
    def test_ldi_scaling(self):
        """Uji adaptabilitas LDI (contoh LDI = 1.25x di medan berat)"""
        ldi = 1.25
        v = 70
        res = simulate_courier_day(v, model="hybrid", base_monthly=self.base_monthly, base_quota=40, ldi=ldi)
        
        # Tarif harus naik sebanding LDI: round(1600 * 1.25) = 2000
        self.assertEqual(res["t1_rate"], 2000)
        self.assertEqual(res["pie_rate"], round(2500 * 1.25))

    def test_hub_profitability_equations(self):
        """Uji konsistensi laba dan margin hub"""
        v = 80
        res = simulate_courier_day(v, model="hybrid", revenue_per_parcel=self.rev, hub_ops_per_parcel=self.hub_ops)
        expected_rev = v * self.rev  # 80 * 8500 = 680,000
        expected_cost = res["daily_pay"] + (v * self.hub_ops)
        expected_profit = expected_rev - expected_cost
        expected_margin = (expected_profit / expected_rev) * 100
        
        self.assertEqual(res["revenue"], expected_rev)
        self.assertEqual(res["total_cost"], expected_cost)
        self.assertEqual(res["net_profit"], expected_profit)
        self.assertAlmostEqual(res["margin_pct"], expected_margin, places=4)

if __name__ == "__main__":
    unittest.main()
