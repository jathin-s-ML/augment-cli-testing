# GitHub + Auggie SDK Integration

Use **Auggie SDK** with **GitHub MCP Server** to perform GitHub operations using natural language.

---

## 🚀 Quick Start (5 Minutes)

### Step 0: Install Dependencies

```bash
pip install python-dotenv
```

### Step 1: Get GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:org`, `read:user`
4. Generate and copy the token (starts with `ghp_`)

### Step 2: Set Environment Variable

**Option 1: Create .env file (Recommended)**
```bash
cd github-auggie-sdk
echo "GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here" > .env
```

**Option 2: Export environment variable**
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

### Step 3: Verify GitHub MCP is Configured

```bash
auggie mcp list
```

You should see `github` in the list. If not:

```bash
auggie mcp add github \
  --transport stdio \
  --command "docker" \
  --args "run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github"
```

### Step 4: Test It

```bash
python tests/test_connection.py
```

Expected output: `✅ ALL TESTS PASSED!`

### Step 5: Use It!

```python
from auggie_sdk import Auggie

sdk = Auggie(model="sonnet4.5")
result = sdk.run("List all my GitHub repositories")
print(result)
```

**That's it!** No complex setup, no SDK modifications needed.

---

## 📚 Examples

### 🧹 Running Without Warnings

**Option 1: Use the clean interactive demo**
```bash
python interactive_demo_clean.py
```

**Option 2: Use the wrapper script**
```bash
./run_clean.sh interactive_demo.py
./run_clean.sh examples/01_list_repos.py
```

**Option 3: Redirect stderr manually**
```bash
python examples/01_list_repos.py 2>/dev/null
```

---

### List Repositories
```bash
python examples/01_list_repos.py
# Or clean: ./run_clean.sh examples/01_list_repos.py
```

### Get PR Details
```bash
python examples/02_get_pr_details.py owner/repo 123
# Or clean: ./run_clean.sh examples/02_get_pr_details.py owner/repo 123
```

### AI Code Review
```bash
python examples/03_review_pr.py owner/repo 123
```

### Search Code
```bash
python examples/04_search_code.py "TODO"
```

### Analyze Error Logs (Find Bugs!)
```bash
# From a file
python examples/05_analyze_error_log.py owner/repo error.log

# Or paste error log interactively
python examples/05_analyze_error_log.py owner/repo

# Example with your fault-injector error
python examples/05_analyze_error_log.py jathin-s-ML/fault-injector fault_injector_error.log
```

### Interactive Mode

**Clean version (recommended - no warnings):**
```bash
python interactive_demo_clean.py
```

**Standard version:**
```bash
python interactive_demo.py
```

---

## 🎯 How It Works

```
Your Python Code
    ↓
Auggie SDK
    ↓
Auggie CLI (auto-detects MCP servers)
    ↓
GitHub MCP Server
    ↓
GitHub API
```

**Key Insight:** Auggie SDK automatically uses configured MCP servers. You just write natural language queries!

---

## 💡 Usage Patterns

### Simple Query
```python
sdk.run("How many repositories do I have?")
```

### Detailed Request
```python
sdk.run("""
List my repositories and show:
- Name
- Stars
- Last updated
""")
```

### Complex Analysis
```python
sdk.run("""
Review PR #123 in owner/repo.
Check for security issues and performance problems.
Provide specific recommendations.
""")
```

---

## 📁 Project Structure

```
github-auggie-sdk/
├── README.md                    # This file
├── .env.example                 # Environment template
├── interactive_demo.py          # Interactive CLI
├── examples/
│   ├── 01_list_repos.py        # List repositories
│   ├── 02_get_pr_details.py    # Get PR details
│   ├── 03_review_pr.py         # AI code review
│   └── 04_search_code.py       # Search code
└── tests/
    └── test_connection.py       # Connection test
```

---

## 🔧 What You Can Do

### Repository Operations
- List all repositories (public + private)
- Get repository details
- Search repositories
- Analyze repository activity

### Pull Request Operations
- List PRs (open/closed/merged)
- Get PR details and diffs
- AI-powered code review
- Analyze PR patterns

### Code Operations
- Search code across all repos
- Find patterns and anti-patterns
- Analyze code quality
- Security analysis

### Advanced
- Team analytics
- Contribution analysis
- Issue management
- Workflow automation

---

## ⚠️ Troubleshooting

### Async Cleanup Warnings

**Problem:** You see warnings like:
```
Task was destroyed but it is pending!
RuntimeWarning: coroutine 'AuggieACPClient._async_stop' was never awaited
```

**Solution:** These are harmless warnings from the Auggie SDK's async cleanup. Choose one:

1. **Use the clean interactive demo:**
   ```bash
   python interactive_demo_clean.py
   ```

2. **Use the wrapper script:**
   ```bash
   ./run_clean.sh examples/01_list_repos.py
   ```

3. **Redirect stderr:**
   ```bash
   python examples/01_list_repos.py 2>/dev/null
   ```

**Note:** These warnings don't affect functionality - your scripts work perfectly!

---

### "GITHUB_PERSONAL_ACCESS_TOKEN not set"
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

### "GitHub MCP server not configured"
```bash
auggie mcp add github --transport stdio --command docker --args "run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github"
```

### "Permission denied"
Check your token has these scopes:
- ✅ `repo` - Full control of private repositories
- ✅ `read:org` - Read org and team membership
- ✅ `read:user` - Read user profile data

### "Docker not found"
Make sure Docker is installed and running (required for GitHub MCP server)

---

## 🎓 Key Concepts

### No SDK Modification Needed
Auggie SDK already supports MCP servers. Just configure and use!

### Natural Language Interface
No need to learn GitHub API. Just ask in plain English.

### Automatic Tool Selection
Auggie figures out which GitHub MCP tools to use based on your query.

### Environment-Based Auth
GitHub token is passed via environment variable to MCP server.

---

## 📝 Prerequisites

- ✅ Auggie CLI installed
- ✅ Python 3.9+
- ✅ Auggie SDK (`pip install auggie-sdk`)
- ✅ Docker (for GitHub MCP server)
- ✅ GitHub Personal Access Token

---

## 🚧 Limitations

- Requires Auggie CLI (can't use SDK standalone)
- Token must be in environment variable
- Need clear natural language prompts for best results
- Docker required for GitHub MCP server

---

## 🎯 Next Steps

1. ✅ Run `python tests/test_connection.py`
2. ✅ Try examples in `examples/`
3. ✅ Run `python interactive_demo.py` for interactive mode
4. ✅ Build your own GitHub automation!

---

## 📖 Learn More

- [Auggie SDK Documentation](https://docs.augmentcode.com)
- [GitHub MCP Server](https://github.com/modelcontextprotocol/servers)
- [MCP Protocol](https://modelcontextprotocol.io)

---

**Happy Coding! 🎉**

