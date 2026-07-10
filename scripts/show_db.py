"""
MongoDB Veritabanı Özet Görüntüleyici.

Bu betik veritabanındaki işletmeleri, personelleri ve alınan randevuları
okunabilir bir tablo olarak ekrana yazdırır.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from app.core.db import get_db

logging.basicConfig(level=logging.WARNING)


async def show_database_summary() -> None:
    db = get_db()

    print("=" * 65)
    print("                MONGODB VERİTABANI ÖZETİ")
    print("=" * 65)

    # 1. İşletmeler
    businesses = []
    async for b in db.businesses.find():
        businesses.append(b)

    print(f"\n🏢 İŞLETMELER ({len(businesses)} kayıt):")
    for b in businesses:
        name = b.get("name", "Bilinmiyor")
        b_id = b.get("business_id", "Bilinmiyor")
        print(f"   • {name:<25} | Kimlik (Slug): {b_id}")

    # 2. Müşteriler
    customers = []
    async for c in db.customers.find():
        customers.append(c)
    print(f"\n👥 MÜŞTERİLER ({len(customers)} kayıt):")
    for c in customers:
        name = c.get("name", "İsimsiz")
        phone = c.get("phone", "Yok")
        print(f"   • {name:<25} | Telefon: {phone}")

    # 3. Randevular
    appointments = []
    async for a in db.appointments.find().sort("start_time", 1):
        appointments.append(a)

    print(f"\n📅 KAYITLI DETAYLI RANDEVULAR ({len(appointments)} kayıt):")
    if not appointments:
        print("   (Henüz kayıtlı randevu bulunmuyor)")
    else:
        header = f"   {'TARİH & SAAT (TR)':<19} | {'MÜŞTERİ ADI':<22} | {'USTA (PERSONEL)':<18} | {'HİZMET':<18} | {'DURUM':<10} | {'TUTAR'}"
        print(header)
        print("   " + "-" * 105)
        for a in appointments:
            # Tarih & Saat (+3 saat Türkiye Saati)
            start_dt = a.get("start_time")
            if isinstance(start_dt, datetime):
                from datetime import timedelta
                tr_dt = start_dt + timedelta(hours=3)
                dt_str = tr_dt.strftime("%d.%m.%Y - %H:%M")
            else:
                dt_str = str(start_dt)

            # Müşteri Bilgisi
            cust = await db.customers.find_one({"_id": a.get("customer_id")})
            cust_name = cust.get("name", "Bilinmiyor") if cust else "Bilinmiyor"

            # Personel (Usta) Bilgisi
            staff = await db.staff.find_one({"_id": a.get("staff_id")})
            staff_name = staff.get("name", "Bilinmiyor") if staff else "Bilinmiyor"

            # Hizmet Bilgisi
            service_names = []
            for s_id in a.get("services", []):
                srv = await db.services.find_one({"_id": s_id})
                if srv:
                    service_names.append(srv.get("name", ""))
            srv_str = ", ".join(service_names) if service_names else "Saç Kesimi"

            status = a.get("status", "pending")
            price = str(a.get("total_price", "0"))
            print(f"   {dt_str:<19} | {cust_name:<22} | {staff_name:<18} | {srv_str:<18} | {status:<10} | {price} TL")

    print("\n" + "=" * 108)


def main() -> None:
    asyncio.run(show_database_summary())


if __name__ == "__main__":
    main()
