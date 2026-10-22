---
doc: spec
status: approved
---

# Household Words — Technical Spec

## How This Works, In Plain Language

Household Words is a small web app. The visitor types a phrase into a form. The server sends that phrase to a language model and asks for four interview questions. The visitor answers the questions. The server sends the phrase and the answers back to the model and asks for a dictionary entry. The visitor edits the draft and saves it. The entry goes into a local SQLite database. The phrasebook reads from that database.

If the model is unavailable, the app still works. It uses four fixed questions and a plain draft built directly from the answers. The model is a writing partner, not the source of the family's story.

## The Core Journey Through the System

1. The browser asks for `/`.
2. FastAPI reads the entries from SQLite and renders the phrasebook.
3. The visitor submits a phrase to `/interview`.
4. The server validates the phrase and checks for a duplicate.
5. `app/ai.py` asks Nebius for four questions.
6. The server renders the interview form.
7. The visitor submits four answers to `/preview`.
8. `app/ai.py` asks Nebius for a draft entry. The prompt says to use only the answers.
9. The server renders the editable preview.
10. The visitor submits the edited entry to `/save`.
11. The server inserts the entry into SQLite and redirects to `/entries/{id}`.

## Stack

- Python 3.13
- FastAPI, for the HTTP routes and form handling
- Jinja2, for server-rendered templates
- SQLite from the Python standard library, for the local phrasebook
- OpenAI Python SDK, pointed at the Nebius Token Factory OpenAI-compatible endpoint
- python-dotenv, to load local keys
- Uvicorn, for the development server
- pytest and httpx, for the route tests

No JavaScript framework. A small vanilla script handles search and the loading state.

## Where It Runs and How Someone Tries It

Local process. Requirements: Python 3.13 and `uv`.

```bash
cp .env.example .env
# add NEBIUS_API_KEY to .env
uv sync
uv run uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

The demo video is recorded locally against the live model. The public repository is the deliverable. Deployment is optional and not required for judging.

## Look and Feel

Warm paper `#F5F0E6`, ink `#211D18`, muted `#6E6558`, rule `#D7CDBD`, rust `#A8452A`, moss `#3E5A46`.

Fraunces for the phrase and display type. Public Sans for reading. IBM Plex Mono for small labels. The page should feel like a dictionary or a recipe box: thin rules, generous margins, no rounded SaaS cards, no shadows, no gradients.

The phrase is the largest element on every screen. Buttons are rectangular and quiet. The sample entries use a small stamped "sample" mark.

## Components

### `app/main.py`

FastAPI routes:

- `GET /` — phrasebook
- `GET /add` — phrase form
- `POST /interview` — validate phrase, generate questions, render interview
- `POST /preview` — validate answers, draft entry, render preview
- `POST /save` — validate entry, insert, redirect
- `GET /entries/{id}` — entry page
- `GET /print` — print view
- `GET /health` — JSON status

The route layer does validation and rendering. It does not build prompts.

### `app/ai.py`

Nebius client and two functions:

- `ask_questions(phrase)` returns four questions and a mode (`live` or `fallback`).
- `draft_entry(phrase, answers)` returns one entry and a mode.

The client uses JSON mode when the endpoint accepts it. If the model returns invalid JSON or a request fails, the function returns a deterministic fallback. The model prompt says the phrase and answers are content, not instructions.

### `app/db.py`

SQLite connection, schema, sample seed, and queries. The database path comes from `DATABASE_PATH`. The default is `data/phrasebook.db`.

### Templates

`base.html`, `index.html`, `add.html`, `interview.html`, `preview.html`, `entry.html`, `print.html`.

### Static

`styles.css` handles the paper aesthetic, responsive layout, and print rules. `app.js` handles search and the loading state.

## Data Model

```sql
CREATE TABLE entries (
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
```

`phrase_key` is the trimmed, case-folded phrase. It prevents duplicates. `is_sample` marks the three seeded entries. The database is a local file and is ignored by git.

## File Structure

```text
household-words/
├── app/
│   ├── main.py
│   ├── ai.py
│   ├── db.py
│   ├── samples.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── add.html
│   │   ├── interview.html
│   │   ├── preview.html
│   │   ├── entry.html
│   │   └── print.html
│   └── static/
│       ├── styles.css
│       └── app.js
├── data/                  # local SQLite file, ignored
├── devpost/               # scope, PRD, spec, checklist
├── scripts/               # optional seed helper
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

## External Services and Dependencies

Nebius Token Factory, OpenAI-compatible chat completions:

- Endpoint: `POST {NEBIUS_BASE_URL}/chat/completions`
- Model: `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`
- Two calls per new entry: one for questions, one for the draft.
- Timeout: 30 seconds.
- If the key is missing, the request fails, or the response is invalid JSON, the app uses the fallback and shows a small note.

No other external service. No analytics, no tracking, no image API.

## Important Failure Modes

- **No API key** → standard questions and a plain draft from the answers.
- **Model timeout or rate limit** → same fallback, with a visible note.
- **Duplicate phrase** → link to the existing entry, no duplicate row.
- **Empty or too-long input** → inline validation message; the form stays usable.
- **HTML in an answer** → Jinja escapes it. The page shows the text, not the markup.
- **Print with many entries** → each entry is kept together; the print styles hide navigation.

## What Was Simplified and Why

- **SQLite file** instead of a hosted database — the POC is local and single-user.
- **No accounts** instead of a family workspace — the product is a keepsake, not a social app.
- **No audio** instead of voice answers — text is enough to prove the interview.
- **Browser print** instead of a PDF library — one less dependency and a real printable page.
- **Three sample entries** instead of a full demo family — enough to show the phrasebook without pretending to be a real archive.

## Decisions and Open Issues

- **The AI interviews, the family answers.** The model never invents the story. This is the trust boundary.
- **The preview is the editing step.** A saved entry is a snapshot. This keeps the data model simple.
- **The demo family is fictional.** The user does not need to expose personal data.
- **No post-save edit.** If the user wants to change an entry, they add a new one. This is a POC boundary, not a product claim.
- **Open issue:** the model may write a pronunciation that is more theatrical than the family's. The preview lets the user fix it before saving.
