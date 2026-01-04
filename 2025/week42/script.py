# -*- coding: utf-8 -*-
# Bar charts with a bottom, wide, 3-column legend that spans figure width.
# The legend is placed outside the axes and will not shade the x-axis.

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from itertools import cycle

# -----------------------------
# Data (efficiency + short configuration)
# -----------------------------

# VGG16 (Table 1)
vgg16_eff = [7.68, 6.51, 6.75, 3.52, 1.27, 1.31, 0.52, 0.43, 0.37, 0.49, 0.53, 0.64, 0.64]
vgg16_cfg = [
    "Cin=64 Hin=Win=32",
    "Cin=64 Hin=Win=16",
    "Cin=128 Hin=Win=16",
    "Cin=128 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=4",
    "Cin=512 Hin=Win=4",
    "Cin=512 Hin=Win=4",
    "Cin=512 Hin=Win=2",
    "Cin=512 Hin=Win=2",
    "Cin=512 Hin=Win=2",
    "Cin=512 Hin=Win=1",
]

# ResNet-19 (Table 2)
resnet19_eff = [6.64, 6.24, 6.52, 6.01, 6.64, 6.60, 4.17, 1.43, 0.82, 0.69, 0.56, 0.49, 0.55, 0.47, 0.55, 0.32]
resnet19_cfg = [
    "Cin=64 Hin=Win=32",
    "Cin=128 Hin=Win=16",
    "Cin=128 Hin=Win=16",
    "Cin=128 Hin=Win=16",
    "Cin=128 Hin=Win=16",
    "Cin=128 Hin=Win=16",
    "Cin=128 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=8",
    "Cin=256 Hin=Win=4",
    "Cin=512 Hin=Win=4",
    "Cin=512 Hin=Win=4",
    "Cin=512 Hin=Win=4",
]

# -----------------------------
# Color assignment: one color per UNIQUE configuration
# -----------------------------
def colors_by_config(config_list):
    """Map identical configs to the same color; different configs to different colors."""
    unique_cfgs = list(dict.fromkeys(config_list))  # preserves first-seen order
    base_colors = plt.get_cmap("tab20").colors      # up to 20 distinct colors
    color_cycle = cycle(base_colors)
    cfg_to_color = {cfg: next(color_cycle) for cfg in unique_cfgs}
    return [cfg_to_color[cfg] for cfg in config_list], cfg_to_color

# -----------------------------
# Plot function
# -----------------------------
def plot_eff_hist(eff, cfg, outfile):
    """
    Bar chart of efficiency by layer index with a large, bottom legend.
    The legend spans the full figure width in 3 columns and sits below the axes.
    """
    idx = list(range(len(eff)))
    bar_colors, cfg_to_color = colors_by_config(cfg)

    # Use a moderately wide figure; no title per request
    fig, ax = plt.subplots(figsize=(8.5, 3.2))

    # Bars
    ax.bar(idx, eff, color=bar_colors)

    # Axis labels
    ax.set_xlabel("Layer Index")
    ax.set_ylabel("Efficiency")  # simplified y-axis title per request

    # X ticks for every layer index
    ax.set_xticks(idx)
    ax.set_xticklabels(idx)

    # Light horizontal grid for readability
    ax.grid(axis='y', linestyle='--', linewidth=0.6, alpha=0.6)

    # Build legend entries (unique configurations only)
    legend_handles = [Patch(facecolor=color, edgecolor='none') for color in cfg_to_color.values()]
    legend_labels  = list(cfg_to_color.keys())

    # Figure-level legend BELOW the axes, full-width box, 3 columns, large font
    # mode='expand' makes the legend entries stretch to the width of the bbox.
    fig.legend(
        legend_handles, legend_labels,
        loc='upper left',                 # anchor to the upper-left corner of the bbox
        bbox_to_anchor=(0.0, -0.02, 1.0, 0.01),  # (x, y, width, height) in figure coords
        ncol=3, mode='expand',
        frameon=False,
        fontsize=12,                      # make legend text bigger
        handlelength=1.6, handletextpad=0.6, columnspacing=1.6, borderaxespad=0.0
    )

    # Save tightly, trimming whitespace and including the bottom legend in the bbox
    fig.savefig(outfile, bbox_inches='tight', pad_inches=0.02, dpi=300)
    plt.close(fig)

# -----------------------------
# Generate figures
# -----------------------------
plot_eff_hist(
    vgg16_eff, vgg16_cfg,
    outfile="vgg16_efficiency_hist_by_layer.pdf"
)

plot_eff_hist(
    resnet19_eff, resnet19_cfg,
    outfile="resnet19_efficiency_hist_by_layer.pdf"
)

print("Saved: vgg16_efficiency_hist_by_layer.pdf")
print("Saved: resnet19_efficiency_hist_by_layer.pdf")
