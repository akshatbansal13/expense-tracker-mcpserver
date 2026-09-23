# Expense Tracker MCP Server

> **Demo Video:** [Insert your video URL here]

A Model Context Protocol (MCP) server for managing and tracking personal expenses. This server integrates directly with Claude Desktop, allowing the AI to add expenses to a local database and provide summaries.

## Features
- **Add Expenses:** Log new expenses with a description, amount, and category.
- **View Summaries:** Retrieve total expenses and breakdowns by category.
- **Local Storage:** Stores all your financial data locally in an SQLite database.

## 🚀 Local Development

1. **Clone the repository**
```bash
git clone https://github.com/akshatbansal13/expense-tracker-mcpserver.git
cd expense-tracker-mcpserver
```

2. **Install dependencies**
```bash
uv sync
```

3. **Run the MCP server**
```bash
uv run fastmcp run src/expense_tracker_mcpserver/server.py
```

4. **Inspect the server**
```bash
uv run fastmcp inspect src/expense_tracker_mcpserver/server.py
```
This allows you to verify the available tools and resources.

## 📦 Claude Desktop Installation

The project can be packaged as an MCPB extension.

**Install MCPB CLI**
```bash
npm install -g @anthropic-ai/mcpb
```

**Validate the manifest**
```bash
mcpb validate .
```
*Expected:*
```text
Manifest schema validation passes!
```

**Build the extension**
```bash
mcpb pack . expense-tracker.mcpb
```
*This generates:*
```text
expense-tracker.mcpb
```

**Install in Claude Desktop**

Open:
- **Claude Desktop**
- → **Settings**
- → **Extensions**
- → **Advanced Settings**
- → **Install Extension**

Select:
`expense-tracker.mcpb`

After installation, the Expense Tracker MCP server can be used directly from Claude Desktop.

---

## Credits

Created by **Akshat Bansal**.

Connect with me:
- **GitHub:** [akshatbansal13](https://github.com/akshatbansal13)
- **LinkedIn:** [Akshat Bansal](https://www.linkedin.com/in/akshat13bansal)
- **Instagram:** [@akshxtt_13](https://www.instagram.com/akshxtt_13)
