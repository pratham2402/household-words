---
doc: checklist
status: approved
---

# Build Checklist

Build mode: fast

## Slices

- [x] **1. The phrasebook renders with sample entries**
  Becomes usable: A running app shows three fictional Vale family entries in a warm, readable grid.
  Why now: Proves the scaffold, database seed, template layout, and visual direction in one pass.
  PRD ref: `prd.md > Screens and Layout`, `prd.md > Features and Behavior`
  Spec ref: `spec.md > Data Model`, `spec.md > File Structure`
  Build: Create the FastAPI app, SQLite schema, sample entries, base template, phrasebook page, and CSS.
  Verify: Start the server, open `/`, and confirm the three entries render.
  Commit: `Build the phrasebook shell and sample entries`

- [x] **2. A phrase can start an interview**
  Becomes usable: The visitor can submit a phrase and see four questions tailored to it.
  Why now: The interview is the unique kernel and the first AI call.
  PRD ref: `prd.md > The Core Journey` steps 3-5
  Spec ref: `spec.md > Components > app/ai.py`
  Build: Add the phrase form, validation, duplicate check, AI question call, fallback questions, and interview template.
  Verify: Submit "the good scissors" and confirm four questions render. Remove the key and confirm the fallback still works.
  Commit: `Add the phrase interview`

- [x] **3. Answers become a saved entry**
  Becomes usable: The visitor answers the questions, edits the draft, saves it, and sees the entry in the phrasebook.
  Why now: This completes the end-to-end loop.
  PRD ref: `prd.md > The Core Journey` steps 5-8
  Spec ref: `spec.md > The Core Journey Through the System`
  Build: Add the answer form, AI draft call, fallback draft, editable preview, save route, entry page, and duplicate protection.
  Verify: Add an entry, save it, and confirm it appears on `/` and `/entries/{id}`.
  Commit: `Turn answers into a saved dictionary entry`

- [x] **4. The phrasebook is usable**
  Becomes usable: Search filters the entries, the print view fits on paper, and the empty and error states are clear.
  Why now: These are the finishing behaviors a reviewer will notice.
  PRD ref: `prd.md > States and Boundaries`, `prd.md > Printing`
  Spec ref: `spec.md > Components > Static`
  Build: Add client-side search, print CSS, empty states, loading states, and mobile rules.
  Verify: Search for "scissors", print to PDF, and submit an empty phrase.
  Commit: `Polish search, print, and empty states`

- [x] **5. The demo is ready**
  Becomes usable: A public repo with planning docs, tests, a 1080p video, and a thumbnail.
  Why now: The judges see the video and repo, not the local server.
  PRD ref: `prd.md > What We're Building`
  Spec ref: `spec.md > Where It Runs and How Someone Tries It`
  Build: Add tests, README, license, video, thumbnail, and final screenshots.
  Verify: `uv run pytest`, the video plays, and the repo is public with the planning docs.
  Commit: `Prepare the demo and submission`

## Hands-on Checkpoints

- [ ] Early usable behavior explored
- [ ] Final kick-the-tires exploration and feedback completed

## Final Review

- [ ] Final review complete

## Code Tour and App Map

- [ ] Learning activity complete
- [ ] Optional edit and transfer reflection addressed
- [ ] `devpost/app-map.html` generated

Activity and evidence: pending
Route and stops: pending
Edit outcome: pending
Reflection: pending
Activity mode: pending
