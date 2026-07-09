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

    print(f"\n📅 KAYITLI RANDEVULAR ({len(appointments)} kayıt):")
    if not appointments:
        print("   (Henüz kayıtlı randevu bulunmuyor)")
    else:
        print(
            f"   {'KAYNAK':<10} | {'TARİH & SAAT (UTC)':<20} | {'DURUM':<10} | {'TUTAR'}"
        )
        print("   " + "-" * 58)
        for a in appointments:
            source = a.get("source", "whatsapp").upper()
            start_dt = a.get("start_time")
            dt_str = start_dt.strftime("%Y-%m-%d %H:%M") if isinstance(start_dt, datetime) else str(start_dt)
            status = a.get("status", "pending")
            price = str(a.get("total_price", "0"))
            print(f"   {source:<10} | {dt_str:<20} | {status:<10} | {price} TL")

    print("\n" + "=" * 65)


def main() -> None:
    asyncio.run(show_database_summary())


if __name__ == "__main__":
    main()
