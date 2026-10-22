---
doc: scope
status: approved
---

# Household Words

One line: a small dictionary for the words only your family uses.

## The Unique Kernel

The AI interviews you about a family phrase, then turns your answers into a dictionary entry. The family supplies the meaning and the story. The app does not invent them.

That is the difference between this and a generic story generator. The interview is the product. The entry is the keepsake.

## Who It's For

Someone who has a phrase in their family that outsiders do not understand. A nickname, a saying, a mispronunciation that stuck. They know what it means when their mother says it. They have never written it down.

Today they might tell the story in a group chat, or not at all. The phrase survives in speech, not on paper.

## The Core Loop

Open the phrasebook. Add a phrase. Answer four questions about who says it, what it means, where it came from, and how it is used. Edit the entry. Save it. Come back to browse the phrasebook or print it.

The loop is intentionally small. One phrase in, one entry out.

## Inspiration & Identity

The mood is a family dictionary left on a kitchen table. Paper, ink, index cards, a little wear. Serif type for the phrase, quiet sans for the explanation, mono for the labels. It should feel like something you would keep, not a dashboard you would close.

The closest references are a well-worn dictionary, a recipe box, and a margin note in a cookbook. The term "familect" is useful context: the words only one family uses.

Avoid: gradients, glass cards, purple AI branding, chat bubbles, and the look of a generic SaaS app.

## Why This Matters to the Learner

Family language disappears quietly. The phrase is obvious until the person who said it is gone. Writing it down is a small act of preservation. The project is also a chance to build a warm, human interface instead of another utility dashboard.

The demo family is fictional. The user can keep their own family out of the video.

## What "Working" Looks Like

A person opens the phrasebook, sees three sample entries, and adds "the good scissors." The AI asks four questions that fit the phrase. The person answers. The app produces a draft entry with a pronunciation, meaning, who says it, usage, story, and example. The person edits one line and saves it. The entry appears in the phrasebook. The print view fits on a page.

The "oh, that's cool" beat is the moment the generic phrase becomes a written entry in the family's voice.

## The POC Boundary

In:

- A phrase input with a clear example.
- Four AI-generated interview questions.
- An editable dictionary entry preview.
- Save to a local SQLite database.
- A phrasebook list with search.
- An entry page.
- A print view.
- Three fictional sample entries.
- A deterministic fallback when the model is unavailable.

Out:

- Accounts, login, and multi-user support.
- Audio recording or voice input.
- Image generation or photo upload.
- Public sharing links.
- Multiple family workspaces.
- Translations.
- A native mobile app.
- PDF export beyond the browser print dialog.

## Later

- Voice answers with a transcript.
- A printable book with a cover and contents.
- Share a single entry as an image.
- Invite relatives to add their own version of a phrase.
- A "phrase of the week" prompt for families.

## Explicitly Cut

- **Accounts** because the POC is a local keepsake, not a social product.
- **Audio recording** because it adds storage and privacy weight without proving the kernel.
- **Image generation** because the phrase is the visual.
- **Public sharing** because the demo family is fictional and the user does not want personal data exposed.
- **Post-save editing** because the preview is the editing step. The entry is a snapshot, not a wiki.
