"""Regenerate every manuscript figure (no QPU or Aer job is run).

    python run/figures/make_all.py [--skip-cache]

1. replay_training.py      bit-exact offline replay of the recorded hardware/emulator runs and of the
                           classical control -> data/derived/learning_curves.npz           (~20 s)
2. simulate_same_budget.py HQPINN ideal / ideal + shot noise at the hardware budget
                           -> data/derived/same_budget_sims.npz                           (~10 s)
3. controls_hardware_budget.py  classical LR sweep and sine middle block at the hardware budget
                           -> data/derived/controls_hardware_budget.npz  (~40 s; reused if present)
4. the figure scripts      -> paper/figures/*.pdf and *.png
"""

# --- repository layout: src/ and run/ go on the import path, and relative paths
# --- such as "data/..." are resolved from the repository root.
import os as _os
import sys as _sys
from pathlib import Path as _Path

_HERE = _Path(__file__).resolve().parent if "__file__" in globals() else _Path.cwd()
_ROOT = next(p for p in (_HERE, *_HERE.parents) if (p / "src").is_dir() and (p / "run").is_dir())
for _p in (_ROOT / "run", _ROOT / "src", _ROOT / "src" / "quantum_hardware", _HERE):
    if str(_p) not in _sys.path:
        _sys.path.insert(0, str(_p))
_os.chdir(_ROOT)
# ---------------------------------------------------------------------------------

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = ["replay_training.py", "simulate_same_budget.py", "controls_hardware_budget.py"]
FIGURES = ["fig2_simulations.py", "fig3_hardware.py", "fig4_noise_ladder.py", "fig5_device_model.py",
           "figS1_exact_ncol.py"]

if __name__ == "__main__":
    scripts = FIGURES if "--skip-cache" in sys.argv else CACHE + FIGURES
    for name in scripts:
        print(f"--- {name}", flush=True)
        subprocess.run([sys.executable, str(HERE / name)], check=True, cwd=HERE)
