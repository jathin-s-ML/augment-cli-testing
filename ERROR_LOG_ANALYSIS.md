# Error Log Analysis with Auggie SDK

## Quick Start

Use `05_analyze_error_log.py` to find bugs in your code by analyzing error logs!

## Usage

### Method 1: From Error Log File

```bash
python examples/05_analyze_error_log.py <owner/repo> <error_log_file>
```

**Example:**
```bash
python examples/05_analyze_error_log.py jathin-s-ML/fault-injector fault_injector_error.log
```

### Method 2: Paste Error Log Interactively

```bash
python examples/05_analyze_error_log.py <owner/repo>
```

Then paste your error log and press `Ctrl+D` when done.

### Method 3: Clean Version (No Warnings)

```bash
./run_clean.sh examples/05_analyze_error_log.py jathin-s-ML/fault-injector fault_injector_error.log
```

---

## Example: Fault Injector Bug

### Your Error Log:

```
📤 POST to SRE: 422
🔗 POST URL: http://135.232.101.211:8080/v1/fault-ledger
❌ SRE API failed: 422 - {"detail":[{"type":"float_type","loc":["body","configured_duration"],"msg":"Input should be a valid number","input":null}]}
```

### Run Analysis:

```bash
python examples/05_analyze_error_log.py jathin-s-ML/fault-injector fault_injector_error.log
```

### What It Does:

1. ✅ Reads your error log
2. ✅ Identifies the main error (configured_duration is null)
3. ✅ Searches your GitHub repository for the code
4. ✅ Shows you the exact file and line causing the bug
5. ✅ Explains what's wrong
6. ✅ Suggests how to fix it

---

## What Auggie Will Find:

The script will search your repository and show you:

- **File:** The Python file that posts to `/v1/fault-ledger`
- **Function:** The function handling workflow notifications
- **Line:** Where `configured_duration` is set to `None`
- **Fix:** How to extract duration from workflow config

---

## Tips

### Save Your Error Logs

Create a file with your error:
```bash
cat > my_error.log << 'EOF'
[paste your error log here]
EOF
```

Then analyze:
```bash
python examples/05_analyze_error_log.py owner/repo my_error.log
```

### Use with Any Repository

Works with any GitHub repository you have access to:
```bash
python examples/05_analyze_error_log.py maplelabs/fault-injector error.log
python examples/05_analyze_error_log.py jathin-s-ML/ai-sre-ops error.log
```

### Combine with Other Examples

1. Find the bug:
   ```bash
   python examples/05_analyze_error_log.py owner/repo error.log
   ```

2. Search for related code:
   ```bash
   python examples/04_search_code.py "configured_duration"
   ```

3. Review recent changes:
   ```bash
   python examples/02_get_pr_details.py owner/repo 123
   ```

---

## Advanced Usage

### Pipe Error from Command

```bash
# Capture error from a running command
your_command 2>&1 | tee error.log
python examples/05_analyze_error_log.py owner/repo error.log
```

### Multiple Repositories

```bash
# Check multiple repos for the same error pattern
python examples/05_analyze_error_log.py repo1 error.log
python examples/05_analyze_error_log.py repo2 error.log
```

---

## Sample Error Log Included

We've included `fault_injector_error.log` as an example. Try it:

```bash
python examples/05_analyze_error_log.py jathin-s-ML/fault-injector fault_injector_error.log
```

This will analyze the actual error you reported and find the bug!

---

## What Makes This Powerful?

🔍 **AI-Powered Analysis**
- Understands error messages
- Searches your actual code
- Finds root cause, not just symptoms

🎯 **Repository-Specific**
- Searches YOUR code
- Shows YOUR files
- Suggests fixes for YOUR codebase

⚡ **Fast**
- No manual code searching
- No guessing
- Direct to the problem

---

## Troubleshooting

### "Repository not found"
Make sure you have access to the repository and your GitHub token is set.

### "No error log provided"
Make sure your error log file exists or paste content when prompted.

### Async warnings
Use the clean version:
```bash
./run_clean.sh examples/05_analyze_error_log.py owner/repo error.log
```

---

**Happy Bug Hunting!** 🐛🔍

