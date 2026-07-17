# UYARI: Bu script veritabanını sıfırlar. Production'da çalıştırmayın.
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from bson import ObjectId
from bson.decimal128 import Decimal128
from pymongo import ASCENDING, MongoClient

DB_NAME = os.getenv("MONGODB_DB", "randevum_chatbot")
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

BERBER_WA_PNID = os.getenv("WA_BERBER_MEHMET_KUTAHYA_PHONE_NUMBER_ID", "WA_PNID_PLACEHOLDER")
BERBER_WA_WABA = os.getenv("WA_BERBER_MEHMET_KUTAHYA_WABA_ID", "WA_WABA_ID_PLACEHOLDER")

UTC = timezone.utc
NOW = datetime.now(UTC)


def _d(x: str | float | int) -> Decimal128:
    return Decimal128(Decimal(str(x)))


def _full_week(open_: str, close: str, breaks=None, closed_days=()) -> list[dict]:
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return [
        {
            "day": d,
            "open": open_,
            "close": close,
            "closed": d in closed_days,
            "breaks": list(breaks or []),
        }
        for d in days
    ]


berber_id = ObjectId()
berber_staff_mehmet = ObjectId()
berber_staff_yusuf = ObjectId()
berber_svc_sac = ObjectId()
berber_svc_sakal = ObjectId()
berber_svc_komple = ObjectId()
berber_svc_cocuk = ObjectId()

berber_business = {
    "_id": berber_id,
    "business_id": "berber_mehmet_kutahya",
    "name": "Berber Mehmet",
    "business_type": "berber",
    "owner": {
        "name": "Mehmet Kaya",
        "phone": "+905551110001",
        "email": "mehmet@berbermehmet.com",
    },
    "contact": {
        "phone": "+902741110001",
        "whatsapp_number": "+905551110001",
        "instagram_username": "berber_mehmet_kutahya",
        "email": "info@berbermehmet.com",
        "address": "Cumhuriyet Cad. No:42 Merkez/Kütahya",
        "location": {"type": "Point", "coordinates": [29.9833, 39.4242]},
        "booking_url": "https://randevumonline.com/isletme/berber-mehmet-kutahya",
    },
    "socials": {
        "instagram": "https://instagram.com/berber_mehmet_kutahya",
        "facebook": None,
        "twitter": None,
        "website": None,
    },
    "channels": {
        "whatsapp": {
            "enabled": True,
            "phone_number_id": BERBER_WA_PNID,
            "business_account_id": BERBER_WA_WABA,
            "access_token_ref": "vault://wa/berber_mehmet_kutahya/access_token",
            "verify_token_ref": "vault://wa/berber_mehmet_kutahya/verify_token",
            "flow_id": None,
        },
        "instagram": {
            "enabled": True,
            "ig_user_id": "17841431819804012",
            "page_id": "FB_PAGE_ID_PLACEHOLDER",
            "access_token_ref": "vault://ig/berber_mehmet_kutahya/access_token",
        },
    },
    "ai_settings": {
        "persona": "Berber Mehmet dükkanının nazik ve kısa konuşan müşteri asistanı. Müşteriye her zaman 'siz' diye hitap eder; 'abi/kardeş/sen' gibi samimi hitaplar kullanmaz. Resmî ama sıcak.",
        "language": "tr-TR",
        "welcome_message": "Merhaba, ben Berber Mehmet'in dijital asistanıyım. Size nasıl yardımcı olabilirim?",
        "fallback_message": "Bu konuda yardımcı olamadım, mesajını dükkana ileteceğim.",
        "confirmation_required": True,
        "booking_buffer_minutes": 30,
        "max_advance_days": 30,
        "online_slot_step_minutes": 30,
        "admin_calendar_step_minutes": 15,
        "calendar_color_coding": True,
        "auto_add_to_calendar": False,
        "customer_cancel_window_minutes": 60,
        "cancel_block_limit": 5,
        "no_show_block_limit": 2,
        "online_booking_who": "everyone",
        "online_booking_mode": "standard",
        "reminder_minutes_before": 60,
        "quiet_hours": {"start": "23:30", "end": "07:30"},
    },
    "working_hours": _full_week("09:00", "20:00", closed_days=["sunday"]),
    "special_days": [
        {"date": datetime(2026, 4, 23).date().isoformat(),
         "closed": True, "open": None, "close": None,
         "reason": "Ulusal Egemenlik ve Çocuk Bayramı"},
        {"date": datetime(2026, 5, 19).date().isoformat(),
         "closed": False, "open": "10:00", "close": "18:00",
         "reason": "19 Mayıs - kısaltılmış mesai"},
    ],
    "rooms": [],
    "timezone": "Europe/Istanbul",
    "subscription": {
        "plan": "business",
        "status": "active",
        "started_at": NOW - timedelta(days=120),
        "next_billing_at": NOW + timedelta(days=15),
    },
    "is_active": True,
    "created_at": NOW - timedelta(days=120),
    "updated_at": NOW,
}

berber_services = [
    {
        "_id": berber_svc_sac, "business_id": berber_id,
        "name": "Saç Kesimi", "description": "Makas/makina ile saç kesimi.",
        "category": "Saç", "duration_minutes": 30, "price": _d(250), "currency": "TRY",
        "staff_ids": [berber_staff_mehmet, berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": berber_svc_sakal, "business_id": berber_id,
        "name": "Sakal Tıraşı", "description": "Klasik ustura ile sakal tıraşı.",
        "category": "Sakal", "duration_minutes": 20, "price": _d(150), "currency": "TRY",
        "staff_ids": [berber_staff_mehmet, berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": berber_svc_komple, "business_id": berber_id,
        "name": "Saç + Sakal", "description": "Saç kesimi ve sakal tıraşı kombo.",
        "category": "Kombo", "duration_minutes": 50, "price": _d(380), "currency": "TRY",
        "staff_ids": [berber_staff_mehmet, berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": berber_svc_cocuk, "business_id": berber_id,
        "name": "Çocuk Saç Kesimi", "description": "0-12 yaş arası saç kesimi.",
        "category": "Saç", "duration_minutes": 25, "price": _d(180), "currency": "TRY",
        "staff_ids": [berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": berber_id,
        "name": "Saç Yıkama & Fön", "description": "Yıkama, saç derisi masajı ve fön.",
        "category": "Saç", "duration_minutes": 20, "price": _d(120), "currency": "TRY",
        "staff_ids": [berber_staff_mehmet, berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": berber_id,
        "name": "Saç Boyası", "description": "Erkek saç boyama, fön dahil.",
        "category": "Saç", "duration_minutes": 45, "price": _d(400), "currency": "TRY",
        "staff_ids": [berber_staff_mehmet],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": berber_id,
        "name": "Yüz & Kulak Ağdası", "description": "Kulak, burun ve yanak ağdası.",
        "category": "Bakım", "duration_minutes": 15, "price": _d(80), "currency": "TRY",
        "staff_ids": [berber_staff_mehmet, berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": berber_id,
        "name": "Cilt Bakımı & Maske", "description": "Siyah nokta temizliği ve maske.",
        "category": "Bakım", "duration_minutes": 30, "price": _d(350), "currency": "TRY",
        "staff_ids": [berber_staff_yusuf],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
]

berber_staff = [
    {
        "_id": berber_staff_mehmet, "business_id": berber_id,
        "name": "Mehmet Kaya", "role": "Usta Berber",
        "phone": "+905551110001", "email": "mehmet@berbermehmet.com",
        "photo_url": None, "bio": "20 yıllık tecrübeli usta berber.",
        "service_ids": [berber_svc_sac, berber_svc_sakal, berber_svc_komple],
        "working_hours": _full_week("09:00", "20:00", closed_days=["sunday"]),
        "time_off": [],
        "commission_rate": 0.0,
        "is_active": True,
        "created_at": NOW - timedelta(days=120),
    },
    {
        "_id": berber_staff_yusuf, "business_id": berber_id,
        "name": "Yusuf Demir", "role": "Berber",
        "phone": "+905551110002", "email": None,
        "photo_url": None, "bio": "Çocuk kesimi konusunda uzman.",
        "service_ids": [berber_svc_sac, berber_svc_sakal, berber_svc_komple, berber_svc_cocuk],
        "working_hours": _full_week("10:00", "20:00", closed_days=["sunday", "monday"]),
        "time_off": [
            {
                "start_date": (NOW + timedelta(days=20)).date().isoformat(),
                "end_date": (NOW + timedelta(days=27)).date().isoformat(),
                "reason": "Yıllık izin",
            }
        ],
        "commission_rate": 0.30,
        "is_active": True,
        "created_at": NOW - timedelta(days=90),
    },
]


salon_id = ObjectId()
salon_staff_ayse = ObjectId()
salon_staff_zeynep = ObjectId()
salon_staff_elif = ObjectId()
salon_svc_manikur = ObjectId()
salon_svc_pedikur = ObjectId()
salon_svc_cilt = ObjectId()
salon_svc_kas = ObjectId()
salon_svc_lazer = ObjectId()
salon_svc_sac_boyama = ObjectId()

salon_business = {
    "_id": salon_id,
    "business_id": "ayse_guzellik_kadikoy",
    "name": "Ayşe Güzellik & Bakım",
    "business_type": "guzellik_salonu",
    "owner": {
        "name": "Ayşe Yılmaz",
        "phone": "+905552220001",
        "email": "ayse@ayseguzellik.com",
    },
    "contact": {
        "phone": "+902162220001",
        "whatsapp_number": "+905552220001",
        "instagram_username": "ayseguzellik_kadikoy",
        "email": "randevu@ayseguzellik.com",
        "address": "Caferağa Mah. Moda Cad. No:88/3 Kadıköy/İstanbul",
        "location": {"type": "Point", "coordinates": [29.0274, 40.9876]},
        "booking_url": "https://randevumonline.com/isletme/ayse-guzellik-kadikoy",
    },
    "socials": {
        "instagram": "https://instagram.com/ayseguzellik_kadikoy",
        "facebook": "https://facebook.com/ayseguzellik",
        "twitter": None,
        "website": "https://ayseguzellik.com",
    },
    "channels": {
        "whatsapp": {
            "enabled": True,
            "phone_number_id": "WA_PNID_PLACEHOLDER",
            "business_account_id": "WA_WABA_PLACEHOLDER",
            "access_token_ref": "vault://wa/ayse_guzellik_kadikoy/access_token",
            "verify_token_ref": "vault://wa/ayse_guzellik_kadikoy/verify_token",
            "flow_id": None,
        },
        "instagram": {
            "enabled": True,
            "ig_user_id": "IG_USER_ID_PLACEHOLDER",
            "page_id": "FB_PAGE_ID_PLACEHOLDER",
            "access_token_ref": "vault://ig/ayse_guzellik_kadikoy/access_token",
        },
    },
    "ai_settings": {
        "persona": "Nazik, kibar, kadın müşterilere hitap eden bir güzellik salonu asistanı. Resmi ama sıcak.",
        "language": "tr-TR",
        "welcome_message": (
            "Merhaba, Ayşe Güzellik & Bakım'a hoş geldiniz! Size nasıl yardımcı "
            "olabilirim?"
        ),
        "fallback_message": "İsteğinizi tam anlayamadım, sizi yetkilimize aktarıyorum.",
        "confirmation_required": True,
        "booking_buffer_minutes": 60,
        "max_advance_days": 45,
        "online_slot_step_minutes": 30,
        "admin_calendar_step_minutes": 15,
        "calendar_color_coding": True,
        "auto_add_to_calendar": True,
        "customer_cancel_window_minutes": 120,
        "cancel_block_limit": 3,
        "no_show_block_limit": 2,
        "online_booking_who": "registered_only",
        "online_booking_mode": "standard",
        "reminder_minutes_before": 60,
        "quiet_hours": {"start": "22:00", "end": "08:00"},
    },
    "working_hours": [
        {"day": "monday",    "open": "10:00", "close": "20:00", "closed": False, "breaks": []},
        {"day": "tuesday",   "open": "10:00", "close": "20:00", "closed": False, "breaks": []},
        {"day": "wednesday", "open": "10:00", "close": "20:00", "closed": False, "breaks": []},
        {"day": "thursday",  "open": "10:00", "close": "21:00", "closed": False, "breaks": []},
        {"day": "friday",    "open": "10:00", "close": "21:00", "closed": False, "breaks": []},
        {"day": "saturday",  "open": "10:00", "close": "19:00", "closed": False, "breaks": []},
        {"day": "sunday",    "open": "12:00", "close": "18:00", "closed": False, "breaks": []},
    ],
    "special_days": [],
    "rooms": [
        {"room_id": "room_manikur",  "name": "Manikür/Pedikür Köşesi", "capacity": 2, "notes": None},
        {"room_id": "room_cilt",     "name": "Cilt Bakım Odası",        "capacity": 1, "notes": None},
        {"room_id": "room_lazer",    "name": "Lazer Odası",             "capacity": 1,
         "notes": "Sadece sertifikalı personel."},
        {"room_id": "room_kuafor_1", "name": "Kuaför Koltuğu 1",        "capacity": 1, "notes": None},
        {"room_id": "room_kuafor_2", "name": "Kuaför Koltuğu 2",        "capacity": 1, "notes": None},
    ],
    "timezone": "Europe/Istanbul",
    "subscription": {
        "plan": "business",
        "status": "active",
        "started_at": NOW - timedelta(days=400),
        "next_billing_at": NOW + timedelta(days=8),
    },
    "is_active": True,
    "created_at": NOW - timedelta(days=400),
    "updated_at": NOW,
}

salon_services = [
    {
        "_id": salon_svc_manikur, "business_id": salon_id,
        "name": "Klasik Manikür", "description": "Tırnak şekillendirme + cila.",
        "category": "El Bakımı", "duration_minutes": 45, "price": _d(400), "currency": "TRY",
        "staff_ids": [salon_staff_zeynep, salon_staff_elif],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": salon_svc_pedikur, "business_id": salon_id,
        "name": "Klasik Pedikür", "description": "Ayak bakımı + cila.",
        "category": "Ayak Bakımı", "duration_minutes": 60, "price": _d(550), "currency": "TRY",
        "staff_ids": [salon_staff_zeynep, salon_staff_elif],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": salon_svc_cilt, "business_id": salon_id,
        "name": "Cilt Bakımı (Klasik)", "description": "Temizleme + maske + masaj.",
        "category": "Cilt Bakım", "duration_minutes": 75, "price": _d(950), "currency": "TRY",
        "staff_ids": [salon_staff_ayse],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": salon_svc_kas, "business_id": salon_id,
        "name": "Kaş Şekillendirme", "description": "İp veya ağda ile kaş.",
        "category": "Kaş", "duration_minutes": 20, "price": _d(200), "currency": "TRY",
        "staff_ids": [salon_staff_ayse, salon_staff_zeynep],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": salon_svc_lazer, "business_id": salon_id,
        "name": "Lazer Epilasyon - Bacak", "description": "Tek seans bacak lazer.",
        "category": "Lazer", "duration_minutes": 60,
        "price": _d(1500), "price_max": _d(3500), "currency": "TRY",
        "staff_ids": [salon_staff_ayse],
        "requires_room": True, "buffer_before_minutes": 5, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": salon_svc_sac_boyama, "business_id": salon_id,
        "name": "Saç Boyama (Komple)",
        "description": "Komple boya, fön dahil. Fiyat saç uzunluğuna göre değişir.",
        "category": "Saç", "duration_minutes": 120,
        "price": _d(1800), "price_max": _d(7500), "currency": "TRY",
        "staff_ids": [salon_staff_zeynep],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 15,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Kalıcı Oje", "description": "Kalıcı oje uygulaması.",
        "category": "El Bakımı", "duration_minutes": 40, "price": _d(650), "currency": "TRY",
        "staff_ids": [salon_staff_zeynep, salon_staff_elif],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Protez Tırnak", "description": "Protez tırnak; kalıcı oje ve nail art dahil.",
        "category": "El Bakımı", "duration_minutes": 90, "price": _d(1000), "currency": "TRY",
        "staff_ids": [salon_staff_elif],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "İpek Kirpik (Volume)", "description": "Volume ipek kirpik uygulaması.",
        "category": "Kirpik & Kaş", "duration_minutes": 90, "price": _d(900), "currency": "TRY",
        "staff_ids": [salon_staff_ayse],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Kirpik Lifting", "description": "Doğal kirpik lifting ve boya.",
        "category": "Kirpik & Kaş", "duration_minutes": 60, "price": _d(650), "currency": "TRY",
        "staff_ids": [salon_staff_ayse, salon_staff_zeynep],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Keratin Bakım", "description": "Keratin nem bakımı, fön dahil.",
        "category": "Saç", "duration_minutes": 90, "price": _d(2000), "currency": "TRY",
        "staff_ids": [salon_staff_zeynep],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 15,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Topuz & Saç Tasarımı", "description": "Özel gün topuz ve şekillendirme.",
        "category": "Saç", "duration_minutes": 60, "price": _d(750), "currency": "TRY",
        "staff_ids": [salon_staff_zeynep, salon_staff_ayse],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Günlük Makyaj", "description": "Günlük makyaj uygulaması.",
        "category": "Makyaj", "duration_minutes": 45, "price": _d(1000), "currency": "TRY",
        "staff_ids": [salon_staff_ayse],
        "requires_room": False, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": ObjectId(), "business_id": salon_id,
        "name": "Gelin Paketi (Tek Gün)",
        "description": "Profesyonel gelin saçı ve makyajı.",
        "category": "Gelin", "duration_minutes": 240,
        "price": _d(10000), "price_max": _d(12000), "currency": "TRY",
        "staff_ids": [salon_staff_ayse],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 15,
        "is_active": True,
    },
]

salon_staff = [
    {
        "_id": salon_staff_ayse, "business_id": salon_id,
        "name": "Ayşe Yılmaz", "role": "Salon Sahibi / Cilt Uzmanı",
        "phone": "+905552220001", "email": "ayse@ayseguzellik.com",
        "photo_url": None,
        "bio": "Cilt bakımı ve lazer epilasyon sertifikalı uzman.",
        "service_ids": [salon_svc_cilt, salon_svc_kas, salon_svc_lazer],
        "working_hours": [
            {"day": d, "open": "11:00", "close": "19:00", "closed": False, "breaks": []}
            for d in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
        ] + [{"day": "sunday", "open": "11:00", "close": "19:00", "closed": True, "breaks": []}],
        "time_off": [],
        "commission_rate": 0.0,
        "is_active": True,
        "created_at": NOW - timedelta(days=400),
    },
    {
        "_id": salon_staff_zeynep, "business_id": salon_id,
        "name": "Zeynep Demir", "role": "Kuaför / Manikürist",
        "phone": "+905552220002", "email": None,
        "photo_url": None,
        "bio": "Saç boyama ve manikür konusunda 8 yıllık tecrübe.",
        "service_ids": [salon_svc_manikur, salon_svc_pedikur, salon_svc_kas, salon_svc_sac_boyama],
        "working_hours": _full_week("10:00", "20:00", closed_days=["monday"]),
        "time_off": [],
        "commission_rate": 0.35,
        "is_active": True,
        "created_at": NOW - timedelta(days=300),
    },
    {
        "_id": salon_staff_elif, "business_id": salon_id,
        "name": "Elif Öztürk", "role": "Manikür/Pedikür Uzmanı",
        "phone": "+905552220003", "email": None,
        "photo_url": None,
        "bio": "Nail-art uzmanı.",
        "service_ids": [salon_svc_manikur, salon_svc_pedikur],
        "working_hours": _full_week("12:00", "21:00", closed_days=["sunday"]),
        "time_off": [
            {
                "start_date": (NOW + timedelta(days=10)).date().isoformat(),
                "end_date": (NOW + timedelta(days=12)).date().isoformat(),
                "reason": "Sağlık raporu",
            }
        ],
        "commission_rate": 0.30,
        "is_active": True,
        "created_at": NOW - timedelta(days=180),
    },
]


vet_id = ObjectId()
vet_staff_can = ObjectId()
vet_staff_selin = ObjectId()
vet_svc_muayene = ObjectId()
vet_svc_asi = ObjectId()
vet_svc_operasyon = ObjectId()
vet_svc_kontrol = ObjectId()

vet_business = {
    "_id": vet_id,
    "business_id": "pati_dostu_cankaya",
    "name": "Pati Dostu Veteriner Kliniği",
    "business_type": "veteriner",
    "owner": {
        "name": "Can Vural",
        "phone": "+905553330001",
        "email": "can@patidostu.com",
    },
    "contact": {
        "phone": "+903123330001",
        "whatsapp_number": "+905553330001",
        "instagram_username": "patidostuvet",
        "email": "klinik@patidostu.com",
        "address": "Tunalı Hilmi Cad. No:55/B Çankaya/Ankara",
        "location": {"type": "Point", "coordinates": [32.8597, 39.9334]},
        "booking_url": "https://randevumonline.com/isletme/pati-dostu-cankaya",
    },
    "socials": {
        "instagram": "https://instagram.com/patidostuvet",
        "facebook": None,
        "twitter": None,
        "website": "https://patidostu.com",
    },
    "channels": {
        "whatsapp": {
            "enabled": True,
            "phone_number_id": "WA_PNID_PLACEHOLDER",
            "business_account_id": "WA_WABA_PLACEHOLDER",
            "access_token_ref": "vault://wa/pati_dostu_cankaya/access_token",
            "verify_token_ref": "vault://wa/pati_dostu_cankaya/verify_token",
            "flow_id": None,
        },
        "instagram": {
            "enabled": True,
            "ig_user_id": "IG_USER_ID_PLACEHOLDER",
            "page_id": "FB_PAGE_ID_PLACEHOLDER",
            "access_token_ref": "vault://ig/pati_dostu_cankaya/access_token",
        },
    },
    "ai_settings": {
        "persona": (
            "Sakin, profesyonel ve şefkatli bir veteriner kliniği asistanı. "
            "Hayvan ismini ve türünü mutlaka sorar. Acil durumda hemen klinik telefonunu paylaşır."
        ),
        "language": "tr-TR",
        "welcome_message": (
            "Merhaba, Pati Dostu Veteriner Kliniği'ne hoş geldiniz. "
            "Size nasıl yardımcı olabiliriz?"
        ),
        "fallback_message": "Acil bir durumsa lütfen 0312 333 00 01 numarasını arayın.",
        "confirmation_required": True,
        "booking_buffer_minutes": 60,
        "max_advance_days": 30,
        "online_slot_step_minutes": 15,
        "admin_calendar_step_minutes": 15,
        "calendar_color_coding": True,
        "auto_add_to_calendar": False,
        "customer_cancel_window_minutes": 240,
        "cancel_block_limit": 5,
        "no_show_block_limit": 2,
        "online_booking_who": "everyone",
        "online_booking_mode": "standard",
        "reminder_minutes_before": 120,
        "quiet_hours": {"start": "22:00", "end": "08:00"},
    },
    "working_hours": [
        {"day": "monday",    "open": "09:00", "close": "19:00", "closed": False,
         "breaks": [{"start": "13:00", "end": "14:00"}]},
        {"day": "tuesday",   "open": "09:00", "close": "19:00", "closed": False,
         "breaks": [{"start": "13:00", "end": "14:00"}]},
        {"day": "wednesday", "open": "09:00", "close": "19:00", "closed": False,
         "breaks": [{"start": "13:00", "end": "14:00"}]},
        {"day": "thursday",  "open": "09:00", "close": "19:00", "closed": False,
         "breaks": [{"start": "13:00", "end": "14:00"}]},
        {"day": "friday",    "open": "09:00", "close": "19:00", "closed": False,
         "breaks": [{"start": "13:00", "end": "14:00"}]},
        {"day": "saturday",  "open": "10:00", "close": "16:00", "closed": False, "breaks": []},
        {"day": "sunday",    "open": "00:00", "close": "00:00", "closed": True,  "breaks": []},
    ],
    "special_days": [],
    "rooms": [
        {"room_id": "muayene_1",   "name": "Muayene Odası 1", "capacity": 1, "notes": None},
        {"room_id": "muayene_2",   "name": "Muayene Odası 2", "capacity": 1, "notes": None},
        {"room_id": "operasyon",   "name": "Operasyon Odası", "capacity": 1,
         "notes": "Steril alan, randevular sadece sabah."},
    ],
    "timezone": "Europe/Istanbul",
    "subscription": {
        "plan": "business",
        "status": "active",
        "started_at": NOW - timedelta(days=200),
        "next_billing_at": NOW + timedelta(days=22),
    },
    "is_active": True,
    "created_at": NOW - timedelta(days=200),
    "updated_at": NOW,
}

vet_services = [
    {
        "_id": vet_svc_muayene, "business_id": vet_id,
        "name": "Genel Muayene", "description": "Genel sağlık kontrolü ve muayene.",
        "category": "Muayene", "duration_minutes": 30, "price": _d(500), "currency": "TRY",
        "staff_ids": [vet_staff_can, vet_staff_selin],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 10,
        "is_active": True,
    },
    {
        "_id": vet_svc_asi, "business_id": vet_id,
        "name": "Karma Aşı", "description": "Yıllık karma aşı uygulaması.",
        "category": "Aşı", "duration_minutes": 20, "price": _d(750), "currency": "TRY",
        "staff_ids": [vet_staff_can, vet_staff_selin],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
    {
        "_id": vet_svc_operasyon, "business_id": vet_id,
        "name": "Kısırlaştırma Operasyonu",
        "description": "Kedi/köpek kısırlaştırma operasyonu (sabah randevu).",
        "category": "Operasyon", "duration_minutes": 120, "price": _d(4500), "currency": "TRY",
        "staff_ids": [vet_staff_can],
        "requires_room": True, "buffer_before_minutes": 15, "buffer_after_minutes": 30,
        "is_active": True,
    },
    {
        "_id": vet_svc_kontrol, "business_id": vet_id,
        "name": "Kontrol Muayenesi", "description": "Önceki tedavi sonrası kontrol.",
        "category": "Kontrol", "duration_minutes": 15, "price": _d(200), "currency": "TRY",
        "staff_ids": [vet_staff_can, vet_staff_selin],
        "requires_room": True, "buffer_before_minutes": 0, "buffer_after_minutes": 5,
        "is_active": True,
    },
]

vet_staff = [
    {
        "_id": vet_staff_can, "business_id": vet_id,
        "name": "Vet. Hekim Can Vural", "role": "Veteriner Hekim (Sahip)",
        "phone": "+905553330001", "email": "can@patidostu.com",
        "photo_url": None,
        "bio": "Küçük cerrahi ve dahiliye uzmanı, 12 yıllık tecrübe.",
        "service_ids": [vet_svc_muayene, vet_svc_asi, vet_svc_operasyon, vet_svc_kontrol],
        "working_hours": _full_week("09:00", "19:00", closed_days=["sunday"],
                                    breaks=[{"start": "13:00", "end": "14:00"}]),
        "time_off": [],
        "commission_rate": 0.0,
        "is_active": True,
        "created_at": NOW - timedelta(days=200),
    },
    {
        "_id": vet_staff_selin, "business_id": vet_id,
        "name": "Vet. Hekim Selin Yıldız", "role": "Veteriner Hekim",
        "phone": "+905553330002", "email": "selin@patidostu.com",
        "photo_url": None, "bio": "Kuş ve egzotik hayvan ilgisi.",
        "service_ids": [vet_svc_muayene, vet_svc_asi, vet_svc_kontrol],
        "working_hours": _full_week("11:00", "19:00", closed_days=["sunday", "monday"]),
        "time_off": [],
        "commission_rate": 0.40,
        "is_active": True,
        "created_at": NOW - timedelta(days=150),
    },
]


cust_ali_id = ObjectId()
cust_ali = {
    "_id": cust_ali_id,
    "business_id": berber_id,
    "name": "Ali Yıldırım",
    "phone": "+905309998877",
    "whatsapp_id": "905309998877",
    "instagram_username": None,
    "instagram_user_id": None,
    "email": None,
    "birthdate": datetime(1992, 6, 15).date().isoformat(),
    "wedding_anniversary": None,
    "notes": "Yan saçları kısa, üst uzun ister.",
    "tags": ["sadık_musteri"],
    "preferred_staff_id": berber_staff_mehmet,
    "total_appointments": 7,
    "last_visit": NOW - timedelta(days=22),
    "no_show_count": 0,
    "cancel_count": 1,
    "is_blocked": False,
    "blocked_at": None,
    "blocked_reason": None,
    "consent": {
        "marketing_sms": True,
        "kvkk_accepted_at": NOW - timedelta(days=180),
    },
    "created_at": NOW - timedelta(days=180),
}

cust_demir_id = ObjectId()
cust_demir = {
    "_id": cust_demir_id,
    "business_id": salon_id,
    "name": "Demir Akın",
    "phone": "+905307776655",
    "whatsapp_id": "905307776655",
    "instagram_username": None,
    "instagram_user_id": None,
    "email": None,
    "birthdate": None,
    "wedding_anniversary": datetime(2018, 9, 3).date().isoformat(),
    "notes": "Geçen 2 randevuya gelmedi.",
    "tags": ["risk"],
    "preferred_staff_id": None,
    "total_appointments": 4,
    "last_visit": NOW - timedelta(days=90),
    "no_show_count": 2,
    "cancel_count": 0,
    "is_blocked": True,
    "blocked_at": NOW - timedelta(days=30),
    "blocked_reason": "no_show_limit",
    "consent": {
        "marketing_sms": False,
        "kvkk_accepted_at": NOW - timedelta(days=200),
    },
    "created_at": NOW - timedelta(days=200),
}

apt_start = (NOW + timedelta(days=2)).replace(hour=14, minute=0, second=0, microsecond=0)
apt_end = apt_start + timedelta(minutes=50)
conv_id = ObjectId()
apt_id = ObjectId()

appointment_ali = {
    "_id": apt_id,
    "business_id": berber_id,
    "customer_id": cust_ali_id,
    "staff_id": berber_staff_mehmet,
    "room_id": None,
    "services": [
        {"service_id": berber_svc_komple, "name": "Saç + Sakal",
         "duration_minutes": 50, "price": _d(380)}
    ],
    "start_time": apt_start,
    "end_time": apt_end,
    "status": "confirmed",
    "source": "whatsapp",
    "total_price": _d(380),
    "payment_status": "unpaid",
    "notes": "Yandan kısa, üstten degrade.",
    "created_by": "ai",
    "conversation_id": conv_id,
    "reminders_sent": [],
    "cancelled_reason": None,
    "created_at": NOW - timedelta(hours=2),
    "updated_at": NOW - timedelta(hours=2),
}

conversation_ali = {
    "_id": conv_id,
    "business_id": berber_id,
    "customer_id": cust_ali_id,
    "channel": "whatsapp",
    "channel_thread_id": "905309998877",
    "state": "booked",
    "context": {
        "booked_appointment_id": str(apt_id),
    },
    "messages": [
        {"role": "user", "content": "Selam, yarın için randevu almak istiyorum.",
         "timestamp": NOW - timedelta(hours=2, minutes=10),
         "channel_msg_id": "wamid.AAA",
         "tool_name": None, "tool_args": None},
        {"role": "assistant",
         "content": "[interactive: flow CTA gönderildi]",
         "timestamp": NOW - timedelta(hours=2, minutes=9),
         "channel_msg_id": None,
         "tool_name": "send_booking_flow", "tool_args": None},
        {"role": "user", "content": "Sent",
         "timestamp": NOW - timedelta(hours=2, minutes=4),
         "channel_msg_id": "wamid.AAC",
         "tool_name": None,
         "tool_args": {"interactive_type": "nfm_reply"}},
        {"role": "assistant",
         "content": (
             "✅ Randevunuz onaylandı.\n"
             "• Saç + Sakal\n"
             f"• {apt_start.strftime('%d.%m.%Y %H:%M')}\n"
             "• Personel: Mehmet Kaya\n"
             "• Süre: 50 dk\n"
             "• Ücret: 380₺\n\n"
             "Görüşmek üzere!"
         ),
         "timestamp": NOW - timedelta(hours=2, minutes=3),
         "channel_msg_id": None,
         "tool_name": None, "tool_args": None},
    ],
    "last_active_at": NOW - timedelta(hours=2),
    "created_at": NOW - timedelta(hours=2, minutes=10),
    "closed_at": None,
}


def ensure_indexes(db):
    db.businesses.create_index("business_id", unique=True)
    db.businesses.create_index("business_type")
    db.businesses.create_index("contact.whatsapp_number", unique=True, sparse=True)
    db.businesses.create_index("channels.whatsapp.phone_number_id", sparse=True)
    db.businesses.create_index("channels.instagram.ig_user_id", sparse=True)

    db.staff.create_index([("business_id", ASCENDING), ("is_active", ASCENDING)])

    db.services.create_index([("business_id", ASCENDING), ("is_active", ASCENDING)])
    db.services.create_index([("business_id", ASCENDING), ("category", ASCENDING)])

    db.customers.create_index(
        [("business_id", ASCENDING), ("whatsapp_id", ASCENDING)],
        unique=True,
        partialFilterExpression={"whatsapp_id": {"$type": "string"}},
    )
    db.customers.create_index(
        [("business_id", ASCENDING), ("instagram_user_id", ASCENDING)],
        unique=True,
        partialFilterExpression={"instagram_user_id": {"$type": "string"}},
    )
    db.customers.create_index([("business_id", ASCENDING), ("phone", ASCENDING)])
    db.customers.create_index([("business_id", ASCENDING), ("is_blocked", ASCENDING)])

    db.appointments.create_index([
        ("business_id", ASCENDING), ("staff_id", ASCENDING), ("start_time", ASCENDING),
    ])
    db.appointments.create_index([
        ("business_id", ASCENDING), ("status", ASCENDING), ("start_time", ASCENDING),
    ])
    db.appointments.create_index([("customer_id", ASCENDING), ("start_time", -1)])
    db.appointments.create_index([("status", ASCENDING), ("start_time", ASCENDING)])

    db.conversations.create_index(
        [("business_id", ASCENDING), ("channel", ASCENDING), ("channel_thread_id", ASCENDING)],
        unique=True,
    )
    db.conversations.create_index([
        ("business_id", ASCENDING), ("state", ASCENDING), ("last_active_at", -1),
    ])


def seed():
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]

    print(f"[seed] Veritabanı sıfırlanıyor: {DB_NAME}")
    for coll in ["businesses", "staff", "services", "customers", "appointments", "conversations"]:
        db[coll].drop()

    db.businesses.insert_many([berber_business, salon_business, vet_business])
    db.staff.insert_many(berber_staff + salon_staff + vet_staff)
    db.services.insert_many(berber_services + salon_services + vet_services)
    db.customers.insert_many([cust_ali, cust_demir])
    db.appointments.insert_one(appointment_ali)
    db.conversations.insert_one(conversation_ali)

    ensure_indexes(db)

    print(f"[seed] businesses     : {db.businesses.count_documents({})}")
    print(f"[seed] staff          : {db.staff.count_documents({})}")
    print(f"[seed] services       : {db.services.count_documents({})}")
    print(f"[seed] customers      : {db.customers.count_documents({})}")
    print(f"[seed] appointments   : {db.appointments.count_documents({})}")
    print(f"[seed] conversations  : {db.conversations.count_documents({})}")
    print("[seed] OK")


if __name__ == "__main__":
    seed()
