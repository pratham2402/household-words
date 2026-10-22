# Household Words

A small dictionary for the words only your family uses.

Household Words asks four questions about a family phrase, turns the answers into a dictionary entry, and keeps the entry in a printable phrasebook. The AI asks and drafts. The family supplies the meaning and the story.

Built for the Devpost **Build With AI: Basics** hackathon.

## Demo

[Watch the 85-second demo](https://youtu.be/VIG4UDS5qFY).

Submitted on [Devpost](https://devpost.com/software/household-words).

## What it does

- Start with a phrase, for example "the good scissors."
- The AI writes four interview questions that fit that phrase.
- Answer in your own words.
- The app drafts an entry with a pronunciation, meaning, who says it, usage, story, and example.
- Edit the draft, save it, and print the phrasebook.
- Search the phrasebook by phrase, meaning, or who says it.

The home page includes three fictional entries from the Vale family. The Vales are a sample. No real family data is used.

## Why it exists

Family language disappears quietly. A phrase is obvious until the person who said it is gone. Most memory apps ask you to write a book. Household Words asks one small question at a time and gives you something you can keep after five minutes.

The interesting part is the interview. The AI does not invent the family story. It asks, and the person answers. That is the human check.

## Quickstart

Requirements: Python 3.13 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env
# add NEBIUS_API_KEY to .env
uv run uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>.

Without a key, the app still runs. It uses four standard questions and a draft built directly from your answers. The header says `Fallback questions`.

## AI use

Two model calls per new entry:

1. `ask_questions` reads the phrase and returns four short questions.
2. `draft_entry` reads the phrase and the answers and returns one JSON entry.

The system prompt says to use only the supplied answers and never invent a person, place, date, or story. If the model is unavailable or returns invalid JSON, the app falls back to a plain draft. The app does not retry in a loop, and page loads make no model calls.

Model: `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` through the Nebius Token Factory OpenAI-compatible endpoint. Change `NEBIUS_MODEL` to use another model.

## Data and privacy

- Entries live in a local SQLite file at `data/phrasebook.db`.
- The database is ignored by git.
- There are no accounts, analytics, cookies, or external storage.
- The app does not upload files or record audio.
- The demo family is fictional.

This is a local proof of concept, not a multi-user service. There is no authentication. Do not put real family data on a public server without adding access control.

## Tests

```bash
uv run pytest -q
```

The suite covers the sample seed, phrase validation, duplicate detection, the AI fallback, route rendering, save, search data, and the print page.

## Project structure

```text
app/
  main.py          FastAPI routes and form validation
  ai.py            Nebius client, prompts, and fallbacks
  db.py            SQLite schema, seed, and queries
  samples.py       The three fictional Vale entries
  templates/       Jinja screens
  static/          Handwritten CSS and a small JS file
devpost/           scope.md, prd.md, spec.md, checklist.md
scripts/           reset_phrasebook.py
tests/             Route and fallback tests
```

## Planning docs

The hackathon asks for the planning documents in the repository. They are in [`devpost/`](devpost/):

- [`scope.md`](devpost/scope.md)
- [`prd.md`](devpost/prd.md)
- [`spec.md`](devpost/spec.md)
- [`checklist.md`](devpost/checklist.md)

## Limitations

- One local phrasebook. No accounts or multiple families.
- No post-save editing. The preview is the editing step.
- Text only. No audio or images.
- English interface, but any language can be entered as a phrase.
- The model can still write something awkward. The preview is there to fix it.
- The print view uses the browser print dialog, not a generated PDF.

## Reset the demo

```bash
uv run python scripts/reset_phrasebook.py
```

This deletes the local database and seeds the three sample entries again.

## License

MIT. See [LICENSE](LICENSE).
