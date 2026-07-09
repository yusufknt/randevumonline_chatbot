"""
RandevumOnline Sesli Randevu Asistanı (Voice Agent) Modülü.

Bu modül, Asterisk VoIP santralinden gelen aramalardaki ses akışını
TCP AudioSocket protokolü üzerinden alıp STT -> LLM -> TTS döngüsü ile
müşteriyle sesli diyalog kurar ve MongoDB'ye randevu kaydeder.
"""

from __future__ import annotations
