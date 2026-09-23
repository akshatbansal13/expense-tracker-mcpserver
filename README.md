# Expense Tracker MCP Server

> **Demo Video:** [Insert link to your demo video here or upload a GIF/video file]

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

To add this server to Claude Desktop, you will need to install the `.mcpb` extension file.

1. **Build the `.mcpb` package:**
```bash
mcpb pack . expense-tracker.mcpb
```

2. **Add to Claude Desktop:**
   - Open the **Claude Desktop** application.
   - Go to **Settings** > **Extensions** > **Advanced Settings** > **Install Extension**.
   - Select the `expense-tracker.mcpb` file you just generated.

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

## Credits

Created by **[Your Name]**.

Connect with me:
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **LinkedIn:** [Your Profile](https://linkedin.com/in/yourusername)
- **Instagram:** [@yourusername](https://instagram.com/yourusername)
