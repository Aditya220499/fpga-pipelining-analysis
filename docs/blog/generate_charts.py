"""
FPGA Pipelining Analysis — Publication-Quality Charts
Generates 7 Medium-ready PNGs (300 DPI, white background) from measured
Vivado implementation results for a 3-implementation adder-tree pipelining study.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ----------------------------------------------------------------------
# Global style — consistent, professional, Medium-friendly
# ----------------------------------------------------------------------
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "font.family": "DejaVu Sans",
    "font.size": 13,
    "axes.titlesize": 17,
    "axes.titleweight": "bold",
    "axes.labelsize": 13,
    "axes.labelweight": "medium",
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 1.0,
    "axes.grid": True,
    "grid.color": "#dddddd",
    "grid.linewidth": 0.7,
    "grid.alpha": 0.8,
    "axes.axisbelow": True,
})

FIGSIZE = (9, 6)
DPI = 300

# Color palette — one consistent identity per implementation
COLOR_BASE = "#2E4057"      # deep slate blue
COLOR_2STAGE = "#4C8577"    # teal green
COLOR_3STAGE = "#D9822B"    # amber orange
COLOR_ACCENT = "#C1272D"    # accent red (for lines/highlights)
COLOR_LUT = "#2E4057"
COLOR_REG = "#D9822B"

labels = ["Baseline\n(1 stage)", "2-Stage\nPipeline", "3-Stage\nPipeline"]
depths = [1, 2, 3]

luts = [38, 52, 60]
regs = [75, 111, 131]
crit_path = [4.741, 3.381, 1.680]
fmax = [211, 296, 595]
power = [0.094, 0.095, 0.096]
latency = [1, 2, 3]

bar_colors = [COLOR_BASE, COLOR_2STAGE, COLOR_3STAGE]

OUT = "/home/claude/charts"


def style_axes(ax, title, ylabel, xlabel="Pipeline Implementation"):
    ax.set_title(title, pad=14)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel, labelpad=8)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")


def value_labels(ax, xs, ys, fmt="{:.0f}", offset_ratio=0.02, color="#222222"):
    yr = max(ys) - min(ys) if max(ys) != min(ys) else max(ys)
    off = yr * offset_ratio if yr else 0.02
    for x, y in zip(xs, ys):
        ax.text(x, y + off, fmt.format(y), ha="center", va="bottom",
                 fontsize=12, fontweight="bold", color=color)


# ----------------------------------------------------------------------
# 1. Maximum Frequency vs Pipeline Depth
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
ax.plot(depths, fmax, marker="o", markersize=10, linewidth=3,
        color=COLOR_ACCENT, markerfacecolor="white", markeredgewidth=2.5,
        markeredgecolor=COLOR_ACCENT, zorder=3)
ax.fill_between(depths, fmax, min(fmax) - 40, color=COLOR_ACCENT, alpha=0.08)
value_labels(ax, depths, fmax, fmt="{:.0f} MHz")
ax.set_xticks(depths)
ax.set_xticklabels(labels)
ax.set_ylim(150, 650)
style_axes(ax, "Maximum Operating Frequency vs. Pipeline Depth", "Fmax (MHz)")
fig.tight_layout()
fig.savefig(f"{OUT}/1_fmax_vs_pipeline_depth.png", dpi=DPI)
plt.close(fig)

# ----------------------------------------------------------------------
# 2. Critical Path Delay vs Pipeline Depth
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
ax.plot(depths, crit_path, marker="s", markersize=10, linewidth=3,
        color=COLOR_BASE, markerfacecolor="white", markeredgewidth=2.5,
        markeredgecolor=COLOR_BASE, zorder=3)
ax.fill_between(depths, crit_path, 0, color=COLOR_BASE, alpha=0.08)
value_labels(ax, depths, crit_path, fmt="{:.3f} ns")
ax.axhline(10, color="#999999", linestyle="--", linewidth=1.2)
ax.text(1.02, 10.15, "10 ns constraint (100 MHz)", fontsize=10.5,
        color="#666666", ha="left", va="bottom")
ax.set_xticks(depths)
ax.set_xticklabels(labels)
ax.set_ylim(0, 11)
style_axes(ax, "Critical Path Delay vs. Pipeline Depth", "Critical Path (ns)")
fig.tight_layout()
fig.savefig(f"{OUT}/2_critical_path_vs_pipeline_depth.png", dpi=DPI)
plt.close(fig)

# ----------------------------------------------------------------------
# 3. Resource Utilization (Grouped Bar Chart: LUTs vs Registers)
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
x = np.arange(len(labels))
width = 0.35
b1 = ax.bar(x - width/2, luts, width, label="Slice LUTs", color=COLOR_LUT,
            edgecolor="white", linewidth=0.8, zorder=3)
b2 = ax.bar(x + width/2, regs, width, label="Slice Registers", color=COLOR_REG,
            edgecolor="white", linewidth=0.8, zorder=3)
for bars, vals in [(b1, luts), (b2, regs)]:
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                 str(v), ha="center", va="bottom", fontsize=11.5, fontweight="bold")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(0, 150)
style_axes(ax, "Resource Utilization by Pipeline Depth", "Count")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(f"{OUT}/3_resource_utilization.png", dpi=DPI)
plt.close(fig)

# ----------------------------------------------------------------------
# 4. Power Consumption vs Pipeline Depth
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
bars = ax.bar(labels, [p * 1000 for p in power], color=bar_colors, width=0.5,
              edgecolor="white", linewidth=0.8, zorder=3)
value_labels(ax, range(len(labels)), [p * 1000 for p in power], fmt="{:.0f} mW",
             offset_ratio=0.01)
ax.set_ylim(0, 120)
style_axes(ax, "Total On-Chip Power vs. Pipeline Depth", "Power (mW)")
fig.tight_layout()
fig.savefig(f"{OUT}/4_power_vs_pipeline_depth.png", dpi=DPI)
plt.close(fig)

# ----------------------------------------------------------------------
# 5. Pipeline Latency vs Pipeline Depth
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
bars = ax.bar(labels, latency, color=bar_colors, width=0.5,
              edgecolor="white", linewidth=0.8, zorder=3)
value_labels(ax, range(len(labels)), latency, fmt="{:.0f} cycle" + ("s" if True else ""),
             offset_ratio=0.05)
ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax.set_ylim(0, 4)
style_axes(ax, "Pipeline Latency vs. Pipeline Depth", "Latency (clock cycles)")
fig.tight_layout()
fig.savefig(f"{OUT}/5_latency_vs_pipeline_depth.png", dpi=DPI)
plt.close(fig)

# ----------------------------------------------------------------------
# 6. Frequency Improvement Percentage (relative to baseline)
# ----------------------------------------------------------------------
improvement = [0.0, (fmax[1] - fmax[0]) / fmax[0] * 100, (fmax[2] - fmax[0]) / fmax[0] * 100]
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
bars = ax.bar(labels, improvement, color=bar_colors, width=0.5,
              edgecolor="white", linewidth=0.8, zorder=3)
value_labels(ax, range(len(labels)), improvement, fmt="+{:.1f}%", offset_ratio=0.02)
ax.set_ylim(0, 200)
style_axes(ax, "Frequency Improvement Relative to Baseline", "Improvement (%)")
fig.tight_layout()
fig.savefig(f"{OUT}/6_frequency_improvement_percentage.png", dpi=DPI)
plt.close(fig)

# ----------------------------------------------------------------------
# 7. Engineering Summary Infographic
# ----------------------------------------------------------------------
fig = plt.figure(figsize=(12, 8), dpi=DPI)
gs = fig.add_gridspec(2, 3, hspace=0.55, wspace=0.4,
                       left=0.07, right=0.96, top=0.86, bottom=0.10)

fig.suptitle("FPGA Pipelining Experiment — Engineering Summary",
             fontsize=20, fontweight="bold", y=0.965, color="#1a1a1a")
fig.text(0.5, 0.925,
         "Same algorithm. Same FPGA. Same constraint. Only register placement changed.",
         ha="center", fontsize=12.5, color="#555555", style="italic")

# Fmax mini
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(depths, fmax, marker="o", color=COLOR_ACCENT, linewidth=2.5, markersize=7)
ax1.set_title("Fmax (MHz)", fontsize=13, fontweight="bold")
ax1.set_xticks(depths); ax1.set_xticklabels(["B", "2S", "3S"], fontsize=10)
value_labels(ax1, depths, fmax, fmt="{:.0f}", offset_ratio=0.04)
for s in ["top", "right"]: ax1.spines[s].set_visible(False)

# Critical path mini
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(depths, crit_path, marker="s", color=COLOR_BASE, linewidth=2.5, markersize=7)
ax2.set_title("Critical Path (ns)", fontsize=13, fontweight="bold")
ax2.set_xticks(depths); ax2.set_xticklabels(["B", "2S", "3S"], fontsize=10)
value_labels(ax2, depths, crit_path, fmt="{:.2f}", offset_ratio=0.04)
for s in ["top", "right"]: ax2.spines[s].set_visible(False)

# Resources mini
ax3 = fig.add_subplot(gs[0, 2])
xw = np.arange(3); w = 0.35
ax3.bar(xw - w/2, luts, w, color=COLOR_LUT, label="LUT")
ax3.bar(xw + w/2, regs, w, color=COLOR_REG, label="Reg")
ax3.set_title("LUTs vs Registers", fontsize=13, fontweight="bold")
ax3.set_xticks(xw); ax3.set_xticklabels(["B", "2S", "3S"], fontsize=10)
ax3.legend(fontsize=8.5, frameon=False, loc="upper left")
for s in ["top", "right"]: ax3.spines[s].set_visible(False)

# Power mini
ax4 = fig.add_subplot(gs[1, 0])
ax4.bar(labels, [p*1000 for p in power], color=bar_colors, width=0.55)
ax4.set_title("Power (mW)", fontsize=13, fontweight="bold")
ax4.set_xticklabels(["B", "2S", "3S"], fontsize=10)
ax4.set_ylim(0, 120)
value_labels(ax4, range(3), [p*1000 for p in power], fmt="{:.0f}", offset_ratio=0.02)
for s in ["top", "right"]: ax4.spines[s].set_visible(False)

# Latency mini
ax5 = fig.add_subplot(gs[1, 1])
ax5.bar(labels, latency, color=bar_colors, width=0.55)
ax5.set_title("Latency (cycles)", fontsize=13, fontweight="bold")
ax5.set_xticklabels(["B", "2S", "3S"], fontsize=10)
ax5.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax5.set_ylim(0, 4)
value_labels(ax5, range(3), latency, fmt="{:.0f}", offset_ratio=0.08)
for s in ["top", "right"]: ax5.spines[s].set_visible(False)

# Key takeaway panel
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis("off")
takeaway = (
    "KEY RESULT\n\n"
    "2.8x Fmax gain\n"
    "211 -> 595 MHz\n\n"
    "72% shorter\ncritical path\n\n"
    "Power flat\n"
    "94 -> 96 mW\n\n"
    "Cost: +3 cycles\nlatency, +56 regs"
)
ax6.text(0.02, 0.98, takeaway, fontsize=11.5, va="top", ha="left",
          linespacing=1.6, color="#1a1a1a",
          bbox=dict(boxstyle="round,pad=0.6", facecolor="#F5F0E6",
                     edgecolor=COLOR_ACCENT, linewidth=1.5))

fig.savefig(f"{OUT}/7_engineering_summary_infographic.png", dpi=DPI)
plt.close(fig)

print("All 7 charts generated successfully.")
