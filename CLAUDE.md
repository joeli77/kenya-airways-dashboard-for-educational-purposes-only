# CLAUDE.md — Standalone Expense Console

## What this repo contains

Two unrelated things. Don't confuse them.

| File | What it is | Status |
|---|---|---|
| `app.py` | Kenya Airways PLC Streamlit dashboard (educational) | Pre-existing, untouched |
| `standalone-console.html` | Standalone Expense Console — single-file browser app | **Active work** |
| `docs/GATE-1-HANDOVER.md` | Locked handover for Gate 1 | Locked |

## The console in one paragraph

`standalone-console.html` is one self-contained HTML file. It opens from
`file://` or any static host. No build step, no npm, no API key, no CDN, no
network requests of any kind. It ingests bank CSVs by rule-based parsing,
accepts manual expense entry through a structured form, persists to
`localStorage`, and exports CSV against a locked column contract.

## Hard constraints — never violate these

1. **One file.** Everything lives in `standalone-console.html`. No separate
   `.css`, `.js`, or asset files. No bundler.
2. **Zero network.** No CDN `<script>` tags, no `fetch`, no fonts, no
   analytics. The file must work fully offline, opened by double-click. This
   is why the CSV parser is hand-written instead of PapaParse.
3. **No API key, no LLM call.** All parsing and categorisation is rule-based
   and deterministic. Same input, same output, every time.
4. **No `window.storage`.** That is a claude.ai artifact API and does not
   exist outside it. Use the `Store` module (§1) only.
5. **The column contract has exactly one definition** — `DEFAULT_CONTRACT`
   in §0, plus whatever the user has adopted into `localStorage`. Export code
   reads the contract; it never hardcodes column names.
6. **No silent row loss.** Every source row on import lands in either
   `imported[]` or `skipped[]` with a stated reason, and the reconciliation
   line is shown in the UI. If the counts don't add up, say so in the
   interface — do not present totals as complete.

## Code layout inside the file

The `<script>` block is sectioned. Keep the sections; add to them.

```
§0  Column contract      — FIELDS, DEFAULT_CONTRACT, SCHEMA_VERSION
§1  Store                — localStorage wrapper (swap point for IndexedDB)
§2  CSV read/write       — RFC4180 parser, CSV writer, download helper
§3  Column detection     — header finding, parseAmount, parseDate
§4  Categorisation       — CAT_KEYWORDS, categorise()
§5  Import pipeline      — importCSVText(), reconciliation, render
§6  Manual entry         — form handling
§7  Ledger               — table, filter, KPIs, delete
§8  Export               — contract-driven CSV, JSON backup/restore
§9  Contract tab         — reference-file diff, adopt header
§10 Boot                 — drag/drop wiring, tabs, refreshAll()
```

## The gate loop

Work proceeds in gates. One gate per session.

1. Read the locked handover docs in `docs/`.
2. Propose the design for the gate. **Build nothing until the user confirms.**
3. Build the gate's scope into `standalone-console.html`.
4. Validate — for parser work, against the reference export CSV.
5. Lock: write `docs/GATE-N-HANDOVER.md`, commit, open the next gate.

### Gate status

- **Gate 1 — Data model, ingest, persistence, export contract.** Built.
  Contract is *provisional* pending validation against the reference export.
  See `docs/GATE-1-HANDOVER.md`.
- **Gate 2 — not opened.**

## Known open item carried into Gate 2

The reference export `Simplified_Expenses_RUN20260711587.csv` (60 rows, 6
fields) and `ExtractionConsole.jsx` are **not in this repo** — they live in a
claude.ai project, and claude.ai project files do not transfer into a Claude
Code session. The 6-column contract in §0 is therefore a documented
best-guess.

The console works around this: the Contract tab accepts the reference CSV,
diffs its header against the contract, and adopts it in one click. Until that
adoption happens, the Contract tab shows a "provisional" banner. **Do not
treat the export contract as validated until that banner turns green.**

If you want the contract baked into the source rather than held in
`localStorage`, edit `DEFAULT_CONTRACT` in §0 to match — that is the only
place it needs to change.

## Testing

There is no test runner. Validate by opening the file in a browser:

```bash
python3 -m http.server 8000    # then open http://localhost:8000/standalone-console.html
```

Or just double-click the file. Round-trip check: import a CSV → export CSV →
re-import the export → row counts and totals must match.

## Git

Develop on `claude/standalone-expense-console-ls22db`. Do not touch `app.py`.
