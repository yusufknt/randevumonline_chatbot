from __future__ import annotations

import json

from app.core.config import get_settings


def build_flow_json() -> str:
    s = get_settings()
    flow = {
        "version": s.wa_flow_json_version,
        "data_api_version": "4.0",  # data_exchange ve refresh_on_back için zorunlu
        "routing_model": {
            "AD_SOYAD": ["SERVICE"],
            "SERVICE":  ["STAFF", "DAY"],
            "STAFF":    ["DAY"],
            "DAY":      ["TIME"],
            "TIME":     ["CONFIRM"],
            "CONFIRM":  [],
        },
        "screens": [
            _ad_soyad_screen(),
            _service_screen(),
            _staff_screen(),
            _day_screen(),
            _time_screen(),
            _confirm_screen(),
        ],
    }
    return json.dumps(flow, ensure_ascii=False)


# ---------- Ekranlar ----------

def _ad_soyad_screen() -> dict:
    return {
        "id": "AD_SOYAD",
        "title": "Adınız",
        "data": {},
        "layout": {
            "type": "SingleColumnLayout",
            "children": [
                {"type": "TextHeading", "text": "Randevu için kişisel bilgileriniz"},
                {"type": "TextBody",
                 "text": "Lütfen adınızı ve soyadınızı yazın."},
                {
                    "type": "Form", "name": "form_ad_soyad",
                    "children": [
                        # min-chars/max-chars: Meta validator literal string reddeder, int veya ${data.x} gerekir
                        {"type": "TextInput", "name": "first_name",
                         "label": "Ad", "input-type": "text",
                         "required": True, "min-chars": 2, "max-chars": 40},
                        {"type": "TextInput", "name": "last_name",
                         "label": "Soyad", "input-type": "text",
                         "required": True, "min-chars": 2, "max-chars": 40},
                        {"type": "Footer", "label": "Devam",
                         "on-click-action": {
                             "name": "data_exchange",
                             "payload": {
                                 "first_name": "${form.first_name}",
                                 "last_name": "${form.last_name}",
                             },
                         }},
                    ],
                },
            ],
        },
    }


def _service_screen() -> dict:
    return {
        "id": "SERVICE",
        "title": "Hizmet",
        "data": {
            "first_name": {"type": "string", "__example__": "Taha"},
            "last_name":  {"type": "string", "__example__": "Demir"},
            "services": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":    {"type": "string"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                    },
                },
                "__example__": [
                    {"id": "x", "title": "Saç Kesimi", "description": "30 dk · 250 TRY"},
                ],
            },
        },
        "layout": {
            "type": "SingleColumnLayout",
            "children": [
                {"type": "TextHeading", "text": "Hizmet seçin"},
                {
                    "type": "Form", "name": "form_service",
                    "children": [
                        {"type": "RadioButtonsGroup", "name": "service_id",
                         "label": "Hizmet", "required": True,
                         "data-source": "${data.services}"},
                        {"type": "Footer", "label": "Devam",
                         "on-click-action": {
                             "name": "data_exchange",
                             "payload": {
                                 "first_name": "${data.first_name}",
                                 "last_name":  "${data.last_name}",
                                 "service_id": "${form.service_id}",
                             },
                         }},
                    ],
                },
            ],
        },
    }


def _staff_screen() -> dict:
    return {
        "id": "STAFF",
        "title": "Personel",
        "refresh_on_back": True,
        "data": {
            "first_name": {"type": "string", "__example__": "Taha"},
            "last_name":  {"type": "string", "__example__": "Demir"},
            "service_id": {"type": "string", "__example__": "x"},
            "service_name": {"type": "string", "__example__": "Saç Kesimi"},
            "staff_options": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":    {"type": "string"},  # ObjectId hex veya "any"
                        "title": {"type": "string"},
                    },
                },
                "__example__": [{"id": "any", "title": "Fark etmez"}],
            },
        },
        "layout": {
            "type": "SingleColumnLayout",
            "children": [
                {"type": "TextHeading", "text": "Personel seçin"},
                {"type": "TextCaption", "text": "${data.service_name}"},
                {
                    "type": "Form", "name": "form_staff",
                    "children": [
                        # Form değeri array<string> döner; backend _route() içinde tek string'e normalize edilir
                        {"type": "ChipsSelector", "name": "staff_id",
                         "label": "Personel", "required": True,
                         "max-selected-items": 1,
                         "data-source": "${data.staff_options}"},
                        {"type": "Footer", "label": "Devam",
                         "on-click-action": {
                             "name": "data_exchange",
                             "payload": {
                                 "first_name": "${data.first_name}",
                                 "last_name":  "${data.last_name}",
                                 "service_id": "${data.service_id}",
                                 "staff_id":   "${form.staff_id}",
                             },
                         }},
                    ],
                },
            ],
        },
    }


def _day_screen() -> dict:
    return {
        "id": "DAY",
        "title": "Gün",
        "refresh_on_back": True,
        "data": {
            "first_name": {"type": "string", "__example__": "Taha"},
            "last_name":  {"type": "string", "__example__": "Demir"},
            "service_id": {"type": "string", "__example__": "x"},
            "service_name": {"type": "string", "__example__": "Saç Kesimi"},
            "staff_id":   {"type": "string", "__example__": "any"},
            "staff_name": {"type": "string", "__example__": "Fark etmez"},
            # Birden fazla dinamik ref tek string'de geçersiz; backend
            # `caption` alanını concat ile hazırlar.
            "caption": {"type": "string", "__example__": "Saç Kesimi · Fark etmez"},
            "days": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":    {"type": "string"},
                        "title": {"type": "string"},
                    },
                },
                "__example__": [{"id": "2026-05-07", "title": "Çar 07 May"}],
            },
        },
        "layout": {
            "type": "SingleColumnLayout",
            "children": [
                {"type": "TextHeading", "text": "Gün seçin"},
                {"type": "TextCaption", "text": "${data.caption}"},
                {
                    "type": "Form", "name": "form_day",
                    "children": [
                        {"type": "RadioButtonsGroup", "name": "day",
                         "label": "Gün", "required": True,
                         "data-source": "${data.days}"},
                        {"type": "Footer", "label": "Devam",
                         "on-click-action": {
                             "name": "data_exchange",
                             "payload": {
                                 "first_name": "${data.first_name}",
                                 "last_name":  "${data.last_name}",
                                 "service_id": "${data.service_id}",
                                 "staff_id":   "${data.staff_id}",
                                 "day":        "${form.day}",
                             },
                         }},
                    ],
                },
            ],
        },
    }


def _time_screen() -> dict:
    return {
        "id": "TIME",
        "title": "Saat",
        "refresh_on_back": True,
        "data": {
            "first_name": {"type": "string", "__example__": "Taha"},
            "last_name":  {"type": "string", "__example__": "Demir"},
            "service_id": {"type": "string", "__example__": "x"},
            "service_name": {"type": "string", "__example__": "Saç Kesimi"},
            "staff_id":   {"type": "string", "__example__": "any"},
            "staff_name": {"type": "string", "__example__": "Fark etmez"},
            "day":        {"type": "string", "__example__": "2026-05-07"},
            "day_label":  {"type": "string", "__example__": "Çar 07 May"},
            "caption": {"type": "string",
                        "__example__": "Saç Kesimi · Fark etmez · Çar 07 May"},
            "times": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":    {"type": "string"},
                        "title": {"type": "string"},
                    },
                },
                "__example__": [{"id": "14:00", "title": "14:00"}],
            },
        },
        "layout": {
            "type": "SingleColumnLayout",
            "children": [
                {"type": "TextHeading", "text": "Saat seçin"},
                {"type": "TextCaption", "text": "${data.caption}"},
                {
                    "type": "Form", "name": "form_time",
                    "children": [
                        # RadioButtonsGroup max 20 öğe
                        {"type": "RadioButtonsGroup", "name": "time",
                         "label": "Saat", "required": True,
                         "data-source": "${data.times}"},
                        {"type": "Footer", "label": "Devam",
                         "on-click-action": {
                             "name": "data_exchange",
                             "payload": {
                                 "first_name": "${data.first_name}",
                                 "last_name":  "${data.last_name}",
                                 "service_id": "${data.service_id}",
                                 "staff_id":   "${data.staff_id}",
                                 "day":        "${data.day}",
                                 "time":       "${form.time}",
                             },
                         }},
                    ],
                },
            ],
        },
    }


def _confirm_screen() -> dict:
    return {
        "id": "CONFIRM",
        "title": "Onay",
        "terminal": True,
        "success": True,
        "data": {
            "first_name": {"type": "string", "__example__": "Taha"},
            "last_name":  {"type": "string", "__example__": "Demir"},
            "full_name":  {"type": "string", "__example__": "Taha Demir"},
            "service_id": {"type": "string", "__example__": "x"},
            "service_name": {"type": "string", "__example__": "Saç Kesimi"},
            "staff_id":   {"type": "string", "__example__": "any"},
            "staff_name": {"type": "string", "__example__": "Fark etmez"},
            "day":        {"type": "string", "__example__": "2026-05-07"},
            "day_label":  {"type": "string", "__example__": "Çar 07 May"},
            "time":       {"type": "string", "__example__": "14:00"},
            "end_time":   {"type": "string", "__example__": "14:45"},
            "time_range": {"type": "string", "__example__": "14:00 – 14:45"},
            "duration_minutes": {"type": "number", "__example__": 45},
            "notes":      {"type": "string", "__example__": ""},
        },
        "layout": {
            "type": "SingleColumnLayout",
            "children": [
                {"type": "TextHeading", "text": "Randevu Özetiniz"},
                {"type": "TextBody", "text": "Ad Soyad: ${data.full_name}"},
                {"type": "TextBody", "text": "Hizmet: ${data.service_name}"},
                {"type": "TextBody", "text": "Personel: ${data.staff_name}"},
                {"type": "TextBody", "text": "Tarih: ${data.day_label}"},
                {"type": "TextBody", "text": "Saat: ${data.time_range}"},
                {"type": "TextCaption",
                 "text": "Tahmini süre: ${data.duration_minutes} dk"},
                {
                    "type": "Form", "name": "form_confirm",
                    # init-values Form düzeyinde: hata tekrarında kullanıcının notu korunur
                    "init-values": {"notes": "${data.notes}"},
                    "children": [
                        # label ≤ 20 karakter (Flow validator zorunluluğu)
                        {"type": "TextArea", "name": "notes",
                         "label": "Not (opsiyonel)",
                         "required": False, "max-length": 200},
                        {"type": "Footer", "label": "Randevuyu Onayla",
                         "on-click-action": {
                             "name": "data_exchange",
                             "payload": {
                                 "first_name":        "${data.first_name}",
                                 "last_name":         "${data.last_name}",
                                 "service_id":        "${data.service_id}",
                                 "service_name":      "${data.service_name}",
                                 "staff_id":          "${data.staff_id}",
                                 "staff_name":        "${data.staff_name}",
                                 "day":               "${data.day}",
                                 "day_label":         "${data.day_label}",
                                 "time":              "${data.time}",
                                 "end_time":          "${data.end_time}",
                                 "time_range":        "${data.time_range}",
                                 "duration_minutes":  "${data.duration_minutes}",
                                 "notes":             "${form.notes}",
                             },
                         }},
                    ],
                },
            ],
        },
    }
