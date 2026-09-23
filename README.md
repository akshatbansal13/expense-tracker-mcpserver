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

To use this server with Claude for Desktop, you need to add it to your configuration file.

1. Open your Claude Desktop configuration:
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Add the following configuration (make sure to use the absolute path to your project):

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\Users\\aksha\\OneDrive\\Desktop\\expense-tracker-mcpserver",
        "run",
        "expense-tracker-mcpserver"
      ]
    }
  }
}
```

3. Restart Claude Desktop. You should now see the expense tracker tools available!

---

## Building an MCPB Package

If you want to package the server into a standard `.mcpb` file for distribution, use the `mcpb` CLI.

1. **Validate the manifest:**
```bash
mcpb validate .
```
*(Ensure it outputs "Manifest schema validation passes!")*

2. **Pack the server into a `.mcpb` archive:**
```bash
mcpb pack . expense-tracker.mcpb
```
This will create a distributable file named `expense-tracker-0.1.0.mcpb`.

3. **Verify the package info:**
```bash
mcpb info expense-tracker.mcpb
```

---

## Development

To run the server locally for testing or development:
```bash
uv run expense-tracker-mcpserver
```
