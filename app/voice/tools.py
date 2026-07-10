"""
FAZ 3 - Sesli Asistan (Voice Agent) için Veritabanı ve Randevu Araçları (Tools).

Bu modül, LLM'in sesli konuşma sırasında çağırabileceği randevu sorgulama
ve randevu oluşturma fonksiyonlarını barındırır.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

from pydantic import BaseModel, Field

from app.core.availability import find_first_available_slots
from app.core.booking import create_appointment
from app.core.db import get_db

logger = logging.getLogger(__name__)


class AvailabilityToolInput(BaseModel):
    """Müsaitlik kontrol aracı parametre modeli."""

    business_slug: str = Field(..., description="İşletmenin benzersiz kısa kodu")
    service_name: str = Field(..., description="Sorgulanan hizmetin adı")
    target_date: str = Field(..., description="Sorgulanan tarih (YYYY-MM-DD)")


class AppointmentCreateToolInput(BaseModel):
    """Randevu oluşturma aracı parametre modeli."""

    business_slug: str = Field(..., description="İşletmenin benzersiz kısa kodu")
    service_name: str = Field(..., description="Hizmet adı")
    staff_name: str = Field(..., description="Personel adı")
    customer_phone: str = Field(..., description="Müşteri telefon numarası")
    customer_name: str = Field(..., description="Müşteri adı")
    start_time_local: str = Field(..., description="Randevu başlangıç saati (YYYY-MM-DD HH:MM)")


class VoiceToolExecutor:
    """Sesli asistanın veritabanı araçlarını çalıştıran yönetici sınıf."""

    @staticmethod
    async def get_services(business_slug: str) -> list[str]:
        """İşletmeye ait aktif hizmet/kategori isimlerini veritabanından getirir."""
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return []
        services = await db.services.find({"business_id": business["_id"]}).to_list(100)
        return [str(s["name"]) for s in services if "name" in s]

    @staticmethod
    async def check_availability(
        business_slug: str,
        service_name: str,
        target_date_str: str,
        staff_name: str | None = None,
    ) -> dict[str, Any]:
        """Belirtilen usta ve gün için müsait randevu saatlerini döndürür."""
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return {"error": "business_not_found"}

        service = await db.services.find_one({
            "business_id": business["_id"],
            "name": {"$regex": f"^{service_name}$", "$options": "i"},
        })
        if not service:
            return {"error": "service_not_found"}

        staff_query: dict[str, Any] = {
            "business_id": business["_id"],
            "service_ids": service["_id"],
        }
        if staff_name:
            staff_query["name"] = {"$regex": f"^{staff_name}$", "$options": "i"}

        staff = await db.staff.find_one(staff_query)
        if not staff:
            return {"error": "no_staff_for_service"}

        try:
            target_date = date.fromisoformat(target_date_str)
        except ValueError:
            return {"error": "invalid_date_format"}

        slots = await find_first_available_slots(
            db=db,
            business=business,
            service=service,
            staff=staff,
            start_date=target_date,
            days_to_scan=1,
            max_slots=5,
            step_minutes=60,
        )
        slot_strs = []
        for s in slots:
            from datetime import timedelta
            local_s = s + timedelta(hours=3)
            slot_strs.append(local_s.strftime("%H:%M"))

        return {
            "status": "success",
            "date": target_date_str,
            "staff": staff.get("name", ""),
            "available_slots": slot_strs,
        }

    @staticmethod
    async def book_appointment(
        business_slug: str,
        service_name: str,
        staff_name: str,
        customer_phone: str,
        customer_name: str,
        start_time_local: str,
    ) -> dict[str, Any]:
        """Müşteri için yeni randevu oluşturur."""
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return {"error": "business_not_found"}

        service = await db.services.find_one({
            "business_id": business["_id"],
            "name": {"$regex": f"^{service_name}$", "$options": "i"},
        })
        if not service:
            return {"error": "service_not_found"}

        staff = await db.staff.find_one({
            "business_id": business["_id"],
            "name": {"$regex": f"^{staff_name}$", "$options": "i"},
        })
        if not staff:
            return {"error": "staff_not_found"}

        customer = await db.customers.find_one({
            "business_id": business["_id"],
            "phone": customer_phone,
        })
        if not customer:
            res = await db.customers.insert_one({
                "business_id": business["_id"],
                "phone": customer_phone,
                "name": customer_name,
            })
            customer = await db.customers.find_one({"_id": res.inserted_id})
        if not customer:
            return {"error": "customer_not_found"}

        conversation = await db.conversations.find_one({
            "business_id": business["_id"],
            "channel": "voice",
        })
        if not conversation:
            res = await db.conversations.insert_one({
                "business_id": business["_id"],
                "channel": "voice",
            })
            conversation = await db.conversations.find_one({"_id": res.inserted_id})
        if not conversation:
            return {"error": "conversation_not_found"}

        result = await create_appointment(
            db=db,
            business=business,
            customer=customer,
            conversation=conversation,
            service=service,
            staff=staff,
            start_local=start_time_local,
            source="voice",
            created_by="voice_agent",
        )
        return result
