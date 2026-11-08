"""
Paper figure (Fig. 2, free-game trade-off) for the EvoApplications submission (LNCS text width 12.2 cm).

Uses the repo's own loader (Optimizer/Stats/Compare.py) so the data handling is
identical to the published charts; only the styling changes: no titles (the
LaTeX caption says what the figure shows), vector PDF, 8 pt fonts, and line
styles / markers that still read in greyscale.

Usage (from the repo root):
    python paper/make_figures.py Results/results.json Results/results_fixedbase.json paper/figures
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "Optimizer", "Stats"))
import Compare as C  # noqa: E402

TEXT_W = 12.2 / 2.54          # LNCS text width in inches
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
    "lines.linewidth": 1.3, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})

# (label, colour, line style, marker) - colour-blind safe and distinct in greyscale
STYLE = {
    "SteadyState":          ("Steady-state GA",        "#0072B2", "-",              "o"),
    "ElistismGenerational": ("Elitist generational GA", "#E69F00", "--",             "s"),
    "Generational":         ("Generational GA",        "#009E73", ":",              "^"),
    "HillClimbing":         ("Hill climbing",          "#CC79A7", "-.",             "D"),
    "SimulatedAnnealing":   ("Simulated annealing",    "#000000", (0, (5, 1, 1, 1)), "v"),
    "RandomSearch":         ("Random search",          "#999999", (0, (1, 1)),      None),
}
ORDER = list(STYLE)

def free_tradeoff(both_json, fixed_json, out_dir):
    """Free stage: hit-rate error vs retrigger-rate error of every final free reel set."""
    frames = []
    for tag, path in (("Own base reels", both_json), ("Fixed base reels", fixed_json)):
        d, _ = C.load(path, "free")
        d = d[(d.strategy != "RandomSearch") & d.final_check.notna()]
        frames.append(d.assign(source=tag))
    import pandas as pd
    d = pd.concat(frames, ignore_index=True).dropna(subset=["err_freeHitRate", "err_freeReTriggerRate"])
    hit_ok = d.err_freeHitRate.abs() <= 5
    a = (~hit_ok) & (d.err_freeHitRate < 0) & (d.err_freeReTriggerRate.abs() <= 15)
    b = hit_ok & (d.err_freeReTriggerRate < -25)

    fig, ax = plt.subplots(figsize=(TEXT_W, 0.5 * TEXT_W))
    norm = LogNorm(vmin=max(d.final.min(), 0.02), vmax=d.final.quantile(0.98))
    for tag, mk in (("Own base reels", "o"), ("Fixed base reels", "^")):
        g = d[d.source == tag]
        sc = ax.scatter(g.err_freeHitRate, g.err_freeReTriggerRate, c=g.final, cmap=LinearSegmentedColormap.from_list("err", ["#08306b", "#4a7fc1", "#c8c8c8"]),
                        norm=norm, s=6, marker=mk, edgecolor="none", alpha=0.8, label=tag)
    ax.axhline(0, color="#555555", lw=0.6)
    ax.axvline(0, color="#555555", lw=0.6)
    ax.scatter([0], [0], marker="*", s=70, color="#D55E00", edgecolor="white", lw=0.6, zorder=5,
               label="Target")
    ax.annotate(f"A: wins too often,\nretrigger on target ({a.mean():.0%})",
                xy=(d[a].err_freeHitRate.median(), d[a].err_freeReTriggerRate.median()),
                xytext=(0.03, 0.97), textcoords="axes fraction", va="top",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", lw=0.5),
                arrowprops=dict(arrowstyle="->", lw=0.6, color="#333333"))
    ax.annotate(f"B: hit rate on target,\nretriggers too often ({b.mean():.0%})",
                xy=(d[b].err_freeHitRate.median(), d[b].err_freeReTriggerRate.median()),
                xytext=(0.36, 0.42), textcoords="axes fraction", va="top",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", lw=0.5),
                arrowprops=dict(arrowstyle="->", lw=0.6, color="#333333"))
    ax.set_xlabel("Free hit-rate error (%), negative = wins more often than 1 in 2.7")
    ax.set_ylabel("Retrigger-rate error (%),\nnegative = more often than 1 in 60")
    cb = fig.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label("Final error (log)")
    cb.outline.set_visible(False)
    ax.legend(loc="lower left", frameon=True, framealpha=0.9, edgecolor="#cccccc", markerscale=1.6)
    fig.tight_layout()
    print(f"[paper] trade-off: {len(d)} reel sets, A {a.mean():.1%}, B {b.mean():.1%}, "
          f"error <= 0.25: {(d.final <= 0.25).sum()}")
    return _save(fig, out_dir, "free_tradeoff")


def _save(fig, out_dir, name):
    os.makedirs(out_dir, exist_ok=True)
    pdf = os.path.join(out_dir, name + ".pdf")
    fig.savefig(pdf, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(os.path.join(out_dir, name + ".png"), dpi=200, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"[paper] wrote {pdf}")
    return pdf


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    base_json, fixed_json, out = sys.argv[1:]
    free_tradeoff(base_json, fixed_json, out)
