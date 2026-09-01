#!/usr/bin/env python3
"""
Copy & Rename
--------------
Pick one or more files, choose a destination folder, and copy them there
with new names built from file metadata (name, extension, modified date/time,
size) plus your own custom text.

Runs as a small desktop app using tkinter, which ships with Python — no
extra installs needed. Just run:

    python3 copy_rename_app.py
"""

import os
import shutil
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

TOKENS = [
    "Year", "Month", "Day", "Time",
    "Custom", "Name", "Counter",
]
DEFAULT_PATTERN = "YearMonthDay-Time-Custom"
DEFAULT_SUBFOLDER = "Year/Year-Month"


def file_meta(path, index, total):
    base, ext = os.path.splitext(os.path.basename(path))
    ext = ext.lstrip(".")
    stat = os.stat(path)
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
    width = max(2, len(str(total)))
    return {
        "name": base,
        "ext": ext,
        "year": mtime.strftime("%Y"),
        "month": mtime.strftime("%m"),
        "day": mtime.strftime("%d"),
        "time": mtime.strftime("%H%M%S"),
        "counter": str(index + 1).zfill(width),
        "size": stat.st_size,
    }


def build_new_name(pattern, custom_text, meta):
    base = pattern
    base = base.replace("Name", meta["name"])
    base = base.replace("Year", meta["year"])
    base = base.replace("Month", meta["month"])
    base = base.replace("Day", meta["day"])
    base = base.replace("Time", meta["time"])
    base = base.replace("Counter", meta["counter"])
    base = base.replace("Custom", custom_text or "")
    base = " ".join(base.split()).strip()
    if not base:
        base = meta["name"]
    return f"{base}.{meta['ext']}" if meta["ext"] else base


def build_subfolder_parts(pattern, custom_text, meta):
    """Turn a subfolder pattern like 'Year/Year-Month' into a list of
    sanitized path segments, e.g. ['2026', '2026-08']."""
    if not pattern:
        return []
    resolved = pattern
    resolved = resolved.replace("Name", meta["name"])
    resolved = resolved.replace("Year", meta["year"])
    resolved = resolved.replace("Month", meta["month"])
    resolved = resolved.replace("Day", meta["day"])
    resolved = resolved.replace("Time", meta["time"])
    resolved = resolved.replace("Counter", meta["counter"])
    resolved = resolved.replace("Custom", custom_text or "")
    parts = []
    for segment in resolved.replace("\\", "/").split("/"):
        segment = " ".join(segment.split()).strip()
        if segment:
            parts.append(segment)
    return parts


def human_size(n):
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Copy & Rename")
        self.geometry("660x680")
        self.minsize(580, 560)

        self.files = []          # list of source paths
        self.dest_dir = None

        self._build_ui()

    # ---------- UI ----------
    def _build_ui(self):
        pad = {"padx": 14, "pady": 8}

        # Step 1: files
        f1 = ttk.LabelFrame(self, text="1. Choose files")
        f1.pack(fill="x", **pad)
        ttk.Button(f1, text="Select files…", command=self.pick_files).pack(
            side="left", padx=10, pady=10
        )
        self.files_label = ttk.Label(f1, text="No files selected")
        self.files_label.pack(side="left", padx=6)

        # Step 2: pattern
        f2 = ttk.LabelFrame(self, text="2. Build the rename pattern")
        f2.pack(fill="x", **pad)

        row = ttk.Frame(f2)
        row.pack(fill="x", padx=10, pady=(10, 4))
        ttk.Label(row, text="Custom text:").pack(side="left")
        self.custom_var = tk.StringVar()
        self.custom_var.trace_add("write", lambda *a: self.refresh_preview())
        ttk.Entry(row, textvariable=self.custom_var).pack(
            side="left", fill="x", expand=True, padx=8
        )

        row2 = ttk.Frame(f2)
        row2.pack(fill="x", padx=10, pady=4)
        ttk.Label(row2, text="Pattern:").pack(side="left")
        self.pattern_var = tk.StringVar(value=DEFAULT_PATTERN)
        self.pattern_var.trace_add("write", lambda *a: self.refresh_preview())
        pattern_entry = ttk.Entry(row2, textvariable=self.pattern_var)
        pattern_entry.pack(side="left", fill="x", expand=True, padx=8)

        tokrow = ttk.Frame(f2)
        tokrow.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Label(tokrow, text="Insert:").pack(side="left")
        for t in TOKENS:
            ttk.Button(
                tokrow, text=t, width=len(t) + 1,
                command=lambda t=t: self.insert_token(pattern_entry, t)
            ).pack(side="left", padx=2)

        # Step 3: preview
        f3 = ttk.LabelFrame(self, text="3. Preview")
        f3.pack(fill="both", expand=True, **pad)
        cols = ("old", "new")
        self.tree = ttk.Treeview(f3, columns=cols, show="headings", height=8)
        self.tree.heading("old", text="Original name")
        self.tree.heading("new", text="New name")
        self.tree.column("old", width=260)
        self.tree.column("new", width=260)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

       # Step 4: destination + copy
        f4 = ttk.LabelFrame(self, text="4. Copy to destination")
        f4.pack(fill="x", **pad)
 
        row4 = ttk.Frame(f4)
        row4.pack(fill="x", padx=10, pady=(10, 4))
        ttk.Button(row4, text="Choose destination folder…", command=self.pick_dest).pack(
            side="left"
        )
        self.dest_label = ttk.Label(row4, text="No destination chosen")
        self.dest_label.pack(side="left", padx=10)
 
        sub_row = ttk.Frame(f4)
        sub_row.pack(fill="x", padx=10, pady=(6, 4))
        ttk.Label(sub_row, text="Subfolder path (leave empty to save directly):").pack(anchor="w")
        self.subfolder_var = tk.StringVar(value="")
        self.subfolder_entry = ttk.Entry(sub_row, textvariable=self.subfolder_var)
        self.subfolder_entry.pack(fill="x", pady=(4, 0))
 
        sub_tokrow = ttk.Frame(f4)
        sub_tokrow.pack(fill="x", padx=10, pady=(6, 0))
        ttk.Label(sub_tokrow, text="Insert:").pack(side="left")
        ttk.Button(
                        sub_tokrow, text=DEFAULT_SUBFOLDER, width=len(DEFAULT_SUBFOLDER) + 1,
                        command=lambda t=DEFAULT_SUBFOLDER: self.insert_token(self.subfolder_entry, t)
                    ).pack(side="left", padx=2)
        for t in TOKENS:
            ttk.Button(
                sub_tokrow, text=t, width=len(t) + 1,
                command=lambda t=t: self.insert_token(self.subfolder_entry, t)
            ).pack(side="left", padx=2)
        ttk.Label(
            f4,
            text="Uses the same tokens as the pattern above; \"/\" splits nested folders (e.g. {year}/{year}-{month} → 2026/2026-08).",
            foreground="#6B716F",
        ).pack(anchor="w", padx=10, pady=(0, 10))
        ttk.Label(
                    f4,
                    text="Folders are created if they don't exist yet, and reused if they do.",
                    foreground="#6B716F",
                ).pack(anchor="w", padx=10, pady=(0, 0))
        
 
        copy_row = ttk.Frame(f4)
        copy_row.pack(fill="x", padx=10, pady=(0, 10))
        self.copy_btn = ttk.Button(
            copy_row, text="Copy renamed files", command=self.do_copy, state="disabled"
        )
        self.copy_btn.pack(side="right")
 
        self.status = ttk.Label(self, text="", foreground="#2F6F4E")
        self.status.pack(fill="x", padx=14, pady=(0, 10))
 
 

    # ---------- actions ----------
    def pick_files(self):
        paths = filedialog.askopenfilenames(title="Select files to copy")
        if not paths:
            return
        self.files = list(paths)
        self.files_label.config(
            text=f"{len(self.files)} file(s) selected — "
            f"{human_size(sum(os.path.getsize(p) for p in self.files))} total"
        )
        self.refresh_preview()

    def insert_token(self, entry_widget, token):
        entry_widget.insert(tk.INSERT, token)
        self.refresh_preview()

    def refresh_preview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        pattern = self.pattern_var.get() or "{name}"
        custom = self.custom_var.get()
        total = len(self.files)
        self.new_names = []
        for i, path in enumerate(self.files):
            meta = file_meta(path, i, total)
            new_name = build_new_name(pattern, custom, meta)
            self.new_names.append(new_name)
            self.tree.insert("", "end", values=(os.path.basename(path), new_name))
        self._update_copy_state()

    def pick_dest(self):
        d = filedialog.askdirectory(title="Choose destination folder")
        if not d:
            return
        self.dest_dir = d
        self.dest_label.config(text=d)
        self._update_copy_state()

    def _update_copy_state(self):
        ready = bool(self.files) and bool(self.dest_dir)
        self.copy_btn.config(state="normal" if ready else "disabled")

    def do_copy(self):
        if not self.files or not self.dest_dir:
            return

        custom = self.custom_var.get()
        subfolder_pattern = self.subfolder_var.get().strip()

        dest_paths = []
        for i, path in enumerate(self.files):
            meta = file_meta(path, i, len(self.files))
            parts = build_subfolder_parts(subfolder_pattern, custom, meta)
            folder = os.path.join(self.dest_dir, *parts) if parts else self.dest_dir
            dest_paths.append(os.path.join(folder, self.new_names[i]))

        # guard against overwriting distinct source files with the same destination path
        if len(set(dest_paths)) != len(dest_paths):
            if not messagebox.askyesno(
                "Duplicate names",
                "Some renamed files would land on the same destination path, so "
                "later copies will overwrite earlier ones. Continue anyway?",
            ):
                return

        done = 0
        errors = []
        for path, dest_path in zip(self.files, dest_paths):
            try:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(path, dest_path)  # copy2 preserves metadata
                done += 1
            except OSError as e:
                errors.append(f"{os.path.basename(path)}: {e}")

        if errors:
            self.status.config(
                foreground="#A34B2B",
                text=f"Copied {done}/{len(self.files)}. Errors: " + "; ".join(errors),
            )
        else:
            self.status.config(
                foreground="#2F6F4E",
                text=f"Done — {done} file(s) copied to {self.dest_dir}",
            )


if __name__ == "__main__":
    App().mainloop()