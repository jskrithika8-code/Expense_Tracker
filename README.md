# 💰 Expense Tracker (GUI)

Intern ID: CITS5313

Full Name: J.S.KRITHIKA

No. of Weeks: 4 Weeks

Project Name: Expense Tracker

Project Scope: Develop a desktop application that automatically records and categorizes daily expenses, safely stores data in both CSV and JSON formats, supports monthly filtering and summary reports with visual bar charts, and provides an intuitive dark-themed graphical interface built with Python and Tkinter.

# 💰 Expense Tracker — Tkinter GUI

A Python-based desktop application that automatically tracks and organizes your expenses by category, handles monthly summaries with visual bar charts, supports CSV & JSON export, and provides an intuitive dark-themed graphical interface.

---

## 📖 Introduction

Expense Tracker GUI is a Python-based desktop application that helps users record, view, filter, and analyze their daily expenses through a clean and modern Tkinter interface. It stores all data in both CSV and JSON formats automatically.

---

## ✨ Features

- ➕ Add expenses with category, description, and date
- 📋 View all expenses in a sortable table
- 🔍 Filter by category or month
- 🗑️ Delete expenses with confirmation
- 📅 Monthly summary with category bar charts
- ⬇️ Export to CSV or JSON
- 🎨 Dark-themed user interface
- 💾 Auto-saves to both CSV and JSON on every change

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core language |
| Tkinter | GUI framework |
| ttk (Themed Widgets) | Styled dropdowns, tables, scrollbars |
| JSON | Primary data storage |
| CSV | Spreadsheet-compatible export |
| OS Module | File path handling |
| Collections | Category grouping & totals |
| Datetime | Date validation and formatting |

---

## 🗂️ Categories Supported

| Category | Color |
|---|---|
| 🍔 Food | Yellow |
| 🚌 Transport | Blue |
| 🛍️ Shopping | Purple |
| 🏥 Health | Green |
| 🎬 Entertainment | Cyan |
| 🧾 Bills | Red |
| 📚 Education | Indigo |
| 📦 Other | Gray |

---

## 🖥️ GUI Tabs

| Tab | Description |
|---|---|
| 📋 Expenses | View, filter, delete, and export expenses |
| 📅 Summary | Monthly breakdown with visual bar charts |
| ➕ Add | Form to add a new expense |

---

## ▶️ Working

1. Launch the app using `python expense_tracker_gui.py`
2. Use the **➕ Add** tab to enter amount, category, description, and date
3. View all recorded expenses in the **📋 Expenses** tab
4. Filter the table by category or month using the filter bar
5. Select any row and click **Delete** to remove an expense
6. Switch to **📅 Summary** to see monthly spend by category with bar charts
7. Click **⬇ Export** to save data as CSV or JSON to any location

---


## 💾 Storage

All expenses are automatically saved to two files in the same folder:

| File | Format |
|---|---|
| `expenses.json` | Human-readable JSON |
| `expenses.csv` | Spreadsheet-compatible CSV |

Both files stay in sync on every add or delete.

---

## 🔧 How It Works

**Step 1 — Launch**
Run the app. It loads any existing expenses from `expenses.json` automatically.

**Step 2 — Add Expense**
Fill in amount, category, description, and date. The form validates input and resets after saving.

**Step 3 — Auto Save**
Every add or delete instantly updates both `expenses.json` and `expenses.csv`.

**Step 4 — View & Filter**
The Expenses tab shows all records in a scrollable table. Filter by category dropdown or type a month (YYYY-MM) to narrow results.

**Step 5 — Summary**
The Summary tab groups expenses by category for the selected month, showing amount, a proportional bar, and percentage of total spend.

**Step 6 — Export**
Click Export to open a save dialog and choose CSV or JSON format. The file is saved to any chosen location.

---

## 🔮 Future Improvements

- Budget limits per category with alerts
- Recurring expense support
- Income vs expense tracking
- Charts using Matplotlib
- Search by description keyword
- Multi-currency support
- Light mode / theme toggle
- Password protection

---

## 🏁 Conclusion

The Expense Tracker GUI simplifies personal finance management by providing an intuitive dark-themed interface to record, categorize, and analyze daily expenses. With automatic dual-format storage, visual monthly summaries, and easy export options, it gives users full control over their spending with minimal effort.

---

