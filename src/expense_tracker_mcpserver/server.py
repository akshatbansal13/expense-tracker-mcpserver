import json
from fastmcp import FastMCP
import os
import sqlite3
from typing import Literal
import platformdirs
import shutil

DATA_DIR = platformdirs.user_data_dir("ExpenseTrackerMCP")
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "expenses.db")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")

# Copy the default categories.json to the data directory if it doesn't exist
DEFAULT_CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")
if not os.path.exists(CATEGORIES_PATH) and os.path.exists(DEFAULT_CATEGORIES_PATH):
    shutil.copy2(DEFAULT_CATEGORIES_PATH, CATEGORIES_PATH)

# Migrate old expenses.db if it exists
OLD_DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
if not os.path.exists(DB_PATH) and os.path.exists(OLD_DB_PATH):
    shutil.copy2(OLD_DB_PATH, DB_PATH)

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        try:
            c.execute("ALTER TABLE expenses ADD COLUMN type TEXT DEFAULT 'expense'")
        except sqlite3.OperationalError:
            pass # Column already exists

init_db()

@mcp.tool()
def add_expense(date: str, amount: float | str, category: str, subcategory: str = "", note: str = "") -> dict:
    '''Add a new expense entry to the database. Date should be YYYY-MM-DD.'''
    amount = float(amount)
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note, type) VALUES (?,?,?,?,?,?)",
            (date, amount, category, subcategory, note, "expense")
        )
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def add_credit(date: str, amount: float | str, category: str, subcategory: str = "", note: str = "") -> dict:
    '''Add a new credit (income) entry to the database. Date should be YYYY-MM-DD.'''
    amount = float(amount)
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note, type) VALUES (?,?,?,?,?,?)",
            (date, amount, category, subcategory, note, "credit")
        )
        return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def edit_expense(id: int, date: str | None = None, amount: float | str | None = None, category: str | None = None, subcategory: str | None = None, note: str | None = None) -> dict:
    '''Edit an existing expense by ID. Only provide fields you want to change.'''
    return _update_transaction(id, date, amount, category, subcategory, note, expected_type="expense")

@mcp.tool()
def edit_credit(id: int, date: str | None = None, amount: float | str | None = None, category: str | None = None, subcategory: str | None = None, note: str | None = None) -> dict:
    '''Edit an existing credit by ID. Only provide fields you want to change.'''
    return _update_transaction(id, date, amount, category, subcategory, note, expected_type="credit")

def _update_transaction(id: int, date: str | None, amount: float | str | None, category: str | None, subcategory: str | None, note: str | None, expected_type: str) -> dict:
    updates = []
    params = []
    if date is not None:
        updates.append("date = ?")
        params.append(date)
    if amount is not None:
        updates.append("amount = ?")
        params.append(float(amount))
    if category is not None:
        updates.append("category = ?")
        params.append(category)
    if subcategory is not None:
        updates.append("subcategory = ?")
        params.append(subcategory)
    if note is not None:
        updates.append("note = ?")
        params.append(note)

    if not updates:
        return {"status": "error", "message": "No fields to update provided."}

    params.extend([expected_type, id])
    query = f"UPDATE expenses SET {', '.join(updates)} WHERE type = ? AND id = ?"
    
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(query, params)
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No {expected_type} found with ID {id}"}
        return {"status": "ok", "message": f"Updated {cur.rowcount} row(s)"}

@mcp.tool()
def delete_expense(id: int) -> dict:
    '''Delete an expense by ID.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE type = 'expense' AND id = ?", (id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No expense found with ID {id}"}
        return {"status": "ok", "message": "Deleted successfully"}

@mcp.tool()
def delete_credit(id: int) -> dict:
    '''Delete a credit by ID.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE type = 'credit' AND id = ?", (id,))
        if cur.rowcount == 0:
            return {"status": "error", "message": f"No credit found with ID {id}"}
        return {"status": "ok", "message": "Deleted successfully"}

@mcp.tool()
def list_expenses(start_date: str, end_date: str) -> list[dict]:
    '''List all entries (expenses and credits) within an inclusive date range (YYYY-MM-DD).'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, type, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC, id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date: str, end_date: str, group_by: Literal["category", "month", "year"] = "category", category: str | None = None) -> list[dict]:
    '''Summarize expenses and credits within a date range (YYYY-MM-DD). Group by category, month, or year.'''
    with sqlite3.connect(DB_PATH) as c:
        if group_by == "month":
            group_col = "strftime('%Y-%m', date)"
            select_col = f"{group_col} AS month"
        elif group_by == "year":
            group_col = "strftime('%Y', date)"
            select_col = f"{group_col} AS year"
        else:
            group_col = "category"
            select_col = "category"

        query = f"""
            SELECT {select_col}, type, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += f" GROUP BY {group_col}, type ORDER BY {group_col} ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def add_category(category: str, subcategories: list[str] | None = None) -> dict:
    '''Add a new category to the categories.json file, with an optional list of subcategories.'''
    try:
        with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    if category in data:
        return {"status": "error", "message": f"Category '{category}' already exists."}
    
    data[category] = subcategories if subcategories else ["other"]
    
    with open(CATEGORIES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    return {"status": "ok", "message": f"Added category '{category}'"}

@mcp.resource("expense://categories", mime_type="application/json")
def categories() -> str:
    # Read fresh each time so you can edit the file without restarting
    try:
        with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "{}"

if __name__ == "__main__":
    mcp.run()