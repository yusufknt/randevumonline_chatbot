from __future__ import annotations

from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import Annotated, Any, Literal

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Geçersiz ObjectId")


class BusinessType(str, Enum):
    BERBER = "berber"
    KUAFOR = "kuafor"
    GUZELLIK_SALONU = "guzellik_salonu"
    MASAJ_SPA = "masaj_spa"
    ESTETIK_KLINIK = "estetik_klinik"
    SPOR_SALONU = "spor_salonu"
    YOGA_PILATES = "yoga_pilates"
    DOVME_PIERCING = "dovme_piercing"
    KLINIK = "klinik"
    VETERINER = "veteriner"
    PSIKOLOG = "psikolog"
    DIYETISYEN = "diyetisyen"
    OZEL_DERS = "ozel_ders"
    OTO_SERVIS = "oto_servis"
    FOTOGRAF_STUDYOSU = "fotograf_studyosu"
    AVUKAT = "avukat"
    OTO_YIKAMA = "oto_yikama"


class Weekday(str, Enum):
    MON = "monday"
    TUE = "tuesday"
    WED = "wednesday"
    THU = "thursday"
    FRI = "friday"
    SAT = "saturday"
    SUN = "sunday"


class Channel(str, Enum):
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    WEB = "web"
    MANUAL = "manual"


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PARTIAL = "partial"
    PAID = "paid"


class ConversationState(str, Enum):
    GREETING = "greeting"
    SELECTING_SERVICE = "selecting_service"
    SELECTING_STAFF = "selecting_staff"
    SELECTING_TIME = "selecting_time"
    COLLECTING_CUSTOMER_INFO = "collecting_customer_info"
    CONFIRMING = "confirming"
    BOOKED = "booked"
    HUMAN_HANDOFF = "human_handoff"
    CLOSED = "closed"


class WorkingHours(BaseModel):
    day: Weekday
    open: str = Field(pattern=r"^\d{2}:\d{2}$")
    close: str = Field(pattern=r"^\d{2}:\d{2}$")
    closed: bool = False
    breaks: list[dict[str, str]] = []


class SpecialDay(BaseModel):
    date: date
    closed: bool = False
    open: str | None = None
    close: str | None = None
    reason: str | None = None


class GeoPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]   # [lng, lat]


class Contact(BaseModel):
    phone: str
    whatsapp_number: str
    instagram_username: str | None = None
    email: EmailStr | None = None
    address: str
    location: GeoPoint | None = None
    booking_url: str | None = None


class Socials(BaseModel):
    instagram: str | None = None
    facebook: str | None = None
    twitter: str | None = None
    website: str | None = None


class WhatsAppChannelConfig(BaseModel):
    enabled: bool = False
    phone_number_id: str | None = None     # WA Cloud API
    business_account_id: str | None = None
    access_token_ref: str | None = None    # vault path, örn "vault://secrets/wa/<biz_id>"
    verify_token_ref: str | None = None
    flow_id: str | None = None             # WhatsApp Flow ID (randevu formu)


class InstagramChannelConfig(BaseModel):
    enabled: bool = False
    ig_user_id: str | None = None
    page_id: str | None = None
    access_token_ref: str | None = None


class ChannelConfigs(BaseModel):
    whatsapp: WhatsAppChannelConfig = WhatsAppChannelConfig()
    instagram: InstagramChannelConfig = InstagramChannelConfig()


class AISettings(BaseModel):
    model_name: str = "llama3.1:8b-instruct-q4"
    persona: str = "Yardımsever ve kısa yanıt veren randevu asistanı."
    language: str = "tr-TR"
    welcome_message: str
    fallback_message: str = "Sizi bir personelimize aktarıyorum."
    confirmation_required: bool = True
    booking_buffer_minutes: int = 30
    max_advance_days: int = 60
    online_slot_step_minutes: int = 30
    admin_calendar_step_minutes: int = 15
    calendar_color_coding: bool = True
    auto_add_to_calendar: bool = False
    customer_cancel_window_minutes: int = 60
    cancel_block_limit: int = 5
    no_show_block_limit: int = 2
    online_booking_who: Literal["nobody", "registered_only", "everyone"] = "registered_only"
    online_booking_mode: Literal["standard", "showcase"] = "standard"
    reminder_minutes_before: int = 60
    quiet_hours: dict[str, str] | None = None


class Subscription(BaseModel):
    plan: Literal["individual", "business"]
    status: Literal["active", "trial", "cancelled", "past_due"] = "active"
    started_at: datetime
    next_billing_at: datetime | None = None


class Room(BaseModel):
    room_id: str
    name: str
    capacity: int = 1
    notes: str | None = None


class Business(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    business_id: str                   # slug, örn "berber_mehmet_kutahya"
    name: str
    business_type: BusinessType
    owner: dict                        # {name, phone, email}
    contact: Contact
    socials: Socials = Socials()
    channels: ChannelConfigs = ChannelConfigs()
    ai_settings: AISettings
    working_hours: list[WorkingHours]
    special_days: list[SpecialDay] = []
    rooms: list[Room] = []
    timezone: str = "Europe/Istanbul"
    subscription: Subscription
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


class Staff(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    business_id: PyObjectId
    name: str
    role: str
    phone: str | None = None
    email: EmailStr | None = None
    photo_url: str | None = None
    bio: str | None = None
    service_ids: list[PyObjectId] = []
    working_hours: list[WorkingHours] = []
    time_off: list[dict] = []
    commission_rate: float = 0.0
    is_active: bool = True
    created_at: datetime


class Service(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    business_id: PyObjectId
    name: str
    description: str | None = None
    category: str | None = None
    duration_minutes: int
    price: Decimal
    price_max: Decimal | None = None  # aralıklı fiyat için üst sınır; None ise tek fiyat
    currency: str = "TRY"
    staff_ids: list[PyObjectId] = []
    requires_room: bool = False
    buffer_before_minutes: int = 0
    buffer_after_minutes: int = 0
    is_active: bool = True


class Customer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    business_id: PyObjectId
    name: str | None = None
    phone: str | None = None  # E.164 "+905551234567"
    whatsapp_id: str | None = None
    instagram_username: str | None = None
    instagram_user_id: str | None = None
    email: EmailStr | None = None
    birthdate: date | None = None
    wedding_anniversary: date | None = None
    notes: str | None = None
    tags: list[str] = []
    preferred_staff_id: PyObjectId | None = None
    total_appointments: int = 0
    last_visit: datetime | None = None
    no_show_count: int = 0
    cancel_count: int = 0
    is_blocked: bool = False
    blocked_at: datetime | None = None
    blocked_reason: str | None = None
    consent: dict = Field(default_factory=lambda: {
        "marketing_sms": False,
        "kvkk_accepted_at": None,
    })
    created_at: datetime


class AppointmentService(BaseModel):
    service_id: PyObjectId
    name: str
    duration_minutes: int
    price: Decimal


class Appointment(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    business_id: PyObjectId
    customer_id: PyObjectId
    staff_id: PyObjectId
    room_id: str | None = None
    services: list[AppointmentService]
    start_time: datetime  # UTC
    end_time: datetime    # UTC
    status: AppointmentStatus = AppointmentStatus.PENDING
    source: Channel
    total_price: Decimal
    payment_status: PaymentStatus = PaymentStatus.UNPAID
    notes: str | None = None
    created_by: Literal["ai", "staff", "customer"] = "ai"
    conversation_id: PyObjectId | None = None
    reminders_sent: list[dict] = []
    cancelled_reason: str | None = None
    created_at: datetime
    updated_at: datetime


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant", "system", "tool"]
    content: str
    timestamp: datetime
    channel_msg_id: str | None = None
    tool_name: str | None = None
    tool_args: dict | None = None


class Conversation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    id: PyObjectId | None = Field(default=None, alias="_id")
    business_id: PyObjectId
    customer_id: PyObjectId | None = None
    channel: Channel
    channel_thread_id: str
    state: ConversationState = ConversationState.GREETING
    context: dict = Field(default_factory=dict)
    messages: list[ConversationMessage] = []
    last_active_at: datetime
    created_at: datetime
    closed_at: datetime | None = None


# ---------- Önerilen MongoDB indeksleri ----------
# businesses     : business_id (unique), business_type, contact.whatsapp_number (unique)
# staff          : (business_id, is_active)
# services       : (business_id, is_active)
# customers      : (business_id, whatsapp_id) unique sparse,
#                  (business_id, instagram_user_id) unique sparse,
#                  (business_id, phone)
# appointments   : (business_id, staff_id, start_time),
#                  (business_id, status, start_time),
#                  (customer_id, start_time)
# conversations  : (business_id, channel, channel_thread_id) unique,
#                  (business_id, state, last_active_at)
