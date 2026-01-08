# 🤖 Manual Code Review Agent - Complete Guide

## ✅ What We've Built

You now have a **fully functional manual code review agent** that works without the subagents feature!

### 📁 Files Created

```
.augment/
├── agents/
│   └── code-review.md              # Subagent config (for when feature is enabled)
└── scripts/
    ├── code-review.sh              # Main review script ⭐
    ├── code-review-prompt.txt      # Review criteria template
    ├── setup-aliases.sh            # Alias setup helper
    └── USAGE-GUIDE.md              # This file
```

---

## 🚀 Quick Start Guide

### Step 1: Setup Aliases (One-time)

```bash
# Run the setup script
./.augment/scripts/setup-aliases.sh

# Reload your shell
source ~/.bashrc  # or ~/.zshrc for zsh
```

This creates convenient shortcuts:
- `cr` - Quick code review
- `cr-all` - Review all changes
- `cr-security` - Security-focused review
- `cr-perf` - Performance review
- `cr-bugs` - Bug-focused review
- `cr-diff` - Show diff before review

### Step 2: Make Changes & Stage Them

```bash
# Edit your code
vim src/myfile.js

# Stage the changes
git add src/myfile.js
```

### Step 3: Run Code Review

```bash
# Using alias (recommended)
cr

# Or directly
./.augment/scripts/code-review.sh
```

---

## 📖 Usage Examples

### Example 1: Basic Review (Staged Changes)

```bash
# Stage your changes
git add .

# Run review
cr
```

### Example 2: Review All Uncommitted Changes

```bash
# Review everything (staged + unstaged)
cr-all
```

### Example 3: Security-Focused Review

```bash
# Stage security-sensitive files
git add src/auth.js src/payment.js

# Run security review
cr-security
```

### Example 4: Review Specific Files

```bash
# Review only JavaScript files
code-review --files "*.js"

# Review only Go files
code-review --files "*.go"
```

### Example 5: Review a Specific Commit

```bash
# Review a past commit
code-review --commit abc123
```

### Example 6: Custom Focus with Message

```bash
# Stage changes
git add .

# Review with custom instructions
code-review "Check for race conditions and concurrency issues"
```

### Example 7: Show Diff Before Review

```bash
# See what will be reviewed
cr-diff
```

---

## 🎯 What the Agent Reviews

### 🐛 Correctness & Bugs
- Logic errors and edge cases
- Null/undefined references
- Off-by-one errors
- Race conditions
- Resource leaks

### 🔒 Security
- SQL/NoSQL injection
- XSS vulnerabilities
- Authentication issues
- Sensitive data exposure
- Input validation

### ⚡ Performance
- Inefficient algorithms
- N+1 query problems
- Memory leaks
- Missing caching

### ✨ Code Quality
- Code duplication
- High complexity
- Poor naming
- Missing error handling

### 📚 Best Practices
- SOLID principles
- Design patterns
- Framework conventions

---

## 📊 Review Output Format

Reviews are structured as:

**🔴 CRITICAL ISSUES** - Must fix before merge
- Security vulnerabilities
- Data loss risks
- Breaking changes

**🟡 WARNINGS** - Should fix
- Potential bugs
- Bad practices
- Performance issues

**🟢 SUGGESTIONS** - Nice to have
- Optimizations
- Refactoring ideas

**✅ POSITIVE NOTES** - What was done well
- Good practices
- Clean code examples

---

## 🔧 Advanced Usage

### All Command Options

```bash
code-review [OPTIONS] [MESSAGE]

Options:
  -h, --help              Show help
  -a, --all               Review all changes (not just staged)
  -f, --files PATTERN     Review specific files
  -c, --commit HASH       Review specific commit
  --focus AREA            Focus on: security, performance, bugs
  --staged                Review staged only (default)
  --diff                  Show diff before review
```

### Combining Options

```bash
# Review all JS files with security focus
code-review --all --files "*.js" --focus security

# Review specific commit with diff
code-review --commit abc123 --diff
```

---

## 💡 Workflow Integration

### Pre-Commit Workflow

```bash
# 1. Make changes
vim src/feature.js

# 2. Stage changes
git add src/feature.js

# 3. Review
cr

# 4. Fix issues if any
vim src/feature.js
git add src/feature.js

# 5. Commit
git commit -m "Add new feature"
```

### Pull Request Workflow

```bash
# Review all changes in your branch
git checkout feature-branch
cr-all

# Or review diff against main
git diff main...HEAD > /tmp/pr.diff
# Then manually review the diff
```

---

## 🎓 Best Practices

1. **Review Early** - Run reviews before committing
2. **Small Changesets** - Review smaller, logical chunks
3. **Focus Reviews** - Use `--focus` for targeted analysis
4. **Act on Feedback** - Address critical issues immediately
5. **Iterate** - Re-review after making fixes

---

## 🐛 Troubleshooting

### "auggie is not installed"
```bash
npm install -g @augment/cli
# or
npm install -g auggie
```

### "No staged changes found"
```bash
# Make sure you've staged files
git add <files>

# Or use --all to review unstaged
cr-all
```

### "Permission denied"
```bash
chmod +x .augment/scripts/code-review.sh
```

### Script not found
```bash
# Use full path
/path/to/project/.augment/scripts/code-review.sh

# Or cd to project root first
cd /path/to/project
./augment/scripts/code-review.sh
```

---

## 🔄 Testing with Example Repo

We tested this with: https://github.com/jathin-s-ML/todo.git

```bash
# Clone the repo
git clone https://github.com/jathin-s-ML/todo.git
cd todo

# Copy the scripts
cp -r /path/to/.augment ./

# Make a change
vim main.go

# Stage and review
git add main.go
./.augment/scripts/code-review.sh
```

---

## 📝 Customization

### Modify Review Criteria

Edit `.augment/scripts/code-review-prompt.txt` to:
- Add/remove review areas
- Change severity levels
- Add project-specific rules
- Customize output format

### Add Custom Aliases

Edit `~/.bashrc` or `~/.zshrc`:

```bash
# Project-specific reviews
alias cr-api='code-review --files "src/api/*"'
alias cr-frontend='code-review --files "src/components/*"'
alias cr-backend='code-review --files "internal/*"'
```

---

## 🆚 Subagent vs Manual Agent

| Feature | Subagent (When Enabled) | Manual Script |
|---------|------------------------|---------------|
| Ease of use | `auggie --agent code-review` | `cr` or `./.augment/scripts/code-review.sh` |
| Setup | Just create .md file | Run setup-aliases.sh |
| Integration | Built into auggie | Standalone script |
| Customization | Edit .md file | Edit prompt.txt |
| Availability | Requires feature flag | Works now! ✅ |

---

## 🎉 You're All Set!

Your manual code review agent is ready to use. Here's what to do next:

1. ✅ Run the alias setup: `./.augment/scripts/setup-aliases.sh`
2. ✅ Reload your shell: `source ~/.bashrc`
3. ✅ Make some changes and stage them
4. ✅ Run your first review: `cr`

Happy coding! 🚀

---

## 📞 Need Help?

- Check script help: `code-review --help`
- View this guide: `cat .augment/scripts/USAGE-GUIDE.md`
- Check auggie: `auggie --version`

