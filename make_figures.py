"""
Paper figure (free-game trade-off) for the LNCS text width of 12.2 cm.

Standalone: reads the results JSON files directly and needs only matplotlib and pandas.
No title (the LaTeX caption says what the figure shows), vector PDF, 8 pt fonts, and
markers and a dark-to-light colour scale that still read in greyscale.

Usage:
    python make_figures.py [results.json] [results_fixedbase.json] [output_dir]

Defaults: Results/results.json, Results/results_fixedbase.json, figures
"""
import json
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LogNorm, LinearSegmentedColormap

TEXT_W = 12.2 / 2.54          # LNCS text width in inches
HIT_TARGET = 2.7              # free hit rate, "1 in X"
RETRIGGER_TARGET = 60.0       # retrigger rate, "1 in X"

plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "legend.fontsize": 7,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "axes.linewidth": 0.6,
    "lines.linewidth": 1.3, "pdf.fonttype": 42, "ps.fonttype": 42,
    "axes.spines.top": False, "axes.spines.right": False,
})


def load_free_runs(path, source):
    """One row per free-stage run with a re-evaluated final value, random search excluded.

    File layout: raw["seed_<n>_free"]["results"]["mutation_<m>"]["<Strategy>_<Selection>"],
    and each run's final re-evaluation is its "bestSpin" entry with source "finalCheck".
    """
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    rows = []
    for seed, seed_entry in raw.items():
        if not re.fullmatch(r"seed_\d+_free", seed):
            continue
        for mut_key, combos in seed_entry["results"].items():
            if not re.fullmatch(r"mutation_\d+", mut_key):
                continue
            for combo, entry in combos.items():
                strategy, selection = combo.split("_", 1)
                best = entry.get("bestSpin") or {}
                if strategy == "RandomSearch" or best.get("source") != "finalCheck" \
                        or best.get("fitness") is None:
                    continue
                sim = best["simOutput"]
                rows.append({
                    "source": source, "seed": seed, "mutation": int(mut_key.split("_")[1]),
                    "strategy": strategy, "selection": selection, "final": float(best["fitness"]),
                    "hit_err": (sim["freeHitRate"] - HIT_TARGET) / HIT_TARGET * 100,
                    "retrigger_err": (sim["freeReTriggerRate"] - RETRIGGER_TARGET) / RETRIGGER_TARGET * 100,
                    "stored_hit_err": best["errorPercent"]["freeHitRate"],
                    "stored_retrigger_err": best["errorPercent"]["freeReTriggerRate"],
                })
    return pd.DataFrame(rows)


def free_tradeoff(main_json, fixed_json, out_dir):
    """Hit-rate error against retrigger-rate error of every final free reel set."""
    d = pd.concat([load_free_runs(main_json, "Own base reels"),
                   load_free_runs(fixed_json, "Fixed base reels")], ignore_index=True)

    # The errors computed here must agree with the ones the optimiser stored (4 decimals).
    worst = max((d.hit_err - d.stored_hit_err).abs().max(),
                (d.retrigger_err - d.stored_retrigger_err).abs().max())
    if worst > 1e-3:
        sys.exit(f"Computed errors differ from the stored errorPercent by up to {worst:.4f}")

    hit_ok = d.hit_err.abs() <= 5
    a = (d.hit_err < -5) & (d.retrigger_err.abs() <= 15)
    b = hit_ok & (d.retrigger_err < -25)

    fig, ax = plt.subplots(figsize=(TEXT_W, 0.5 * TEXT_W))
    norm = LogNorm(vmin=max(d.final.min(), 0.02), vmax=d.final.quantile(0.98))
    cmap = LinearSegmentedColormap.from_list("err", ["#08306b", "#4a7fc1", "#c8c8c8"])
    for tag, marker in (("Own base reels", "o"), ("Fixed base reels", "^")):
        g = d[d.source == tag]
        sc = ax.scatter(g.hit_err, g.retrigger_err, c=g.final, cmap=cmap, norm=norm, s=6,
                        marker=marker, edgecolor="none", alpha=0.8, label=tag)
    ax.axhline(0, color="#555555", lw=0.6)
    ax.axvline(0, color="#555555", lw=0.6)
    ax.scatter([0], [0], marker="*", s=70, color="#D55E00", edgecolor="white", lw=0.6, zorder=5,
               label="Target")
    ax.annotate(f"A: wins too often,\nretrigger on target ({a.mean():.0%})",
                xy=(d[a].hit_err.median(), d[a].retrigger_err.median()),
                xytext=(0.03, 0.97), textcoords="axes fraction", va="top",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", lw=0.5),
                arrowprops=dict(arrowstyle="->", lw=0.6, color="#333333"))
    ax.annotate(f"B: hit rate on target,\nretriggers too often ({b.mean():.0%})",
                xy=(d[b].hit_err.median(), d[b].retrigger_err.median()),
                xytext=(0.36, 0.42), textcoords="axes fraction", va="top",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", lw=0.5),
                arrowprops=dict(arrowstyle="->", lw=0.6, color="#333333"))
    ax.set_xlabel("Free hit-rate error (%), negative = wins more often than 1 in 2.7")
    ax.set_ylabel("Retrigger-rate error (%),\nnegative = more often than 1 in 60")
    cb = fig.colorbar(sc, ax=ax, pad=0.02)
    cb.set_label("Final error (log)")
    cb.outline.set_visible(False)
    ax.legend(loc="lower left", frameon=True, framealpha=0.9, edgecolor="#cccccc", markerscale=1.6)
    fig.tight_layout(pad=0.2)

    print(f"trade-off: {len(d)} reel sets "
          f"({(d.source == 'Own base reels').sum()} own base, {(d.source == 'Fixed base reels').sum()} fixed base), "
          f"A {a.mean():.1%}, B {b.mean():.1%}, error <= 0.25: {(d.final <= 0.25).sum()}")

    os.makedirs(out_dir, exist_ok=True)
    pdf = os.path.join(out_dir, "free_tradeoff.pdf")
    fig.savefig(pdf, metadata={"Creator": None, "Producer": None, "CreationDate": None})
    plt.close(fig)
    print(f"wrote {pdf}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 3:
        sys.exit(__doc__)
    defaults = ["Results/results.json", "Results/results_fixedbase.json", "figures"]
    free_tradeoff(*(args + defaults[len(args):]))
