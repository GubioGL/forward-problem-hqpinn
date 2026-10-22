# Notes for Claude

Forward problem of the HQPINN project (viscous Burgers equation, fixed quantum layer, `ibm_berlin` in the loop).
The author writes notes in Portuguese; code comments and the paper are in English.

## Layout rules
- `src/` = importable library (`main/` package, hardware core, `paths.py`). `run/` = entry points; they may import each other.
- Every script in `run/` starts with the repository header block (puts `run/`, `src/`, `src/quantum_hardware/`
  and the script's own folder on `sys.path`, then `chdir`s to the repo root). Keep it when adding scripts.
- Figures: always write to `paper/figures/` as PDF, via `paths.save_figure(fig, name)` or
  `run/figures/paper_common.save`. Never commit PNGs (they are git-ignored local previews).
- Manuscript figures are built by `run/figures/make_all.py`; intermediate results live in `data/derived/`.

## Paper / Overleaf
- `paper/` is synced two-way with Overleaf project `6ad4df833716c9db1f4aabee` by
  `.github/workflows/overleaf-sync.yml` (script: `.github/scripts/overleaf_sync.sh`, state in
  `.github/overleaf-sync-state` — do not edit by hand).
- To change the paper: edit `paper/` and push to `main`; the workflow pushes to Overleaf.
- Branch `overleaf-conflict` = unresolved same-line edits; merge it into `main` and push.

## Not in the repository
- `src/quantum_hardware/regression_hardware_nqubits.py` and `data/quantum_ibm_faker/` (local only, user's machine).
  Hardware scripts, `run/figures/fig3`–`fig5`, `replay_training.py`, `simulate_same_budget.py` need them.
- `losshist_*.npz` of `data/Forward/classical*` (4 GB total with the inverse ones): `data/fetch_full_histories.sh`.
  Use the `histories_summary.csv` in each folder for final values.

## Before claiming a manuscript number
Check it against the data (`docs/manuscript_notes_pt.md` lists the verified numbers and open issues).
