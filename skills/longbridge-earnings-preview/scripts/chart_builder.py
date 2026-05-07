"""
earnings-preview Chart Builder
================================
Reusable matplotlib chart functions for earnings preview DOCX reports.
Each function saves a PNG to /tmp and returns the file path for embedding.

Usage
-----
    from scripts.chart_builder import ChartBuilder
    cb = ChartBuilder()

    path = cb.quarterly_bar(
        title="Tencent Quarterly Revenue Trend",
        quarters=["Q1 2024", "Q2 2024", "Q3 2024", "Q1 2026E"],
        values=[159.5, 161.1, 167.2, 198.9],
        estimate_idx=-1,
        ylabel="Revenue (RMB Billion)",
    )
    b.image(path)

Style
-----
- Clean white background, light grey grid
- Primary blue: #1A56DB  |  Estimate/accent: #F5A623
- 150 DPI, bbox_inches="tight"
"""

from __future__ import annotations

import os
import tempfile
import numpy as np

# ── Matplotlib backend (headless) ────────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ── Palette ───────────────────────────────────────────────────────────────────
C_BLUE   = "#1A56DB"
C_ORANGE = "#F5A623"
C_GREEN  = "#27AE60"
C_RED    = "#E74C3C"
C_PURPLE = "#8E44AD"
C_GREY   = "#95A5A6"

_PALETTE = [C_BLUE, C_ORANGE, C_GREEN, C_RED, C_PURPLE, C_GREY]

DPI = 150


def _savefig(fig: plt.Figure, prefix: str = "chart") -> str:
    fd, path = tempfile.mkstemp(prefix=f"{prefix}_", suffix=".png", dir="/tmp")
    os.close(fd)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def _style_ax(ax: plt.Axes, ylabel: str = "", xlabel: str = "") -> None:
    ax.set_facecolor("white")
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CCCCCC")
    ax.spines["bottom"].set_color("#CCCCCC")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)


# ── Chart 1: Quarterly Bar Chart ─────────────────────────────────────────────
def quarterly_bar(
    title: str,
    quarters: list[str],
    values: list[float],
    estimate_idx: int = -1,
    ylabel: str = "Revenue",
    color: str = C_BLUE,
    est_color: str = C_ORANGE,
    figsize: tuple = (10, 5),
) -> str:
    """Vertical bar chart with one highlighted estimate bar."""
    fig, ax = plt.subplots(figsize=figsize)
    colors = [est_color if i == (len(values) + estimate_idx if estimate_idx < 0 else estimate_idx)
              else color for i in range(len(values))]
    bars = ax.bar(quarters, values, color=colors, width=0.6, zorder=3)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.01,
                f"{val:g}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_ylim(0, max(values) * 1.15)
    ax.tick_params(axis="x", rotation=30, labelsize=9)
    _style_ax(ax, ylabel=ylabel)
    fig.tight_layout()
    return _savefig(fig, "quarterly_bar")


# ── Chart 2: Multi-Series Line Chart ─────────────────────────────────────────
def growth_lines(
    title: str,
    quarters: list[str],
    series: list[dict],
    ylabel: str = "YoY Growth (%)",
    figsize: tuple = (10, 5),
) -> str:
    """
    Line chart with multiple series.
    series = [{"label": "Revenue Growth", "color": C_BLUE, "marker": "o", "values": [13, 14, 15, ...]}, ...]
    """
    fig, ax = plt.subplots(figsize=figsize)
    for s in series:
        ax.plot(quarters, s["values"], color=s.get("color", C_BLUE),
                marker=s.get("marker", "o"), linewidth=2, markersize=7, label=s["label"], zorder=3)
        for x, y in zip(quarters, s["values"]):
            ax.annotate(f"{y:g}%", (x, y), textcoords="offset points", xytext=(0, 8),
                        ha="center", fontsize=8, color=s.get("color", C_BLUE), fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=9, framealpha=0.9)
    ax.tick_params(axis="x", rotation=20, labelsize=9)
    ax.set_ylim(0, max(max(s["values"]) for s in series) * 1.25)
    _style_ax(ax, ylabel=ylabel)
    fig.tight_layout()
    return _savefig(fig, "growth_lines")


# ── Chart 3: Grouped Bar Chart ────────────────────────────────────────────────
def grouped_bar(
    title: str,
    categories: list[str],
    series: list[dict],
    ylabel: str = "",
    figsize: tuple = (11, 5),
) -> str:
    """
    Grouped bar chart.
    series = [{"label": "Q1 2025", "color": C_BLUE, "values": [...]}, {"label": "Q1 2026E", ...}]
    """
    n_cats = len(categories)
    n_series = len(series)
    x = np.arange(n_cats)
    width = 0.35 if n_series == 2 else 0.8 / n_series

    fig, ax = plt.subplots(figsize=figsize)
    offsets = np.linspace(-(n_series - 1) / 2 * width, (n_series - 1) / 2 * width, n_series)
    for s, offset in zip(series, offsets):
        bars = ax.bar(x + offset, s["values"], width * 0.95,
                      label=s["label"], color=s.get("color", C_BLUE), zorder=3)
        for bar, val in zip(bars, s["values"]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(s["values"]) * 0.01,
                    f"{val:g}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(fontsize=9)
    all_vals = [v for s in series for v in s["values"]]
    ax.set_ylim(0, max(all_vals) * 1.18)
    _style_ax(ax, ylabel=ylabel)
    fig.tight_layout()
    return _savefig(fig, "grouped_bar")


# ── Chart 4: Side-by-Side Pie Charts ─────────────────────────────────────────
def pie_pair(
    title1: str,
    title2: str,
    labels: list[str],
    values1: list[float],
    values2: list[float],
    figsize: tuple = (12, 5),
) -> str:
    """Two pie charts side by side."""
    colors = _PALETTE[:len(labels)]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    def _pie(ax, vals, title):
        wedges, texts, autotexts = ax.pie(
            vals, labels=None, autopct="%1.0f%%", colors=colors,
            startangle=90, pctdistance=0.75)
        for at in autotexts:
            at.set_fontsize(10)
            at.set_fontweight("bold")
        ax.set_title(title, fontsize=13, fontweight="bold", pad=8)
    _pie(ax1, values1, title1)
    _pie(ax2, values2, title2)
    patches = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, labels)]
    fig.legend(handles=patches, loc="lower center", ncol=min(len(labels), 3),
               fontsize=9, bbox_to_anchor=(0.5, -0.05))
    fig.tight_layout()
    return _savefig(fig, "pie_pair")


# ── Chart 5: Scenario Horizontal Bar ─────────────────────────────────────────
def scenario_hbar(
    title: str,
    scenarios: list[str],
    values: list[float],
    current: float,
    current_label: str,
    colors: list[str] | None = None,
    xlabel: str = "Implied Share Price",
    figsize: tuple = (10, 4),
) -> str:
    """Horizontal bar chart for scenario analysis with current price dashed line."""
    if colors is None:
        colors = [C_GREEN, C_BLUE, C_RED]
    fig, ax = plt.subplots(figsize=figsize)
    y = np.arange(len(scenarios))
    bars = ax.barh(y, values, color=colors, height=0.5, zorder=3)
    for bar, val, scenario in zip(bars, values, scenarios):
        pct = (val / current - 1) * 100
        sign = "+" if pct >= 0 else ""
        label = f"{xlabel.split()[0][:2]}${val:,.0f} ({sign}{pct:.0f}%)"
        ax.text(bar.get_width() + max(values) * 0.01, bar.get_y() + bar.get_height() / 2,
                label, va="center", fontsize=10, fontweight="bold")
    ax.axvline(current, color=C_RED, linestyle="--", linewidth=1.5, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(scenarios, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlim(0, max(values) * 1.25)
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    legend = [Line2D([0], [0], color=C_RED, linestyle="--", label=f"Current: {current_label}")]
    ax.legend(handles=legend, fontsize=9, loc="lower right")
    _style_ax(ax, xlabel=xlabel)
    fig.tight_layout()
    return _savefig(fig, "scenario_hbar")


# ── Chart 6: Peer Multiples Side-by-Side ─────────────────────────────────────
def peer_multiples(
    title_left: str,
    title_right: str,
    companies: list[str],
    vals_left: list[float | None],
    vals_right: list[float | None],
    highlight: str,
    xlabel_left: str = "P/E Ratio (TTM)",
    xlabel_right: str = "P/B Ratio",
    figsize: tuple = (13, 5),
) -> str:
    """Side-by-side horizontal bar charts for peer comparison."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    def _hbar(ax, vals, title, xlabel):
        clean = [(c, v) for c, v in zip(companies, vals) if v is not None]
        names = [x[0] for x in clean]
        numbers = [x[1] for x in clean]
        colors = [C_RED if n == highlight else C_BLUE for n in names]
        y = np.arange(len(names))
        bars = ax.barh(y, numbers, color=colors, height=0.5, zorder=3)
        for bar, val in zip(bars, numbers):
            ax.text(bar.get_width() + max(numbers) * 0.02, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}x", va="center", fontsize=9)
        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=10)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlim(0, max(numbers) * 1.3)
        ax.grid(axis="x", color="#DDDDDD", linewidth=0.8, zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_xlabel(xlabel, fontsize=9)

    _hbar(ax1, vals_left, title_left, xlabel_left)
    _hbar(ax2, vals_right, title_right, xlabel_right)
    fig.tight_layout(pad=3)
    return _savefig(fig, "peer_multiples")


# ── Chart 7: Price Action Line Chart ─────────────────────────────────────────
def price_action(
    title: str,
    dates: list[str],
    prices: list[float],
    current: float,
    current_label: str,
    target: float | None = None,
    target_label: str = "Consensus PT",
    ylabel: str = "Price",
    figsize: tuple = (12, 4.5),
) -> str:
    """Line chart for price action with reference lines."""
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(dates))
    ax.plot(x, prices, color=C_BLUE, linewidth=2, zorder=3)
    ax.fill_between(x, prices, alpha=0.15, color=C_BLUE)
    ax.axhline(current, color=C_RED, linestyle="--", linewidth=1.2, zorder=4)
    legend_lines = [Line2D([0], [0], color=C_RED, linestyle="--", label=f"Current: {current_label}")]
    if target is not None:
        ax.axhline(target, color=C_GREEN, linestyle="--", linewidth=1.2, zorder=4)
        legend_lines.append(
            Line2D([0], [0], color=C_GREEN, linestyle="--", label=f"{target_label}: {target_label.split(':')[-1] if ':' in target_label else target_label}"))
    # Tick every ~10 points
    step = max(1, len(dates) // 10)
    ax.set_xticks(x[::step])
    ax.set_xticklabels(dates[::step], rotation=30, fontsize=8)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.legend(handles=legend_lines, fontsize=9)
    _style_ax(ax, ylabel=ylabel)
    fig.tight_layout()
    return _savefig(fig, "price_action")


# ── Chart 8: Analyst Price Target Horizontal Bar ──────────────────────────────
def analyst_pt_hbar(
    title: str,
    brokers: list[str],
    targets: list[float],
    current: float,
    current_label: str,
    colors: list[str] | None = None,
    xlabel: str = "Target Price",
    figsize: tuple = (10, 4),
) -> str:
    """Horizontal bar chart for analyst price targets vs current price."""
    if colors is None:
        colors = [C_ORANGE, C_PURPLE, C_GREEN, C_BLUE] + [C_BLUE] * len(brokers)
    fig, ax = plt.subplots(figsize=figsize)
    y = np.arange(len(brokers))
    bars = ax.barh(y, targets, color=colors[:len(brokers)], height=0.5, zorder=3)
    for bar, val, broker in zip(bars, targets, brokers):
        pct = (val / current - 1) * 100
        sign = "+" if pct >= 0 else ""
        ax.text(bar.get_width() + max(targets) * 0.01, bar.get_y() + bar.get_height() / 2,
                f"{xlabel[0]}${val:,.0f} ({sign}{pct:.0f}%)", va="center", fontsize=10, fontweight="bold")
    ax.axvline(current, color=C_RED, linestyle="--", linewidth=1.5, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(brokers, fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlim(0, max(targets) * 1.3)
    ax.grid(axis="x", color="#DDDDDD", linewidth=0.8, zorder=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    legend = [Line2D([0], [0], color=C_RED, linestyle="--", label=f"Current: {current_label}")]
    ax.legend(handles=legend, fontsize=9, loc="lower right")
    ax.set_xlabel(xlabel, fontsize=9)
    fig.tight_layout()
    return _savefig(fig, "analyst_pt_hbar")


# ── Convenience class ─────────────────────────────────────────────────────────
class ChartBuilder:
    """Thin wrapper exposing all chart functions as instance methods."""
    quarterly_bar   = staticmethod(quarterly_bar)
    growth_lines    = staticmethod(growth_lines)
    grouped_bar     = staticmethod(grouped_bar)
    pie_pair        = staticmethod(pie_pair)
    scenario_hbar   = staticmethod(scenario_hbar)
    peer_multiples  = staticmethod(peer_multiples)
    price_action    = staticmethod(price_action)
    analyst_pt_hbar = staticmethod(analyst_pt_hbar)
