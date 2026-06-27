#!/usr/bin/env python3
"""
expense_tracker_gui.py — Tkinter GUI Expense Tracker with CSV & JSON storage
Run: python expense_tracker_gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os
from datetime import datetime
from collections import defaultdict

# ── Files ──────────────────────────────────────────────────────────────────────
DATA_JSON = "expenses.json"
DATA_CSV  = "expenses.csv"

CATEGORIES = ["Food", "Transport", "Shopping", "Health", "Entertainment", "Bills", "Education", "Other"]

CATEGORY_COLORS = {
    "Food":          "#f59e0b",
    "Transport":     "#3b82f6",
    "Shopping":      "#a855f7",
    "Health":        "#22c55e",
    "Entertainment": "#06b6d4",
    "Bills":         "#ef4444",
    "Education":     "#6366f1",
    "Other":         "#6b7280",
}

# ── Theme ──────────────────────────────────────────────────────────────────────
BG       = "#0f172a"
BG2      = "#1e293b"
BG3      = "#334155"
FG       = "#f1f5f9"
FG2      = "#94a3b8"
ACCENT   = "#38bdf8"
GREEN    = "#22c55e"
RED      = "#ef4444"
YELLOW   = "#f59e0b"
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_H   = ("Segoe UI", 13, "bold")
FONT_SM  = ("Segoe UI", 9)


# ── Data I/O ───────────────────────────────────────────────────────────────────
def load_expenses():
    if os.path.exists(DATA_JSON):
        with open(DATA_JSON, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_JSON, "w") as f:
        json.dump(expenses, f, indent=2)
    with open(DATA_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id","date","amount","category","description"])
        writer.writeheader()
        writer.writerows(expenses)

def next_id(expenses):
    return max((e["id"] for e in expenses), default=0) + 1


# ── Main App ───────────────────────────────────────────────────────────────────
class ExpenseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💰 Expense Tracker")
        self.geometry("900x620")
        self.minsize(800, 560)
        self.configure(bg=BG)
        self.expenses = load_expenses()
        self._build_ui()
        self._refresh_table()
        self._refresh_summary()

    def _build_ui(self):
        # ── Sidebar ────────────────────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=BG2, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="💰", font=("Segoe UI", 28), bg=BG2, fg=ACCENT).pack(pady=(24,4))
        tk.Label(sidebar, text="Expense Tracker", font=FONT_H, bg=BG2, fg=FG).pack()
        tk.Label(sidebar, text="CSV  &  JSON", font=FONT_SM, bg=BG2, fg=FG2).pack(pady=(0,24))

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=16)

        self.nav_btns = {}
        for label, tab in [("📋  Expenses", "expenses"), ("📅  Summary", "summary"), ("➕  Add", "add")]:
            btn = tk.Button(
                sidebar, text=label, font=FONT_B, anchor="w",
                bg=BG2, fg=FG, activebackground=BG3, activeforeground=ACCENT,
                bd=0, padx=20, pady=10, cursor="hand2",
                command=lambda t=tab: self._show_tab(t)
            )
            btn.pack(fill="x", pady=1)
            self.nav_btns[tab] = btn

        # Stats at bottom of sidebar
        self.lbl_total  = tk.Label(sidebar, text="", font=FONT_SM, bg=BG2, fg=FG2)
        self.lbl_count  = tk.Label(sidebar, text="", font=FONT_SM, bg=BG2, fg=FG2)
        self.lbl_total.pack(side="bottom", pady=4)
        self.lbl_count.pack(side="bottom", pady=2)
        ttk.Separator(sidebar, orient="horizontal").pack(side="bottom", fill="x", padx=16, pady=8)

        # ── Main area ──────────────────────────────────────────────────────────
        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.frames = {}
        for tab in ("expenses", "summary", "add"):
            f = tk.Frame(self.main, bg=BG)
            f.place(relwidth=1, relheight=1)
            self.frames[tab] = f

        self._build_expenses_tab()
        self._build_summary_tab()
        self._build_add_tab()
        self._show_tab("expenses")
        self._update_sidebar_stats()

    # ── Tab switching ──────────────────────────────────────────────────────────
    def _show_tab(self, tab):
        for name, btn in self.nav_btns.items():
            btn.config(bg=BG3 if name == tab else BG2, fg=ACCENT if name == tab else FG)
        self.frames[tab].lift()

    # ── Expenses Tab ───────────────────────────────────────────────────────────
    def _build_expenses_tab(self):
        f = self.frames["expenses"]

        # Header + filters
        hdr = tk.Frame(f, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(20,10))
        tk.Label(hdr, text="All Expenses", font=FONT_H, bg=BG, fg=FG).pack(side="left")

        # Filter bar
        fbar = tk.Frame(f, bg=BG2, pady=8)
        fbar.pack(fill="x", padx=20, pady=(0,10))

        tk.Label(fbar, text="Category:", font=FONT_SM, bg=BG2, fg=FG2).pack(side="left", padx=(12,4))
        self.filter_cat = ttk.Combobox(fbar, values=["All"] + CATEGORIES, width=14, font=FONT_SM, state="readonly")
        self.filter_cat.set("All")
        self.filter_cat.pack(side="left", padx=4)
        self.filter_cat.bind("<<ComboboxSelected>>", lambda e: self._refresh_table())

        tk.Label(fbar, text="Month (YYYY-MM):", font=FONT_SM, bg=BG2, fg=FG2).pack(side="left", padx=(16,4))
        self.filter_month = tk.Entry(fbar, width=10, font=FONT_SM, bg=BG3, fg=FG, insertbackground=FG, relief="flat")
        self.filter_month.pack(side="left", padx=4)

        tk.Button(fbar, text="Filter", font=FONT_SM, bg=ACCENT, fg=BG, relief="flat",
                  padx=8, cursor="hand2", command=self._refresh_table).pack(side="left", padx=6)
        tk.Button(fbar, text="Clear", font=FONT_SM, bg=BG3, fg=FG, relief="flat",
                  padx=8, cursor="hand2", command=self._clear_filters).pack(side="left", padx=2)
        tk.Button(fbar, text="⬇ Export", font=FONT_SM, bg=GREEN, fg=BG, relief="flat",
                  padx=8, cursor="hand2", command=self._export).pack(side="right", padx=12)

        # Table
        cols = ("ID", "Date", "Amount", "Category", "Description")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG2, foreground=FG, fieldbackground=BG2,
                        rowheight=28, font=FONT, borderwidth=0)
        style.configure("Treeview.Heading", background=BG3, foreground=ACCENT,
                        font=FONT_B, relief="flat")
        style.map("Treeview", background=[("selected", BG3)], foreground=[("selected", ACCENT)])

        tree_frame = tk.Frame(f, bg=BG)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0,8))

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for col, w in zip(cols, (50, 100, 110, 120, 360)):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center" if col != "Description" else "w")
        self.tree.column("Description", anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Bottom bar
        bot = tk.Frame(f, bg=BG2, pady=8)
        bot.pack(fill="x", padx=20, pady=(0,16))
        self.lbl_table_total = tk.Label(bot, text="", font=FONT_B, bg=BG2, fg=GREEN)
        self.lbl_table_total.pack(side="left", padx=12)
        tk.Button(bot, text="🗑  Delete Selected", font=FONT_SM, bg=RED, fg="white",
                  relief="flat", padx=10, cursor="hand2",
                  command=self._delete_selected).pack(side="right", padx=12)

    def _refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        cat   = self.filter_cat.get()
        month = self.filter_month.get().strip()

        filtered = self.expenses
        if cat and cat != "All":
            filtered = [e for e in filtered if e["category"] == cat]
        if month:
            filtered = [e for e in filtered if e["date"].startswith(month)]

        total = 0
        for e in sorted(filtered, key=lambda x: x["date"]):
            self.tree.insert("", "end", iid=str(e["id"]),
                             values=(e["id"], e["date"], f"₹{e['amount']:,.2f}",
                                     e["category"], e["description"]))
            total += e["amount"]

        self.lbl_table_total.config(text=f"Total: ₹{total:,.2f}  ({len(filtered)} records)")
        self._update_sidebar_stats()

    def _clear_filters(self):
        self.filter_cat.set("All")
        self.filter_month.delete(0, "end")
        self._refresh_table()

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select an expense to delete.")
            return
        eid = int(sel[0])
        match = next((e for e in self.expenses if e["id"] == eid), None)
        if not match:
            return
        if messagebox.askyesno("Confirm Delete",
                               f"Delete: ₹{match['amount']} — {match['description']}?"):
            self.expenses = [e for e in self.expenses if e["id"] != eid]
            save_expenses(self.expenses)
            self._refresh_table()
            self._refresh_summary()

    def _export(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv"), ("JSON", "*.json")],
            initialfile=f"expenses_export_{datetime.now().strftime('%Y%m%d')}"
        )
        if not path:
            return
        if path.endswith(".json"):
            with open(path, "w") as f:
                json.dump(self.expenses, f, indent=2)
        else:
            with open(path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["id","date","amount","category","description"])
                writer.writeheader()
                writer.writerows(self.expenses)
        messagebox.showinfo("Exported", f"Saved to:\n{path}")

    # ── Summary Tab ────────────────────────────────────────────────────────────
    def _build_summary_tab(self):
        f = self.frames["summary"]
        tk.Label(f, text="Monthly Summary", font=FONT_H, bg=BG, fg=FG).pack(anchor="w", padx=20, pady=(20,4))

        # Month selector
        mbar = tk.Frame(f, bg=BG2, pady=8)
        mbar.pack(fill="x", padx=20, pady=(0,12))
        tk.Label(mbar, text="Month:", font=FONT_SM, bg=BG2, fg=FG2).pack(side="left", padx=(12,4))
        self.sum_month = ttk.Combobox(mbar, width=12, font=FONT_SM, state="readonly")
        self.sum_month.pack(side="left", padx=4)
        self.sum_month.bind("<<ComboboxSelected>>", lambda e: self._refresh_summary())

        self.sum_canvas = tk.Frame(f, bg=BG)
        self.sum_canvas.pack(fill="both", expand=True, padx=20, pady=(0,16))

    def _refresh_summary(self):
        # Update month dropdown
        months = sorted({e["date"][:7] for e in self.expenses}, reverse=True)
        self.sum_month["values"] = months
        if months and self.sum_month.get() not in months:
            self.sum_month.set(months[0])

        # Clear
        for w in self.sum_canvas.winfo_children():
            w.destroy()

        month = self.sum_month.get()
        if not month:
            tk.Label(self.sum_canvas, text="No data yet.", font=FONT, bg=BG, fg=FG2).pack(pady=40)
            return

        filtered = [e for e in self.expenses if e["date"].startswith(month)]
        if not filtered:
            tk.Label(self.sum_canvas, text="No expenses for this month.", font=FONT, bg=BG, fg=FG2).pack(pady=40)
            return

        by_cat = defaultdict(float)
        for e in filtered:
            by_cat[e["category"]] += e["amount"]
        total = sum(by_cat.values())
        sorted_cats = sorted(by_cat.items(), key=lambda x: x[1], reverse=True)

        label = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
        tk.Label(self.sum_canvas, text=f"📅  {label}", font=FONT_H, bg=BG, fg=ACCENT).pack(anchor="w", pady=(8,12))

        for cat, amt in sorted_cats:
            pct  = amt / total * 100
            color = CATEGORY_COLORS.get(cat, "#6b7280")

            row = tk.Frame(self.sum_canvas, bg=BG)
            row.pack(fill="x", pady=3)

            tk.Label(row, text=cat, font=FONT_B, bg=BG, fg=color, width=14, anchor="w").pack(side="left")
            tk.Label(row, text=f"₹{amt:,.2f}", font=FONT_B, bg=BG, fg=GREEN, width=12, anchor="e").pack(side="left", padx=(0,12))

            # Bar
            bar_bg = tk.Frame(row, bg=BG3, height=14, width=300)
            bar_bg.pack(side="left", padx=(0,8))
            bar_bg.pack_propagate(False)
            bar_fill = tk.Frame(bar_bg, bg=color, height=14, width=int(300 * pct / 100))
            bar_fill.place(x=0, y=0)

            tk.Label(row, text=f"{pct:.1f}%", font=FONT_SM, bg=BG, fg=FG2).pack(side="left")

        ttk.Separator(self.sum_canvas, orient="horizontal").pack(fill="x", pady=10)
        tot_row = tk.Frame(self.sum_canvas, bg=BG)
        tot_row.pack(fill="x")
        tk.Label(tot_row, text="Total", font=FONT_B, bg=BG, fg=FG, width=14, anchor="w").pack(side="left")
        tk.Label(tot_row, text=f"₹{total:,.2f}", font=FONT_B, bg=BG, fg=GREEN, width=12, anchor="e").pack(side="left")

    # ── Add Tab ────────────────────────────────────────────────────────────────
    def _build_add_tab(self):
        f = self.frames["add"]

        card = tk.Frame(f, bg=BG2, padx=32, pady=32)
        card.place(relx=0.5, rely=0.5, anchor="center", width=440)

        tk.Label(card, text="➕  Add Expense", font=FONT_H, bg=BG2, fg=FG).grid(
            row=0, column=0, columnspan=2, pady=(0,20), sticky="w")

        fields = [
            ("Amount (₹)",   "entry"),
            ("Category",     "combo"),
            ("Description",  "entry"),
            ("Date",         "entry"),
        ]
        self.add_vars = {}
        for i, (label, ftype) in enumerate(fields, 1):
            tk.Label(card, text=label, font=FONT_SM, bg=BG2, fg=FG2).grid(
                row=i, column=0, sticky="w", pady=6)
            if ftype == "entry":
                w = tk.Entry(card, font=FONT, bg=BG3, fg=FG, insertbackground=FG,
                             relief="flat", width=24)
                if label == "Date":
                    w.insert(0, datetime.now().strftime("%Y-%m-%d"))
            else:
                w = ttk.Combobox(card, values=CATEGORIES, font=FONT, state="readonly", width=22)
                w.set("Food")
            w.grid(row=i, column=1, sticky="ew", padx=(12,0), pady=6)
            self.add_vars[label] = w

        card.columnconfigure(1, weight=1)

        self.add_status = tk.Label(card, text="", font=FONT_SM, bg=BG2, fg=GREEN)
        self.add_status.grid(row=len(fields)+1, column=0, columnspan=2, pady=(8,0))

        tk.Button(card, text="Add Expense", font=FONT_B, bg=ACCENT, fg=BG,
                  relief="flat", padx=16, pady=8, cursor="hand2",
                  command=self._add_expense).grid(
            row=len(fields)+2, column=0, columnspan=2, pady=(16,0), sticky="ew")

    def _add_expense(self):
        raw_amt  = self.add_vars["Amount (₹)"].get().strip()
        category = self.add_vars["Category"].get().strip()
        desc     = self.add_vars["Description"].get().strip()
        date     = self.add_vars["Date"].get().strip()

        # Validate
        try:
            amount = float(raw_amt)
            if amount <= 0: raise ValueError
        except ValueError:
            self.add_status.config(text="⚠ Enter a valid positive amount.", fg=RED)
            return
        if not category:
            self.add_status.config(text="⚠ Select a category.", fg=RED)
            return
        if not desc:
            desc = category
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            self.add_status.config(text="⚠ Date must be YYYY-MM-DD.", fg=RED)
            return

        expense = {
            "id":          next_id(self.expenses),
            "date":        date,
            "amount":      round(amount, 2),
            "category":    category,
            "description": desc,
        }
        self.expenses.append(expense)
        save_expenses(self.expenses)
        self._refresh_table()
        self._refresh_summary()
        self._update_sidebar_stats()

        # Reset form
        self.add_vars["Amount (₹)"].delete(0, "end")
        self.add_vars["Description"].delete(0, "end")
        self.add_vars["Date"].delete(0, "end")
        self.add_vars["Date"].insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.add_status.config(
            text=f"✓ Added ₹{amount:,.2f} — {category}", fg=GREEN)

    # ── Sidebar stats ──────────────────────────────────────────────────────────
    def _update_sidebar_stats(self):
        total = sum(e["amount"] for e in self.expenses)
        self.lbl_count.config(text=f"{len(self.expenses)} expenses")
        self.lbl_total.config(text=f"Total: ₹{total:,.2f}")


if __name__ == "__main__":
    app = ExpenseApp()
    app.mainloop()
