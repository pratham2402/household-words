---
doc: prd
status: approved
---

# Household Words — Product Requirements

A small dictionary for the words only your family uses. Source: `scope.md > The Unique Kernel`.

## The Core Journey

1. The visitor lands on the phrasebook and sees three sample entries from the fictional Vale family.
2. They choose **Add a phrase**.
3. They type a phrase, for example "the good scissors."
4. The AI reads the phrase and writes four short interview questions: who says it, what it means, where it came from, and how it is used.
5. The visitor answers in their own words.
6. The app drafts a dictionary entry from those answers.
7. The visitor edits anything that does not sound right and saves it.
8. The new entry appears in the phrasebook.
9. The visitor can search the phrasebook, open an entry, or print the collection.

Success: a phrase that lived only in speech becomes a written entry the family would recognize.

## Screens and Layout

- **Phrasebook** — The home screen. A short introduction, search, and a grid of entries. Each card shows the phrase, pronunciation, a line of meaning, and who says it.
- **Add a phrase** — A single large input with examples. One primary button.
- **Interview** — The phrase as a heading, then four numbered questions with text areas. A note says the AI asks and the family answers.
- **Preview** — The draft entry as an editable card. All fields are visible. The save button is the only primary action.
- **Entry** — The saved dictionary entry. A print action and a link back to the phrasebook.
- **Print** — A clean page of all entries, with no navigation or buttons.

The layout is a single column on mobile and a two-column grid on wide screens. The phrase is always the largest element on the page.

## Look and Feel

Warm paper, dark ink, and a rust accent. Fraunces for display, Public Sans for body text, IBM Plex Mono for labels and small metadata. Thin rules instead of heavy cards. No gradients, no glass, no chat bubbles.

The interface should feel like a dictionary or a recipe box. Quiet, legible, and a little tactile. The sample family should feel specific enough to be real.

## Features and Behavior

### The phrasebook

- Shows entries newest first.
- Each card links to the full entry.
- Search filters by phrase, meaning, or who says it.
- Sample entries carry a small "sample" stamp.
- An empty phrasebook invites the first phrase.

### The interview

- The phrase is normalised before the AI call: trimmed, collapsed whitespace, and limited to 80 characters.
- The AI returns four questions with fixed keys: `who`, `meaning`, `origin`, `usage`.
- If the model is unavailable, the app uses four plain-language questions instead.
- Answers are limited to 600 characters each.

### The entry

The generated entry has these fields:

- phrase
- pronunciation
- part of speech
- meaning
- who says it
- usage
- story
- example

The AI must use only the phrase and the answers. It must not invent a family story. Missing information becomes "Not recorded yet."

### Saving and duplicates

- A phrase can appear once, compared case-insensitively after trimming.
- A duplicate phrase links to the existing entry instead of creating another.
- The saved entry is a snapshot. Editing after saving is out of scope.

### Printing

- The print view includes every entry.
- Navigation, search, buttons, and the page footer are hidden.
- Entries do not break across pages.

## States and Boundaries

- **First visit** — Three sample entries and a clear invitation to add a phrase.
- **Empty phrase** — An inline error: "Give the phrase a name first."
- **Duplicate** — A notice with a link to the existing entry.
- **AI unavailable** — A small note: "The AI is unavailable. These are the standard questions. Your answers still work." The entry draft is built directly from the answers.
- **Long text** — The form limits input length and the card wraps long words.
- **Missing field** — The app writes "Not recorded yet." It does not leave a blank.
- **Refresh on preview** — The browser may resubmit the form. The app handles it idempotently enough for a local POC; no duplicate is saved until the save action.
- **Print** — Each entry stays together on the page.

Nothing persists between sessions except the SQLite database on the server.

## Product Decisions

- **Local SQLite, no accounts** — keeps the POC small and the family data on the machine.
- **Fictional sample family** — the demo needs warmth without exposing a real family.
- **Editable preview** — the AI drafts, the person decides. This is the human check.
- **No post-save editing** — the preview is the editing step; a saved entry is a snapshot.
- **No audio** — the phrase is text. Voice would add storage and privacy weight without proving the kernel.
- **Print instead of PDF export** — the browser print dialog is enough for a proof of concept.

## What We're Building

- A FastAPI app with six screens.
- SQLite storage for entries.
- Nebius Token Factory for the interview questions and the entry draft.
- A deterministic fallback for both AI steps.
- Three fictional sample entries.
- Search and print.
- A test suite for validation, duplicates, fallback, and routes.

## Deferred From the POC

- Accounts and family workspaces.
- Audio answers and transcription.
- Sharing a single entry.
- Post-save editing.
- A cover and contents page for the printed book.
- Translations.

## Possible Later Enhancements

- A "record the pronunciation" button.
- A family invitation link.
- A weekly prompt by email.
- A small printed book with one phrase per page.

## Non-Goals

- This is not a social network.
- This is not a genealogy product.
- This is not a general dictionary.
- This is not a chatbot.
- This is not a replacement for a family historian.

## Open Questions

- Should the phrase be editable in the preview? **Decision: yes, it is a text input, but a saved entry cannot be edited.**
- Should the sample entries be deletable? **No. They are part of the demo.**
- Should the app support multiple families? **Not in the POC.**
