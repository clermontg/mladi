## Purpose

Provide concise, actionable guidance for AI coding agents working in this repository of data-processing scripts.

## Big picture

- **What this repo is**: a collection of standalone Python scripts that process EHR/CSV data and stage it for MySQL import. See [README.md](README.md) for a short overview.
- **Primary pipeline (discoverable):** raw CSVs under `/ix1/mladi/read` -> per-encounter grouping & cleanup (scripts like `CompressRead.py`, `dedup.py`, `dedouble.py`, `Annotate2.py`) -> aggregate CSV outputs written to `/ix1/mladi/work/cler/data` by `DBbuildfromCSV.py` -> bulk import to MySQL via `ImportCSV2SQL.py`.

## Key files to reference

- [reshape_dirs.py](reshape_dirs.py): groups CSVs by their first 15 filename characters, extracts ZIPs in-place, reads source dirs from `/ix1/mladi/work/cler/sourcedirs.csv` and moves files into a dest dir. Example: it expects absolute UNIX paths and uses `shutil.move` semantics.
- [DBbuildfromCSV.py](DBbuildfromCSV.py): concatenates type-specific CSVs (typelist contains `_lab`, `_micro`, `_suscep`, etc.). It builds output files under `/ix1/mladi/work/cler/` and appends to `dumpeddirs.csv` to track processed directories.
- [ImportCSV2SQL.py](ImportCSV2SQL.py): executes several `LOAD DATA LOCAL INFILE` SQL commands (via `pymysql`) to import `_*.csv` files from `/ix1/mladi/work/cler/data` into the `mladi` schema on host `auview.ccm.pitt.edu`. Note the DB user `cler` and use of `local_infile` and string-to-date parsing.
- [README.md](README.md): concise repository-level description — cites core scripts and their responsibilities.

## Patterns & conventions (concrete, repo-specific)

- Scripts are mostly standalone command-line Python scripts (no package layout). Expect to run them with the repository Python (Python 3).
- Many scripts use absolute UNIX-style paths under `/ix1/mladi/...`. Prioritize search/replace of those constants when porting or testing locally.
- Filenames encode type suffixes: `_lab`, `_micro`, `_suscep`, `_patient`, `_demo`, `_ce`, `_cs`, `_med`, `_surg`, etc. See the `typelist` array in `DBbuildfromCSV.py` for the full list.
- `reshape_dirs.py` groups by the filename prefix (first 15 chars). Edits that change grouping logic should update both the grouping code and any downstream assumptions about file naming.
- CSV handling often assumes header-first-line and concatenates lines verbatim (e.g., `DBbuildfromCSV.py` writes all non-header lines into type files). Be careful when changing newline/encoding behavior.
- Database import scripts rely on carefully crafted `LOAD DATA` SQL strings with local variables (e.g., `@dat`, `@Vdate`) and `str_to_date` usage — preserve the SQL shape when refactoring.

## How to run (examples)

- Run a single script locally (example):

```
python reshape_dirs.py /some/destination/path
```

- Build CSV outputs for DB import (existing workflow derived from README):
  1. Prepare /ix1/mladi/read with per-encounter folders.
 2. Run cleanup/packaging scripts (e.g., `CompressRead.py`, `dedup.py`) as needed.
 3. Run `DBbuildfromCSV.py` to produce `_*.csv` under `/ix1/mladi/work/cler/data`.
 4. Run `ImportCSV2SQL.py` (requires `pymysql` and DB access) to load into MySQL.

## Dependencies (detectable from imports)

- `pandas` (used in `DBbuildfromCSV.py`), `pymysql` (used in `ImportCSV2SQL.py`), stdlib modules: `csv`, `zipfile`, `shutil`, `os`, `glob`, `collections`.

## Important integration points & gotchas

- Hard-coded absolute paths and hostnames: `/ix1/mladi/...` and `auview.ccm.pitt.edu` (DB). Confirm environment access before running import scripts.
- No tests or CI present — changes should be validated on a small subset of data first.
- Many scripts assume data hygiene (e.g., consistent headers). When modifying parsing, add a small validation step to avoid silent corruptions.

## Guidance for AI coding agents (how to be productive quickly)

- Start with `README.md` and the three central scripts: `reshape_dirs.py`, `DBbuildfromCSV.py`, `ImportCSV2SQL.py` to understand the dataflow.
- For changes that affect file paths or DB details, update the absolute paths and document where they are defined (`/ix1/mladi/work/cler/sourcedirs.csv`, variables near top of `ImportCSV2SQL.py`).
- When editing CSV logic, include a small, data-driven unit or a short-run script demonstrating the transform on 1–3 sample files.
- Preserve SQL `LOAD DATA` variants and date parsing unless migrating the import step to a different mechanism; tests should confirm row counts before/after import.

## When to ask the repo owner

- If you need DB credentials or a testing subset of `/ix1/mladi/read` data.
- If you plan to change the on-disk layout (paths under `/ix1/mladi`), confirm the intended production mount points.

---
If any of these sections are unclear or you'd like me to include additional, specific examples (e.g., annotate exact lines to change in `ImportCSV2SQL.py`), tell me which area to expand.
