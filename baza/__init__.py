"""PostgreSQL (Supabase) ulanishi — `web` va `bot` uchun umumiy qatlam.

Manzil `DATABASE_URL` environment o'zgaruvchisidan olinadi (`.env` avtomatik
yuklanadi). Supabase'ning **pooler** manzili ishlatiladi (6543-port,
transaction rejimi) — u ko'p qisqa ulanishlarga mo'ljallangan.

Ishlatish:

    from baza import kursor, sorov, bitta, bajarish

    xizmatlar = sorov("select * from xizmatlar where soha = %s", (soha,))

    with ulanish() as conn:            # bir nechta buyruq — bitta tranzaksiyada
        with conn.cursor() as cur:
            ...

Chaqiruvlar **bloklovchi** (psycopg2). FastAPI ichida ular `async def` emas,
oddiy `def` marshrutlaridan chaqiriladi — u holda FastAPI ularni alohida
oqimda bajaradi va hodisa halqasi bloklanmaydi.
"""

from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import psycopg2
from psycopg2 import InterfaceError, OperationalError
from psycopg2.extras import Json, RealDictCursor
from psycopg2.pool import ThreadedConnectionPool

from baza.muhit import env_yuklash

env_yuklash()

SXEMA_YOLI = Path(__file__).resolve().parent / "sxema.sql"

# Supabase pooler bir loyihaga cheklangan ulanish beradi, shuning uchun hovuz kichik.
ENG_KAM_ULANISH = int(os.environ.get("BAZA_ENG_KAM_ULANISH", "1"))
ENG_KOP_ULANISH = int(os.environ.get("BAZA_ENG_KOP_ULANISH", "8"))
ULANISH_KUTISH_SONIYA = int(os.environ.get("BAZA_KUTISH_SONIYA", "15"))

__all__ = [
    "BazaSozlanmagan",
    "Json",
    "bajarish",
    "bitta",
    "hovuzni_yopish",
    "kursor",
    "manzil",
    "sorov",
    "sxemani_yaratish",
    "tekshirish",
    "ulanish",
]


class BazaSozlanmagan(RuntimeError):
    """`DATABASE_URL` berilmagan — ulanish mumkin emas."""


def manzil() -> str:
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        raise BazaSozlanmagan(
            "DATABASE_URL topilmadi. Loyiha ildizidagi .env faylga yozing "
            "(namuna: .env.example) yoki `export DATABASE_URL=...` qiling."
        )
    return url


_hovuz: ThreadedConnectionPool | None = None
_qulf = threading.Lock()


def _hovuzni_olish() -> ThreadedConnectionPool:
    global _hovuz
    if _hovuz is None:
        with _qulf:
            if _hovuz is None:
                _hovuz = ThreadedConnectionPool(
                    ENG_KAM_ULANISH,
                    ENG_KOP_ULANISH,
                    dsn=manzil(),
                    connect_timeout=ULANISH_KUTISH_SONIYA,
                    application_name="compass",
                )
    return _hovuz


def hovuzni_yopish() -> None:
    """Barcha ulanishlarni yopadi (server to'xtaganda / testlardan keyin)."""
    global _hovuz
    with _qulf:
        if _hovuz is not None:
            _hovuz.closeall()
            _hovuz = None


@contextmanager
def ulanish() -> Iterator[Any]:
    """Hovuzdan ulanish beradi; blok muvaffaqiyatli tugasa — commit, xatoda — rollback."""
    hovuz = _hovuzni_olish()
    conn = hovuz.getconn()
    buzilgan = False
    try:
        yield conn
        conn.commit()
    except BaseException:
        # Ulanishning o'zi uzilgan bo'lsa rollback ham ishlamaydi — uni hovuzga
        # qaytarmasdan yopamiz, aks holda keyingi so'rov ham shu ulanishga tushadi.
        try:
            conn.rollback()
        except (OperationalError, InterfaceError):
            buzilgan = True
        raise
    finally:
        hovuz.putconn(conn, close=buzilgan)


@contextmanager
def kursor(conn: Any | None = None) -> Iterator[Any]:
    """Lug'at qaytaruvchi kursor (`RealDictCursor`).

    `conn` berilsa mavjud tranzaksiya ichida ishlaydi, aks holda o'zi ulanadi.
    """
    if conn is not None:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        return
    with ulanish() as yangi:
        with yangi.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur


def _bajar(sql: str, parametrlar: tuple | list | dict, olish: str) -> Any:
    """Bitta buyruqni bajaradi; uzilgan ulanish uchun bir marta qayta uriniladi.

    Pooler bo'sh turgan ulanishni o'zi yopishi mumkin — bu xato emas, shunchaki
    yangi ulanish olish kerak.
    """
    for urinish in (1, 2):
        try:
            with kursor() as cur:
                cur.execute(sql, parametrlar)
                if olish == "hammasi":
                    return [dict(q) for q in cur.fetchall()]
                if olish == "bitta":
                    qator = cur.fetchone()
                    return dict(qator) if qator is not None else None
                return cur.rowcount
        except (OperationalError, InterfaceError):
            if urinish == 2:
                raise
    return None  # bu yerga yetib kelinmaydi


def sorov(sql: str, parametrlar: tuple | list | dict = ()) -> list[dict]:
    """`select` — barcha qatorlar lug'atlar ro'yxati sifatida."""
    return _bajar(sql, parametrlar, "hammasi")


def bitta(sql: str, parametrlar: tuple | list | dict = ()) -> dict | None:
    """`select` — birinchi qator yoki `None`."""
    return _bajar(sql, parametrlar, "bitta")


def bajarish(sql: str, parametrlar: tuple | list | dict = ()) -> int:
    """`insert`/`update`/`delete` — o'zgargan qatorlar soni."""
    return _bajar(sql, parametrlar, "soni")


def sxemani_yaratish() -> None:
    """`sxema.sql` ni bajaradi (mavjud jadvallarga tegmaydi)."""
    with ulanish() as conn:
        with conn.cursor() as cur:
            cur.execute(SXEMA_YOLI.read_text(encoding="utf-8"))


def tekshirish() -> dict:
    """Ulanishni sinaydi — server versiyasi va bazani qaytaradi."""
    natija = bitta("select version() as versiya, current_database() as baza")
    return natija or {}


def jadval_bormi(nomi: str) -> bool:
    return bool(
        bitta(
            "select 1 from information_schema.tables "
            "where table_schema = 'public' and table_name = %s",
            (nomi,),
        )
    )


# psycopg2'ni to'g'ridan-to'g'ri chaqirish kerak bo'lganda (masalan kochirish
# skriptida `execute_values`) — shu modul orqali olinadi.
driver = psycopg2
