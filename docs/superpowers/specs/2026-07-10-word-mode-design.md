# Word Mode (Passphrase Generator) — Design Spec

**Date:** 2026-07-10
**Extends:** Password Generator Website (initial spec: `2026-07-10-password-generator-design.md`)

---

## Overview

Add a "Random / Words" mode toggle to the existing password generator. In Words mode, the app generates a passphrase of random common English words joined by hyphens (e.g. `correct-horse-battery-staple`). The user chooses how many words (3–10). The existing Random mode is unchanged.

---

## Backend

### New file: `words.py`

A plain Python module containing a single list `WORD_LIST` of ~1,000 common English words. No external dependencies. Words are lowercase, no punctuation.

### Updated file: `password_gen.py`

Add `generate_passphrase(word_count: int) -> str`:
- Imports `WORD_LIST` from `words.py`
- Uses `secrets.choice(WORD_LIST)` to pick `word_count` words
- Returns them joined with `"-"` (e.g. `"horse-battery-staple-correct"`)

### Updated route: `POST /generate` in `app.py`

New accepted JSON fields:
```json
{ "mode": "random" | "words", "word_count": 4 }
```

Logic:
- `mode` defaults to `"random"` if omitted (backward compatible)
- When `mode == "words"`: validate `word_count` is an integer between 3 and 10 (inclusive); return 400 + `{"error": "..."}` otherwise; call `generate_passphrase(word_count)`
- When `mode == "random"`: existing behaviour unchanged
- Character toggle fields (`use_upper`, `use_digits`, `use_symbols`) are ignored when `mode == "words"`

---

## Frontend

### Mode toggle

Two pill-shaped buttons at the top of the card: **Random** and **Words**. Active button uses the existing indigo/violet gradient; inactive is outlined. Default: Random.

### Control swap

- Existing controls (length slider + three toggle switches) wrapped in `<div id="random-controls">`.
- New controls in `<div id="word-controls">` (hidden by default):
  - Word count slider: range 3–10, default 4, with the same live numeric badge style as the length slider.
- Clicking the mode toggle shows the relevant div and hides the other.

### Generate button behaviour

When mode is Words, `fetch('/generate')` sends:
```json
{ "mode": "words", "word_count": <slider value as int> }
```
When mode is Random, existing payload unchanged (`mode` field omitted for backward compatibility).

### Visual style

Pill toggle uses the same `#6366f1 / #8b5cf6` gradient as the Generate button. Inactive button is white background with a border. No other visual changes to the card.

---

## Tests

### `password_gen.py`

- `test_generate_passphrase_word_count`: returned passphrase contains exactly N words (split by `-`)
- `test_generate_passphrase_words_from_list`: every word in the output appears in `WORD_LIST`
- `test_generate_passphrase_uses_hyphens`: separator is `-`

### `app.py` route

- `test_generate_words_mode_returns_passphrase`: `mode=words, word_count=4` → 200, `password` key contains 4 hyphen-separated words
- `test_generate_words_mode_rejects_count_too_low`: `word_count=2` → 400 + `error` key
- `test_generate_words_mode_rejects_count_too_high`: `word_count=11` → 400 + `error` key
- `test_generate_words_mode_rejects_boolean_count`: `word_count=True` → 400 + `error` key
- `test_generate_random_mode_unchanged`: existing random tests still pass (backward compatibility)

---

## Out of Scope

- Custom separators (space, underscore, etc.) — hyphen only
- Capitalising words in passphrase
- Mixing words and random characters
