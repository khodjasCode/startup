"""Vaqt bilan cheklangan xotira keshi.

Katalog va tarjimalar Postgres'da turadi, lekin ular deyarli o'zgarmaydi va
har bir so'rovda bazaga borish (Supabase serveri chet elda — har chaqiruv
yuzlab millisekund) sahifani sekinlashtiradi. Shuning uchun ular bir marta
o'qilib, `COMPASS_KATALOG_KESH_SONIYA` davomida xotirada saqlanadi.

`COMPASS_KATALOG_KESH_SONIYA=0` bo'lsa kesh o'chadi — har so'rov bazadan
o'qiydi (ma'lumot tez-tez o'zgaradigan muhitda foydali).
"""

from __future__ import annotations

import os
import threading
import time
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

KESH_SONIYA = float(os.environ.get("COMPASS_KATALOG_KESH_SONIYA", "300"))


class Kesh(Generic[T]):
    """Bitta qiymatni saqlaydigan kesh: kerak bo'lganda `yuklovchi` chaqiriladi."""

    def __init__(self, yuklovchi: Callable[[], T], umr_soniya: float | None = None) -> None:
        self._yuklovchi = yuklovchi
        self._umr = KESH_SONIYA if umr_soniya is None else umr_soniya
        self._qiymat: T | None = None
        self._vaqt = 0.0
        self._qulf = threading.Lock()

    def olish(self) -> T:
        # Ikki oqim bir vaqtda kelsa, ikkinchisi qulfni kutib turadi va tayyor
        # qiymatni oladi — baza bir marta o'qiladi.
        with self._qulf:
            eskirgan = (
                self._umr <= 0
                or self._qiymat is None
                or time.monotonic() - self._vaqt > self._umr
            )
            if eskirgan:
                self._qiymat = self._yuklovchi()
                self._vaqt = time.monotonic()
            return self._qiymat

    def tozalash(self) -> None:
        """Keyingi murojaatda baza qayta o'qiladi."""
        with self._qulf:
            self._qiymat = None
            self._vaqt = 0.0
