from __future__ import annotations

import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import ai, db

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Household Words", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _context(request: Request, **extra) -> dict:
    context = {
        "request": request,
        "path": request.url.path,
        "now": datetime.now(timezone.utc),
        "live_ai": ai.available(),
        "msg": request.query_params.get("msg"),
    }
    context.update(extra)
    return context


def _clean(value: str, limit: int = 600) -> str:
    return " ".join((value or "").split()).strip()[:limit]


def _entry_payload(
    phrase: str,
    pronunciation: str,
    part_of_speech: str,
    meaning: str,
    who_says_it: str,
    usage: str,
    story: str,
    example: str,
) -> dict:
    return {
        "phrase": db.normalise_phrase(phrase),
        "pronunciation": _clean(pronunciation, 120),
        "part_of_speech": _clean(part_of_speech, 60) or "family phrase",
        "meaning": _clean(meaning),
        "who_says_it": _clean(who_says_it),
        "usage": _clean(usage),
        "story": _clean(story),
        "example": _clean(example),
    }


@app.get("/")
def phrasebook(request: Request):
    entries = db.list_entries()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=_context(request, entries=entries),
    )


@app.get("/add")
def add_phrase(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add.html",
        context=_context(request),
    )


@app.post("/interview")
def interview(request: Request, phrase: str = Form("")):
    phrase = db.normalise_phrase(phrase)
    if not phrase:
        return templates.TemplateResponse(
            request=request,
            name="add.html",
            context=_context(request, error="Give the phrase a name first."),
            status_code=400,
        )
    if len(phrase) > 80:
        return templates.TemplateResponse(
            request=request,
            name="add.html",
            context=_context(
                request,
                error="Keep the phrase under 80 characters.",
                phrase=phrase,
            ),
            status_code=400,
        )
    existing = db.find_by_phrase(phrase)
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="add.html",
            context=_context(
                request,
                error="That phrase is already in the phrasebook.",
                phrase=phrase,
                existing=existing,
            ),
            status_code=409,
        )

    result = ai.ask_questions(phrase)
    return templates.TemplateResponse(
        request=request,
        name="interview.html",
        context=_context(
            request,
            phrase=phrase,
            questions=result["questions"],
            ai_mode=result["mode"],
        ),
    )


@app.post("/preview")
def preview(
    request: Request,
    phrase: str = Form(""),
    who: str = Form(""),
    meaning: str = Form(""),
    origin: str = Form(""),
    usage: str = Form(""),
):
    phrase = db.normalise_phrase(phrase)
    if not phrase:
        return RedirectResponse("/add", status_code=303)

    answers = {
        "who": _clean(who),
        "meaning": _clean(meaning),
        "origin": _clean(origin),
        "usage": _clean(usage),
    }
    result = ai.draft_entry(phrase, answers)
    return templates.TemplateResponse(
        request=request,
        name="preview.html",
        context=_context(
            request,
            entry=result,
            ai_mode=result.get("mode", "fallback"),
        ),
    )


@app.post("/save")
def save_entry(
    request: Request,
    phrase: str = Form(""),
    pronunciation: str = Form(""),
    part_of_speech: str = Form(""),
    meaning: str = Form(""),
    who_says_it: str = Form(""),
    usage: str = Form(""),
    story: str = Form(""),
    example: str = Form(""),
):
    payload = _entry_payload(
        phrase,
        pronunciation,
        part_of_speech,
        meaning,
        who_says_it,
        usage,
        story,
        example,
    )
    if not payload["phrase"]:
        return RedirectResponse("/add", status_code=303)
    if len(payload["phrase"]) > 80:
        return templates.TemplateResponse(
            request=request,
            name="preview.html",
            context=_context(
                request,
                entry=payload,
                error="Keep the phrase under 80 characters.",
            ),
            status_code=400,
        )
    existing = db.find_by_phrase(payload["phrase"])
    if existing:
        return templates.TemplateResponse(
            request=request,
            name="preview.html",
            context=_context(
                request,
                entry=payload,
                error="That phrase is already in the phrasebook.",
                existing=existing,
            ),
            status_code=409,
        )

    try:
        entry_id = db.create_entry(payload)
    except (ValueError, sqlite3.IntegrityError):
        return templates.TemplateResponse(
            request=request,
            name="preview.html",
            context=_context(
                request,
                entry=payload,
                error="That phrase could not be saved. Try a slightly different phrase.",
            ),
            status_code=409,
        )
    return RedirectResponse(f"/entries/{entry_id}?msg=Added+to+the+phrasebook", status_code=303)


@app.get("/entries/{entry_id}")
def entry_detail(request: Request, entry_id: int):
    entry = db.get_entry(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return templates.TemplateResponse(
        request=request,
        name="entry.html",
        context=_context(request, entry=entry),
    )


@app.get("/print")
def print_phrasebook(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="print.html",
        context=_context(request, entries=db.list_entries()),
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "ai": "live" if ai.available() else "fallback",
        "entries": db.count_entries(),
    }
