# Forward problem: hybrid quantum PINN for the viscous Burgers equation

Code, data and manuscript for training a **hybrid quantum physics-informed neural network (HQPINN)**,
a PINN with a fixed (non-variational) quantum layer, on the forward problem
u_t + u u_x = ν u_xx, and for running that training with a superconducting quantum processor
(`ibm_berlin`) in the loop.

Main results (details in `paper/` and `docs/`):

- **Same-protocol simulations (n = 10 qubits / neurons).** Both models reach the finite-difference
  floor at T = 0.1. The HQPINN reaches the physical target in 100 % of runs versus 64 %, in about half
  the optimizer steps, with 271 versus 491 parameters.
- **Real QPU.** Trained with `ibm_berlin` in the loop (110 epochs, no error mitigation), the HQPINN
  reaches a relative L2 error of 5.7 % (MSE 1.45 × 10⁻³). A classical PINN trained with the same
  protocol has a median of 24.7 %.

## Repository layout

```text
forward-problem-hqpinn/
├── src/                     shared library code
│   ├── main/                PINN models, quantum circuits, physics, training loops
│   ├── Inverser_quantum_hardware_pinn.py      hardware machinery (qubit chains, calibration surrogate)
│   ├── Inverser_quantum_exact_pinn_paralelo.py exact quantum layer and finite-difference residual
│   └── paths.py             repository paths + save_figure()
├── run/                     everything you execute
│   ├── requirements.txt
│   ├── run_classical.py, run_qubit_sweep.py, run_classical_vs_qpu.py   simulations
│   ├── run_quantum_hardware*.py, run_quantum_ibm_faker.py, search_optimizer_ibm_faker.py  QPU / FakeBerlin
│   ├── figures/             the manuscript figures (make_all.py regenerates them)
│   └── plots/               exploratory plots
├── data/                    results read by the scripts and the paper
│   ├── Forward/             simulation sweeps
│   ├── quantum_forward_hardware_real/   training on ibm_berlin
│   └── derived/             intermediate results for the figures (replayed training, same-budget sims)
├── paper/                   LaTeX manuscript, synced with Overleaf
│   ├── main.tex, references.bib
│   └── figures/             written by run/figures/*.py
├── docs/                    working notes in Portuguese (results report, manuscript notes)
└── .github/                 Overleaf sync workflow
```

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r run/requirements.txt

python run/figures/make_all.py             # all manuscript figures -> paper/figures/
python run/figures/make_all.py --skip-cache  # figures only, reusing data/derived/
python run/run_qubit_sweep.py              # example: a simulation sweep
```

Scripts can be started from any folder. Each one puts `src/` and `run/` on the import path and
resolves `data/...` from the repository root, so `python run/X.py` and `cd run && python X.py` behave
the same.

## Figures go straight into the paper

Every plotting script writes its PDF into `paper/figures/`, the folder that LaTeX reads and that is
synced with Overleaf. For new plots, use the helper in `src/paths.py`:

```python
from paths import save_figure

fig, ax = plt.subplots()
...
save_figure(fig, "fig6_new_result")   # -> paper/figures/fig6_new_result.pdf (+ a local .png preview)
```

Then `\includegraphics{fig6_new_result.pdf}` in `paper/main.tex`. Commit and push, and the figure
appears in Overleaf.

## Paper and Overleaf

`paper/` is synced in both directions with the Overleaf project through Overleaf's Git integration
(`.github/workflows/overleaf-sync.yml`):

| Direction | When |
|---|---|
| GitHub → Overleaf | every push to `main` that changes `paper/` |
| Overleaf → GitHub | every 3 hours, or right away from **Actions → Overleaf sync → Run workflow** |

Edits to different parts of the text on both sides are merged automatically. If the same lines were
edited in both places, the run stops and puts the Overleaf version on the branch `overleaf-conflict`.
Merge that branch into `main`, push, and the sync completes.

**One-time setup:** in Overleaf, open *Account Settings → Git integration* and generate a token. Here,
open *Settings → Secrets and variables → Actions → New repository secret*, name it `OVERLEAF_TOKEN` and
paste the token. Tokens expire after one year; replace the secret then. The Overleaf project id is set
in the workflow file.

On the first run, if the Overleaf project already holds a different version of the paper, nothing is
overwritten. The Overleaf version is saved on the branch `overleaf-initial` and the run asks you to
choose: run the workflow again with `first_sync = github` or `overleaf`.

## Data

All result files the scripts and the paper read are included (under 100 MB), with two exceptions:

- **Per-epoch loss histories of the large classical sweeps** (`data/Forward/classical*/**/losshist_*.npz`,
  about 2 GB). Each of those folders has a `histories_summary.csv` with every run's final and minimum
  values. The full histories are in [GubioGL/CBPF-Geral](https://github.com/GubioGL/CBPF-Geral);
  `bash data/fetch_full_histories.sh` copies them back into place.
- **Files kept on your own machine:** `src/quantum_hardware/` (with `regression_hardware_nqubits.py`) and
  `data/quantum_ibm_faker/` (the FakeBerlin runs). The hardware scripts and Figs. 3–5 need them; copy
  them into those paths to run those parts. `src/quantum_hardware/` is git-ignored.

## Origin

Split from [GubioGL/CBPF-Geral](https://github.com/GubioGL/CBPF-Geral) (commit `5776ab2`), which keeps
the full history and serves as the archive. The inverse problem lives in
[GubioGL/inverse-problem-hqpinn](https://github.com/GubioGL/inverse-problem-hqpinn).
