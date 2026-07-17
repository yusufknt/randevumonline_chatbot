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
    async def get_business_info(business_slug: str) -> dict[str, Any] | None:
        """İşletmenin temel bilgilerini veritabanından getirir."""
        db = get_db()
        return await db.businesses.find_one({"business_id": business_slug})

    @staticmethod
    async def get_staff(business_slug: str) -> list[str]:
        """İşletmeye ait aktif personelleri (ustaları) veritabanından getirir."""
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return []
        staff_members = await db.staff.find({"business_id": business["_id"]}).to_list(100)
        return [str(s["name"]) for s in staff_members if "name" in s]

    @staticmethod
    async def get_services(business_slug: str, staff_name: str | None = None, return_detailed_string: bool = False) -> list[str] | str:
        """İşletmeye ait aktif hizmet/kategori isimlerini veritabanından getirir."""
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return [] if not return_detailed_string else ""
            
        services = await db.services.find({"business_id": business["_id"]}).to_list(100)
        staffs = await db.staff.find({"business_id": business["_id"]}).to_list(100)
        
        # Sadece belirli bir personelin hizmetlerini istiyorsak
        if staff_name:
            staff_doc = None
            first_name = staff_name.split()[0].lower()
            for stf in staffs:
                if first_name in stf["name"].lower():
                    staff_doc = stf
                    break
            
            if staff_doc and "service_ids" in staff_doc:
                staff_service_ids = [str(sid) for sid in staff_doc["service_ids"]]
                filtered_services = [str(s["name"]) for s in services if "name" in s and str(s["_id"]) in staff_service_ids]
                return filtered_services if filtered_services else [str(s["name"]) for s in services if "name" in s]
                
        # Detaylı bir string isteniyorsa (System Prompt için: Usta1: x, y | Usta2: z, w)
        if return_detailed_string:
            staff_mapping = []
            for stf in staffs:
                stf_name = stf["name"].split()[0]
                if "service_ids" in stf:
                    s_ids = [str(sid) for sid in stf["service_ids"]]
                    s_names = [str(s["name"]) for s in services if str(s["_id"]) in s_ids]
                    if s_names:
                        staff_mapping.append(f"{stf_name} ustanın yaptığı işlemler: {', '.join(s_names)}")
            if staff_mapping:
                return " | ".join(staff_mapping)
            else:
                return ", ".join([str(s["name"]) for s in services if "name" in s])
                
        return [str(s["name"]) for s in services if "name" in s]

    @staticmethod
    async def check_availability(
        business_slug: str,
        service_name: str | None,
        target_date_str: str,
        staff_name: str | None = None,
    ) -> dict[str, Any]:
        """Belirtilen usta ve gün için müsait randevu saatlerini döndürür."""
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return {"error": "business_not_found"}

        import difflib

        # 1. Service eşleşmesi (Fuzzy Search) - Opsiyonel
        service = None
        if service_name and service_name.lower() != "belirsiz":
            services = await db.services.find({"business_id": business["_id"]}).to_list(100)
            if services:
                service_names = [s["name"] for s in services]
                matches = difflib.get_close_matches(service_name, service_names, n=1, cutoff=0.3)
                if matches:
                    service = next(s for s in services if s["name"] == matches[0])
                    
            if not service:
                return {"error": "service_not_found"}

        staff_query: dict[str, Any] = {
            "business_id": business["_id"],
        }
        if service:
            staff_query["service_ids"] = service["_id"]
        
        # 2. Personel eşleşmesi (Fuzzy Search)
        staff = None
        if staff_name:
            staffs = await db.staff.find(staff_query).to_list(100)
            if staffs:
                first_name = staff_name.split()[0].lower()
                for stf in staffs:
                    if first_name in stf["name"].lower():
                        staff = stf
                        break
        else:
            # Usta belirtilmemişse ilkini seç
            staff = await db.staff.find_one(staff_query)

        if not staff:
            return {"error": "staff_not_found"}
            
        # Hizmet bilinmiyorsa, süre hesaplaması için standart 30 dk varsay
        if not service:
            service = {"_id": "dummy", "duration_minutes": 30}

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

        import difflib

        # 1. Service eşleşmesi (Fuzzy Search)
        services = await db.services.find({"business_id": business["_id"]}).to_list(100)
        service = None
        if services:
            # En yakın eşleşmeyi bul
            service_names = [s["name"] for s in services]
            matches = difflib.get_close_matches(service_name, service_names, n=1, cutoff=0.3)
            if matches:
                service = next(s for s in services if s["name"] == matches[0])
                
        if not service:
            return {"error": "service_not_found"}

        # 2. Personel eşleşmesi (Fuzzy Search)
        staffs = await db.staff.find({"business_id": business["_id"]}).to_list(100)
        staff = None
        if staffs:
            # Sadece ilk ismiyle arama yap ("Yusuf Usta" -> "Yusuf")
            first_name = staff_name.split()[0].lower()
            for stf in staffs:
                if first_name in stf["name"].lower():
                    staff = stf
                    break
                    
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

        try:
            result = await create_appointment(
                db=db,
                business=business,
                customer=customer,
                conversation=conversation,
                service=service,
                staff=staff,
                start_local=start_time_local,
                source="voice",
                created_by="voice_assistant",
            )
            logger.info("📅 Randevu API Çağrısı Başarılı: %s", result)
            return result
        except Exception as e:
            logger.error("❌ Randevu API Çağrısı Başarısız: %s", str(e))
            return {"error": "api_error", "details": str(e)}

    @staticmethod
    async def cancel_appointment(appointment_id: str) -> bool:
        db = get_db()
        from app.core.booking import cancel_appointment
        return await cancel_appointment(db, appointment_id, reason="voice_assistant_cancelled")

    @staticmethod
    async def reschedule_appointment(
        business_slug: str,
        appointment_id: str,
        new_start_local: str | None = None,
        new_service_name: str | None = None,
        new_staff_name: str | None = None
    ) -> dict[str, Any]:
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return {"error": "business_not_found"}
            
        import difflib
        
        # 1. Service eşleşmesi
        new_service = None
        if new_service_name and new_service_name != "-":
            services = await db.services.find({"business_id": business["_id"]}).to_list(100)
            if services:
                service_names = [s["name"] for s in services]
                matches = difflib.get_close_matches(new_service_name, service_names, n=1, cutoff=0.3)
                if matches:
                    new_service = next(s for s in services if s["name"] == matches[0])
            if not new_service:
                return {"error": "service_not_found"}

        # 2. Personel eşleşmesi
        new_staff = None
        if new_staff_name and new_staff_name != "-":
            staffs = await db.staff.find({"business_id": business["_id"]}).to_list(100)
            if staffs:
                first_name = new_staff_name.split()[0].lower()
                for stf in staffs:
                    if first_name in stf["name"].lower():
                        new_staff = stf
                        break
            if not new_staff:
                return {"error": "staff_not_found"}
                
        # Zaman '-' gelmişse None yap
        if new_start_local == "-":
            new_start_local = None

        from app.core.booking import reschedule_appointment
        return await reschedule_appointment(db, appointment_id, new_start_local, business, new_service, new_staff)

    @staticmethod
    async def get_customer_appointments(business_slug: str, customer_phone: str) -> list[dict[str, Any]]:
        db = get_db()
        business = await db.businesses.find_one({"business_id": business_slug})
        if not business:
            return []
            
        customer = await db.customers.find_one({"business_id": business["_id"], "phone": customer_phone})
        if not customer:
            return []
            
        # Gelecekteki aktif randevuları getir
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        
        cursor = db.appointments.find({
            "business_id": business["_id"],
            "customer_id": customer["_id"],
            "status": {"$in": ["pending", "confirmed"]},
            "start_time": {"$gt": now}
        }).sort("start_time", 1)
        
        apts = []
        async for a in cursor:
            # Usta ve hizmet ismini bul
            staff = await db.staff.find_one({"_id": a["staff_id"]})
            staff_name = staff["name"] if staff else "Bilinmiyor"
            
            service_name = a["services"][0]["name"] if a.get("services") else "Bilinmiyor"
            
            from zoneinfo import ZoneInfo
            tz = ZoneInfo(business.get("timezone", "Europe/Istanbul"))
            start_local = a["start_time"].astimezone(tz)
            
            apts.append({
                "id": str(a["_id"]),
                "staff": staff_name,
                "service": service_name,
                "date": start_local.strftime("%Y-%m-%d %H:%M")
            })
            
        return apts
