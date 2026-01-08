# 🤖 Manual Code Review Agent

A shell-based code review agent that mimics Augment subagent functionality using `auggie`.

## 📋 What's Included

- **code-review.sh** - Main code review script
- **code-review-prompt.txt** - Comprehensive review prompt template
- **setup-aliases.sh** - Convenient alias setup script
- **README.md** - This documentation

## 🚀 Quick Start

### 1. Setup Aliases (Recommended)

```bash
# Run the setup script
./.augment/scripts/setup-aliases.sh

# Reload your shell configuration
source ~/.bashrc  # or ~/.zshrc for zsh
```

### 2. Make Some Changes

```bash
# Edit some files
vim src/example.js

# Stage your changes
git add src/example.js
```

### 3. Run Code Review

```bash
# Using alias (if setup)
cr

# Or directly
./.augment/scripts/code-review.sh
```

## 📖 Usage

### Basic Commands

```bash
# Review staged changes (default)
code-review

# Review all uncommitted changes
code-review --all

# Review with custom message
code-review "Focus on security vulnerabilities"

# Show diff before review
code-review --diff
```

### Advanced Options

```bash
# Review specific commit
code-review --commit abc123

# Review specific files
code-review --files "*.js"

# Focus on specific area
code-review --focus security
code-review --focus performance
code-review --focus bugs

# Combine options
code-review --all --focus security --diff
```

### Using Aliases (After Setup)

```bash
cr                  # Quick review of staged changes
cr-all              # Review all changes
cr-security         # Security-focused review
cr-perf             # Performance-focused review
cr-bugs             # Bug-focused review
cr-diff             # Show diff before review
```

## 🎯 Review Areas

The agent checks for:

- **🐛 Correctness & Bugs** - Logic errors, edge cases, null references
- **🔒 Security** - Injection attacks, auth issues, data exposure
- **⚡ Performance** - Inefficient algorithms, N+1 queries, memory leaks
- **✨ Code Quality** - DRY violations, complexity, naming
- **📚 Best Practices** - SOLID principles, design patterns
- **🧪 Testing** - Missing tests, inadequate coverage
- **📝 Documentation** - Comments, API docs, README updates

## 📊 Output Format

Reviews are structured as:

- **🔴 CRITICAL ISSUES** - Must fix before merge
- **🟡 WARNINGS** - Should fix
- **🟢 SUGGESTIONS** - Nice to have
- **✅ POSITIVE NOTES** - What was done well

## 💡 Examples

### Example 1: Pre-commit Review

```bash
# Make changes
vim src/auth.js

# Stage changes
git add src/auth.js

# Review before committing
cr

# If review passes, commit
git commit -m "Add authentication"
```

### Example 2: Security Review

```bash
# Stage security-sensitive changes
git add src/payment.js

# Run security-focused review
cr-security
```

### Example 3: Review Entire Feature Branch

```bash
# Review all changes in current branch
cr-all
```

### Example 4: Review Specific Commit

```bash
# Review a specific commit
code-review --commit abc123
```

## 🔧 Customization

### Modify Review Prompt

Edit `.augment/scripts/code-review-prompt.txt` to customize:
- Review criteria
- Output format
- Focus areas
- Severity levels

### Add Custom Aliases

Edit your `~/.bashrc` or `~/.zshrc`:

```bash
# Custom review for your project
alias cr-api='code-review --files "src/api/*" --focus security'
alias cr-frontend='code-review --files "src/components/*"'
alias cr-tests='code-review --files "tests/*"'
```

## 🐛 Troubleshooting

### "auggie is not installed"
```bash
# Install auggie
npm install -g @augment/cli
```

### "No staged changes found"
```bash
# Stage your changes first
git add <files>

# Or use --all to review unstaged changes
code-review --all
```

### "Permission denied"
```bash
# Make script executable
chmod +x .augment/scripts/code-review.sh
```

### Changes too large
The script will warn if changes exceed 50,000 characters. Consider:
- Reviewing smaller changesets
- Using `--files` to filter specific files
- Breaking up large commits

## 🎓 Best Practices

1. **Review Early, Review Often** - Run reviews before committing
2. **Focus Reviews** - Use `--focus` for targeted analysis
3. **Incremental Reviews** - Review small, logical changesets
4. **Act on Feedback** - Address critical issues before merging
5. **Iterate** - Re-review after making fixes

## 🔄 Integration Ideas

### Git Hook (Pre-commit)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running code review..."
./.augment/scripts/code-review.sh --focus security

read -p "Proceed with commit? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi
```

### VS Code Task

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Code Review",
      "type": "shell",
      "command": "./.augment/scripts/code-review.sh",
      "problemMatcher": []
    }
  ]
}
```

Then run with `Ctrl+Shift+P` → "Tasks: Run Task" → "Code Review"

## 📝 Notes

- This is a **manual workaround** until subagents feature is enabled
- Requires `auggie` CLI to be installed
- Works with any git repository
- Reviews are powered by the same AI as Augment Agent

## 🆘 Support

If you encounter issues:
1. Check that `auggie` is installed: `auggie --version`
2. Verify git repository: `git status`
3. Check script permissions: `ls -la .augment/scripts/`
4. Review the prompt template for syntax errors

## 🎉 Enjoy Your Code Reviews!

Happy coding! 🚀

