# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for managing and tracking personal expenses. This server integrates directly with Claude Desktop, allowing the AI to add expenses to a local database and provide summaries.

## Features
- **Add Expenses:** Log new expenses with a description, amount, and category.
- **View Summaries:** Retrieve total expenses and breakdowns by category.
- **Local Storage:** Stores all your financial data locally in an SQLite database.

## Prerequisites
- **Python** (version specified in `.python-version`)
- **uv** (Python package and project manager)
- **mcpb** (MCP Builder CLI, for building the distribution package)

---

## Installation & Setup (Claude Desktop)

The modern way to add this server to Claude Desktop is by installing the packed `.mcpb` file.

1. **First, build the `.mcpb` package:**
```bash
mcpb pack . expense-tracker.mcpb
```

2. **Add to Claude Desktop:**
   - Open the **Claude Desktop** application.
   - Go to **Settings** (usually via the profile icon or menu).
   - Navigate to the **Developer** or **MCP** section.
   - Click **Add Server** (or **Install Server**).
   - Choose to install from a file and select the `expense-tracker.mcpb` file you just generated.

3. **Restart Claude Desktop** if prompted, and your expense tracker tools will be ready to use!

---

## Building & Verification

If you are modifying the server and want to verify your build:

1. **Validate the manifest:**
```bash
mcpb validate .
```

2. **Verify the packaged info:**
```bash
mcpb info expense-tracker.mcpb
```

---

## Development

To run the server locally for testing or development:
```bash
uv run expense-tracker-mcpserver
```
