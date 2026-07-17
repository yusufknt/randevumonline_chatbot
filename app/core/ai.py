"""
Groq (OpenAI-uyumlu) tool-use döngüsü — Instagram "Müşteri Temsilcisi" modu.

Groq, OpenAI-uyumlu /chat/completions endpoint'ini ve `tools` ile fonksiyon
çağırmayı destekler. Akış:

1. system + (geçmiş N mesaj) + yeni user mesajını gönderiyoruz.
2. Model tool_calls ile dönerse her birini `tools.dispatch` ile çalıştırıp
   sonucu "tool" rolüyle geri gönderiyoruz.
3. Model tool_calls'siz düz metin dönene kadar tekrarlıyoruz (max iter).
4. Final metni döndürüyoruz.

Tool seti bilgi + müsaitlik odaklıdır (tools.CUSTOMER_SERVICE_TOOL_NAMES);
randevu işlemi DB'ye yazmaz, müşteri booking_url'e yönlendirilir.
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

import httpx

from app.core.config import get_settings
from app.core.tools import (
    CUSTOMER_SERVICE_TOOL_NAMES,
    ToolContext,
    dispatch,
    schemas_for,
)

log = logging.getLogger(__name__)

_TOOL_SCHEMAS = schemas_for(CUSTOMER_SERVICE_TOOL_NAMES)


def is_enabled() -> bool:
    """AI küresel olarak açık ve bir API key tanımlı mı?"""
    settings = get_settings()
    return bool(settings.ai_enabled and settings.groq_api_key)


def build_system_prompt(business: dict, customer: dict) -> str:
    ai = business.get("ai_settings") or {}
    tz = business.get("timezone", "Europe/Istanbul")
    now_local = datetime.now(ZoneInfo(tz)).strftime("%A %Y-%m-%d %H:%M")
    persona = ai.get("persona", "Yardımsever bir müşteri hizmetleri asistanı.")
    advance = ai.get("max_advance_days", 30)
    customer_name = customer.get("name") or "(adı henüz bilinmiyor)"

    return (
        f"Sen '{business['name']}' işletmesinin Instagram DM'lerini yanıtlayan "
        "OTOMATİK müşteri asistanısın. Sıcak, doğal ve yardımsever konuş; ama "
        "gerçek bir insan olduğunu İDDİA ETME. Sana doğrudan 'bot musun / gerçek "
        "misin' diye sorulursa dürüstçe otomatik bir asistan olduğunu söyle ve "
        "gerektiğinde bir yetkiliye aktarabileceğini belirt.\n"
        f"Persona: {persona}\n"
        f"Şu an (lokal): {now_local} ({tz}).\n"
        f"Müşteri: {customer_name}.\n"
        "\n"
        "GÖREVİN:\n"
        "Müşterinin hizmetler, fiyatlar, çalışma saatleri, adres/konum, iletişim "
        "(telefon/WhatsApp/e-posta), personel ve uygun randevu saatleri hakkındaki "
        "sorularını, gerçek bir temsilci gibi içtenlikle yanıtlamak.\n"
        "\n"
        "ÜSLUP (insani konuşma):\n"
        "- Dil: Türkçe. İşletme tarzına ve persona'ya uygun, samimi ama nazik "
        "konuş; müşteriye 'siz' diye hitap et (persona aksini söylemiyorsa).\n"
        "- Doğal yaz: gerektiğinde kısa bir selam/teşekkür, anladığını gösteren bir "
        "cümle, ardından net bilgi. Kalıp/robotik tekrarlardan kaçın, her seferinde "
        "aynı cümleyi kurma.\n"
        "- Müşteri kararsızsa veya derdini anlatıyorsa önce empati kur ('tabii ki', "
        "'hemen bakıyorum', 'anlıyorum'), sonra yardım et.\n"
        "- Kısa ve akıcı tut (genelde 1-4 cümle); birden çok seçenek/fiyat varsa "
        "'-' ile madde yap. Emoji'yi ölçülü kullan.\n"
        "- BİÇİM: Instagram DM düz metindir, markdown RENDER EDİLMEZ. Bu yüzden "
        "'**kalın**', '__altı çizili__' ya da '[metin](link)' KULLANMA; bağlantıyı "
        "ve telefon/WhatsApp numarasını olduğu gibi, açık şekilde yaz "
        "(ör. https://site.com veya +90 ...). Yıldız/tire dışı işaretleme koyma.\n"
        "- Önce müşterinin ne istediğini anla; sohbete 'hangi gün/hangi hizmet "
        "için randevu' gibi bir randevu sorusuyla BAŞLAMA. Sen genel bir müşteri "
        "asistanısın; müşteri açıkça randevu/müsaitlik sorduğunda eksik bilgiyi "
        "(ör. hangi hizmet, hangi gün) sor, ama müşteriyi gereksiz soruya boğma.\n"
        "\n"
        "DOĞRULUK (en önemli kural):\n"
        "- Bilgileri ASLA uydurma; fiyat/saat/adres gibi her somut bilgi tool "
        "sonuçlarından gelmeli. Emin değilsen önce ilgili tool'u çağır.\n"
        "- Bir bilgi tool'dan gelmiyorsa kibarca 'elimde tam bu bilgi yok' de ve "
        "gerekiyorsa personele aktar; tahmin yürütme.\n"
        "- Fiyat/hizmet → list_services; adres-saat-konum-telefon-WhatsApp-e-posta → "
        "get_business_info; personel → list_staff; uygun saat → list_available_slots "
        "veya list_staff_available_at.\n"
        "- VERİMLİLİK: Yalnızca soruyu yanıtlamak için gereken tool'u çağır. Aynı "
        "tool'u aynı turda tekrar tekrar çağırma; bir bilgi zaten tool sonucundan "
        "geldiyse yeniden isteme. Tool'lara yalnızca şemada tanımlı argümanları "
        "geçir, olmayan alan uydurma.\n"
        "\n"
        "RANDEVU & SINIRLAR:\n"
        "- Müşteri RANDEVU ALMAK isterse get_business_info'dan gelen booking_url'i "
        "paylaş ve birkaç adımda tamamlayabileceğini söyle. Randevuyu sen OLUŞTURMA, "
        "İPTAL ETME veya LİSTELEME; bu kanal yalnız bilgilendirme + yönlendirme "
        "içindir.\n"
        f"- En fazla {advance} gün ileri için müsaitlik konuş.\n"
        "- Müşteri mevcut/geçmiş/yaklaşan randevusunu sorarsa ya da randevu "
        "iptal/değişiklik isterse: bu işlemler Instagram'dan YAPILAMAZ. Randevu "
        "listesi verme, tarih/saat uydurma. Bunları online randevu sayfasından "
        "(booking_url) görüntüleyip iptal/değişiklik yapabileceğini sıcak bir dille "
        "söyle; gerekiyorsa escalate_to_human ile yetkiliye aktar. Telefon/e-posta "
        "İSTEME (burada kimlik doğrulayamazsın).\n"
        "- Şikayet, özel/karmaşık talep, müşterinin insan/yetkili istemesi ya da "
        "çıkmaza girme durumunda escalate_to_human kullan ve müşteriye bir "
        "yetkiliye aktardığını sıcak bir dille söyle.\n"
        "- Konu işletme dışıysa kibarca işletmeyle ilgili konulara yönlendir.\n"
    )


async def _post_chat(
    client: httpx.AsyncClient,
    url: str,
    headers: dict,
    payload: dict,
) -> httpx.Response:
    """Groq /chat/completions POST'u; 429'da backoff'lu 3 deneme.

    Hata gövdesini (Groq'un asıl mesajı: tool_use_failed, context_length vb.)
    loglar — raise_for_status traceback'inde kaybolmasın diye.
    """
    resp = None
    for attempt in range(3):
        resp = await client.post(url, headers=headers, json=payload)
        if resp.status_code != 429 or attempt == 2:
            break
        wait = float(resp.headers.get("Retry-After") or (1.5 * (1 + attempt)))
        log.warning("Groq 429 — %.1fs bekleyip tekrar deneniyor (attempt=%d)",
                    wait, attempt + 1)
        await asyncio.sleep(wait)
    if resp is None:
        raise RuntimeError("Groq API isteği yapılamadı")
    if resp.status_code >= 400:
        log.error("Groq %d yanıtı: %s", resp.status_code, resp.text[:2000])
    return resp


def to_messages_payload(
    system_prompt: str,
    history: list[dict],
    user_message: str,
    history_turns: int,
) -> list[dict]:
    """Mongo mesaj formatından OpenAI mesaj formatına dönüştürür."""
    msgs: list[dict] = [{"role": "system", "content": system_prompt}]

    # Son N user/assistant mesajını al (tool turlarını atla)
    trimmed = [
        m for m in history if m.get("role") in ("user", "assistant") and m.get("content")
    ][-history_turns:]
    for m in trimmed:
        msgs.append({"role": m["role"], "content": m.get("content") or ""})

    msgs.append({"role": "user", "content": user_message})
    return msgs


async def run_turn(
    ctx: ToolContext,
    history: list[dict],
    user_message: str,
) -> tuple[str, list[dict]]:
    """
    Bir kullanıcı mesajı üzerine AI turunu çalıştırır.
    Döner: (assistant_metni, Mongo'ya eklenecek tool mesaj logu).
    """
    settings = get_settings()
    system_prompt = build_system_prompt(ctx.business, ctx.customer)
    messages = to_messages_payload(
        system_prompt, history, user_message, settings.conversation_history_turns
    )

    new_log: list[dict] = []  # bu turda Mongo'ya eklenecek tool mesajları

    url = f"{settings.groq_base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.groq_api_key}",
    }

    async with httpx.AsyncClient(timeout=settings.ai_request_timeout_s) as client:
        for _iteration in range(settings.ai_max_tool_iterations):
            payload: dict[str, Any] = {
                "model": settings.groq_model,
                "messages": messages,
                "tools": _TOOL_SCHEMAS,
                "tool_choice": "auto",
                "temperature": 0.2,
                "stream": False,
            }
            resp = await _post_chat(client, url, headers, payload)
            # 400 genelde Groq'un `tool_use_failed`'i: model geçerli tool çağrısı
            # üretemedi. Elimizde zaten tool sonuçları varsa, tool'suz tek bir
            # çağrıyla yanıtı toparlamayı dene — kullanıcıyı akışın ortasında
            # ölü uca düşürmektense.
            if resp.status_code == 400 and any(m["role"] == "tool" for m in messages):
                log.warning("Groq 400 — tool'suz yeniden deneniyor (degrade).")
                degraded = await _post_chat(client, url, headers, {
                    "model": settings.groq_model,
                    "messages": messages,
                    "temperature": 0.2,
                    "stream": False,
                })
                degraded.raise_for_status()
                content = (degraded.json()["choices"][0]["message"].get("content")
                           or "").strip()
                if content:
                    return content, new_log
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]["message"]
            tool_calls = choice.get("tool_calls") or []
            content = choice.get("content") or ""

            if not tool_calls:
                return content.strip(), new_log

            # Asistanın tool_call mesajını da geçmişe ekle (modelin beklediği biçim)
            messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls,
            })

            for tc in tool_calls:
                fn = tc.get("function") or {}
                name = fn.get("name") or ""
                raw_args = fn.get("arguments")
                if isinstance(raw_args, str):
                    try:
                        args = json.loads(raw_args) if raw_args else {}
                    except json.JSONDecodeError:
                        args = {}
                else:
                    args = raw_args or {}

                log.info("AI tool çağrısı: %s args=%s", name, args)
                result = await dispatch(ctx, name, args)

                tool_content = json.dumps(result, default=str, ensure_ascii=False)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", name),
                    "name": name,
                    "content": tool_content,
                })
                new_log.append({
                    "role": "tool",
                    "content": tool_content,
                    "timestamp": datetime.now(timezone.utc),
                    "tool_name": name,
                    "tool_args": args,
                    "channel_msg_id": None,
                })

        # Iter limiti doldu — personele aktar ve fallback dön
        log.warning("AI tool-use iter limiti aşıldı; fallback metnine düşülüyor.")
        fallback = (
            (ctx.business.get("ai_settings") or {}).get("fallback_message")
            or "Şu an yardımcı olamadım, sizi bir personelimize aktarıyorum."
        )
        await dispatch(ctx, "escalate_to_human", {"reason": "tool_iter_limit"})
        return fallback, new_log
