from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.samples import SAMPLE_ENTRIES

SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phrase TEXT NOT NULL,
    phrase_key TEXT NOT NULL UNIQUE,
    pronunciation TEXT NOT NULL DEFAULT '',
    part_of_speech TEXT NOT NULL DEFAULT 'family phrase',
    meaning TEXT NOT NULL DEFAULT '',
    who_says_it TEXT NOT NULL DEFAULT '',
    usage TEXT NOT NULL DEFAULT '',
    story TEXT NOT NULL DEFAULT '',
    example TEXT NOT NULL DEFAULT '',
    is_sample INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
"""


def get_db_path() -> Path:
    raw = os.environ.get("DATABASE_PATH", "data/phrasebook.db")
    path = Path(raw)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(get_db_path())
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with connect() as connection:
        connection.executescript(SCHEMA)
        count = connection.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
        if count:
            return
        for sample in SAMPLE_ENTRIES:
            _insert(connection, sample, is_sample=True)
        connection.commit()


def list_entries() -> list[dict]:
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT * FROM entries
            ORDER BY is_sample ASC, created_at DESC, id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_entry(entry_id: int) -> dict | None:
    with connect() as connection:
        row = connection.execute(
            "SELECT * FROM entries WHERE id = ?", (entry_id,)
        ).fetchone()
    return dict(row) if row else None


def find_by_phrase(phrase: str) -> dict | None:
    key = phrase_key(phrase)
    if not key:
        return None
    with connect() as connection:
        row = connection.execute(
            "SELECT * FROM entries WHERE phrase_key = ?", (key,)
        ).fetchone()
    return dict(row) if row else None


def create_entry(data: dict) -> int:
    phrase = normalise_phrase(data.get("phrase", ""))
    if not phrase:
        raise ValueError("A phrase is required.")
    with connect() as connection:
        entry_id = _insert(connection, data, is_sample=False)
        connection.commit()
    return entry_id


def count_entries() -> int:
    with connect() as connection:
        return connection.execute("SELECT COUNT(*) FROM entries").fetchone()[0]


def normalise_phrase(value: str) -> str:
    return " ".join((value or "").split()).strip()


def phrase_key(value: str) -> str:
    return normalise_phrase(value).casefold()


def _insert(connection: sqlite3.Connection, data: dict, is_sample: bool) -> int:
    phrase = normalise_phrase(data.get("phrase", ""))
    created_at = datetime.now(timezone.utc).isoformat()
    cursor = connection.execute(
        """
        INSERT INTO entries (
            phrase, phrase_key, pronunciation, part_of_speech, meaning,
            who_says_it, usage, story, example, is_sample, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            phrase,
            phrase_key(phrase),
            data.get("pronunciation", ""),
            data.get("part_of_speech", "family phrase"),
            data.get("meaning", ""),
            data.get("who_says_it", ""),
            data.get("usage", ""),
            data.get("story", ""),
            data.get("example", ""),
            1 if is_sample else 0,
            created_at,
        ),
    )
    return int(cursor.lastrowid)
