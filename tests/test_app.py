from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_DB = Path(__file__).resolve().parent / "test_phrasebook.db"
os.environ["DATABASE_PATH"] = str(TEST_DB)

from app import ai, db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    if TEST_DB.exists():
        TEST_DB.unlink()
    db.init_db()
    yield
    if TEST_DB.exists():
        TEST_DB.unlink()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_phrasebook_renders_samples(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "The good scissors" in response.text
    assert "A porch call" in response.text
    assert "The blue bowl" in response.text


def test_add_page_renders(client):
    response = client.get("/add")
    assert response.status_code == 200
    assert "What's a word only your family uses?" in response.text


def test_empty_phrase_is_rejected(client):
    response = client.post("/interview", data={"phrase": "   "})
    assert response.status_code == 400
    assert "Give the phrase a name first" in response.text


def test_phrase_length_is_limited(client):
    response = client.post("/interview", data={"phrase": "x" * 81})
    assert response.status_code == 400
    assert "under 80 characters" in response.text


def test_duplicate_phrase_links_to_existing_entry(client):
    response = client.post("/interview", data={"phrase": "The good scissors"})
    assert response.status_code == 409
    assert "already in the phrasebook" in response.text
    assert "/entries/1" in response.text


def test_fallback_questions_render(client, monkeypatch):
    monkeypatch.setattr(ai, "available", lambda: False)
    response = client.post("/interview", data={"phrase": "the kitchen meeting"})
    assert response.status_code == 200
    assert "standard questions" in response.text
    assert "Who in your family says this?" in response.text


def test_fallback_preview_and_save(client, monkeypatch):
    monkeypatch.setattr(ai, "available", lambda: False)
    response = client.post(
        "/preview",
        data={
            "phrase": "the kitchen meeting",
            "who": "Mum and Dad, while the kettle is on.",
            "meaning": "A conversation that lasts longer than the tea.",
            "origin": "From the winter everyone stood in the kitchen.",
            "usage": "We had a kitchen meeting about the holiday.",
        },
    )
    assert response.status_code == 200
    assert "built directly from your answers" in response.text
    assert "A conversation that lasts longer than the tea." in response.text

    response = client.post(
        "/save",
        data={
            "phrase": "the kitchen meeting",
            "pronunciation": "",
            "part_of_speech": "family phrase",
            "meaning": "A conversation that lasts longer than the tea.",
            "who_says_it": "Mum and Dad, while the kettle is on.",
            "usage": "We had a kitchen meeting about the holiday.",
            "story": "From the winter everyone stood in the kitchen.",
            "example": "Not recorded yet.",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "the kitchen meeting" in response.text
    assert "A conversation that lasts longer than the tea." in response.text


def test_html_in_answers_is_escaped(client, monkeypatch):
    monkeypatch.setattr(ai, "available", lambda: False)
    response = client.post(
        "/preview",
        data={
            "phrase": "the warning",
            "who": "<script>alert(1)</script>",
            "meaning": "A test.",
            "origin": "",
            "usage": "",
        },
    )
    assert response.status_code == 200
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in response.text
    assert "<script>alert(1)</script>" not in response.text


def test_print_page_renders(client):
    response = client.get("/print")
    assert response.status_code == 200
    assert "The Vale family phrasebook" in response.text
    assert "The good scissors" in response.text


def test_entry_not_found(client):
    response = client.get("/entries/9999")
    assert response.status_code == 404


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["entries"] == 3
