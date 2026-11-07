# interface/graph_viewer.py
import tkinter as tk
from tkinter import messagebox
from typing import Iterable, Any, Sequence
from collections import Counter

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------- small utilities ----------

def _extract_attr(item: Any, names: Sequence[str]) -> str | None:
    """Try attributes or dict keys in order; return first truthy value found."""
    if isinstance(item, dict):
        for n in names:
            v = item.get(n)
            if v:
                return str(v)
        return None
    for n in names:
        if hasattr(item, n):
            v = getattr(item, n)
            if v:
                return str(v)
    return None


def _counts_from(items: Iterable[Any], names: Sequence[str]) -> Counter:
    values = (_extract_attr(x, names) for x in items)
    return Counter(v for v in values if v)  # drop None/empty


def _make_bar_figure(title: str, xlabel: str, ylabel: str, counts: Counter):
    labels = list(counts.keys())
    values = list(counts.values())

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=30, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    return fig


def _show_matplotlib_popup(master: tk.Misc, fig, title: str, size: str = "760x520"):
    win = tk.Toplevel(master)
    win.title(title)
    win.geometry(size)

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return win


# ---------- public API ----------

def show_books_by_genre_popup(master: tk.Misc, books: Iterable[Any]):
    """Embed a 'Books per Genre' bar chart in a Tkinter popup."""
    counts = _counts_from(books, names=("genre", "book_genre", "bookGenre"))
    if not counts:
        messagebox.showinfo("Info", "No genre data to display.")
        return
    fig = _make_bar_figure("Books per Genre", "Genre", "Number of Books", counts)
    _show_matplotlib_popup(master, fig, "Books by Genre")


def show_members_by_type_popup(master: tk.Misc, members: Iterable[Any]):
    """Embed a 'Members by Type' bar chart in a Tkinter popup."""
    counts = _counts_from(members, names=("type", "member_type", "memberType"))
    if not counts:
        messagebox.showinfo("Info", "No member type data to display.")
        return
    fig = _make_bar_figure("Members by Type", "Type", "Number of Members", counts)
    _show_matplotlib_popup(master, fig, "Members by Type")
