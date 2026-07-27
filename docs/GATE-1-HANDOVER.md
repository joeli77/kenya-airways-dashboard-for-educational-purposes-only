# Gate 1 — Handover

**Status:** Built and tested. Export contract *provisional* — see §5.
**Deliverable:** `standalone-console.html` (single file, ~700 lines incl. CSS + JS)

---

## §1 — Internal data model

Every row in the ledger is this shape. This is the console's own model, not the
export shape — the two are deliberately separate.

| Field | Type | Notes |
|---|---|---|
| `id` | string | `exp_<base36>_<rand>`, generated locally |
| `date` | string | **ISO `YYYY-MM-DD`**, always. Normalised on import. |
| `description` | string | Falls back to `(no description)` |
| `category` | string | From the file's own category column if present, else keyword-derived |
| `payee` | string | Blank on import (Gate 2 candidate: payee extraction) |
| `amount` | number | **Expenses positive, money-in negative.** 2dp on export. |
| `source` | string | Source filename, or `Manual` |
| `confidence` | `high` \| `inferred` \| `verify` | Surfaced as a coloured chip |
| `origin` | `import` \| `manual` | |
| `notes` | string | Manual entry only |
| `createdAt` / `updatedAt` | ISO datetime | |
| `raw` | object | The original CSV row, keyed by its own headers — audit trail |

`raw` is kept so any import decision can be traced back to the source row. It
goes into the JSON backup and never into the CSV export.

## §2 — Export contract

CSV export is driven **entirely** by `CONTRACT`, never by hardcoded names.

```js
{ version: 1,
  columns: [ { column: "Date",        field: "date"        },
             { column: "Description", field: "description" },
             { column: "Category",    field: "category"    },
             { column: "Payee",       field: "payee"       },
             { column: "Amount",      field: "amount"      },
             { column: "Source",      field: "source"      } ] }
```

Guarantees:

- Columns are written in contract order, always, even when every value is blank.
- `amount` is always `toFixed(2)` — no locale separators, no currency symbol.
- Fields containing `,` `"` or a newline are RFC4180-quoted; inner quotes doubled.
- Line terminator is `\r\n`.
- **Row order is date ascending**, tie-broken by `createdAt`. The same ledger
  always produces a byte-identical file.
- A column mapped to `""` exports as empty — the column still appears.

Filename: `Simplified_Expenses_YYYYMMDD.csv`.

JSON backup is separate and lossless: `{ schemaVersion, exportedAt, contract,
rowCount, rows }` including `raw`, `id`, `confidence`. Restore replaces the
ledger and adopts the contract stored in the backup.

## §3 — Import rules

1. Read the file with a hand-written RFC4180 parser (no PapaParse — the file
   must work offline). Each parsed row keeps a `.line` property pointing at its
   **real line in the source file**, so blank lines don't shift the reporting.
2. Scan the first 25 rows and score each against known column patterns; the
   best-scoring row is the header. This is what skips bank statement preamble.
3. Detect `date` / `description` / `debit` / `credit` / `amount` / `category`
   columns by substring match, case-insensitive.
4. Per row, in order — a row is **skipped with a stated reason** if any fails:
   - `^Total` in the date or description column → *totals row*
   - no debit, credit or signed amount → *no amount found*
   - it's a credit and "include credits" is off → *credit (money in) — excluded*
   - date unparseable → *unreadable date: `<value>`*
5. Categorise: credits → `Revenue / Receipts`; debits by Kenya keyword table;
   no match → `Overheads & Operations` + `verify` confidence.

Date parsing is **day-first** (`19/01/2025` → 19 Jan). Handles `DD-Mon-YY`
(NCBA), `DD/MM/YYYY`, and ISO. Amounts handle thousands separators, currency
prefixes, and `(1,200.00)` as negative.

**Reconciliation is mandatory and visible.** `imported + skipped` must equal the
source row count; the UI shows a green "Reconciled" banner or a red "MISMATCH"
banner, and every skipped row is listed with its file line and reason.

## §4 — Persistence

`localStorage`, behind a `Store` module (§1 of the source). Keys `sec.rows.v1`
and `sec.contract.v1`. If `localStorage` is blocked — Safari on `file://` — the
console falls back to memory and shows a red banner telling the user to export a
backup. It does not silently pretend data is saved.

IndexedDB was not needed at Gate 1 volumes. `Store` is the only place that would
change.

## §5 — Open item carried to Gate 2 ⚠️

`ExtractionConsole.jsx` and `Simplified_Expenses_RUN20260711587.csv` are **not
in this repo** — they're claude.ai project files, which don't transfer into a
Claude Code session. The six columns above are a documented best-guess.

**To close this:** open the console → tab 5 (Contract) → drop the reference CSV
on the second panel. It diffs the header against the contract and, if they
differ, offers one-click adoption with automatic field mapping. The banner turns
from amber "Provisional" to green "Custom contract in force".

Until that happens, treat the export contract as unvalidated.

## §6 — Verification performed

Two suites, both green, run against a synthetic NCBA-style fixture (preamble
rows, a blank line, quoted fields with embedded commas and quotes, a malformed
row, an unparseable date, and a totals row).

**Logic — 37/37.** RFC4180 edge cases (embedded comma / doubled quote /
embedded newline / BOM), amount parsing, day-first dates, categorisation,
reconciliation, and CSV export round-trip preserving row count and total
(350,621.25).

**Browser (Chromium, `file://`) — 31/31.** Boot with **zero external network
requests** and no JS errors; `localStorage` works from `file://`; import →
reconcile → commit; persistence across reload; manual entry; search filter;
click-row-to-edit; contract-locked download; date-ascending order; quote
escaping; reference-file diff → adopt → export header changes accordingly;
JSON backup → delete all → restore.

Not covered: Excel and PDF ingest (out of Gate 1 scope, CSV only); Safari;
payee extraction.

## §7 — Suggested Gate 2 scope

1. Validate the contract against the real reference file (§5) — **do this first**.
2. Payee/vendor extraction from description text.
3. Excel (`.xlsx`) ingest — needs SheetJS, which conflicts with the zero-CDN
   rule. Decide: vendor the library inline, or keep CSV-only.
4. Duplicate detection across repeat imports of overlapping statement periods.
5. Bulk re-categorisation of `verify`-confidence rows.
