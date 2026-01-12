#!/usr/bin/env python3
"""
Example 5: Analyze Error Logs and Find Root Cause

This example demonstrates how to use Auggie SDK to analyze error logs
and find the code that caused the issue in your GitHub repositories.
"""

import os
import sys
from pathlib import Path
from auggie_sdk import Auggie

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, will use system env vars

def main():
    # Check for GitHub token
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("❌ Please set GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
        print("\nOptions:")
        print("1. Create a .env file with: GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token")
        print("2. Or export it: export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token")
        return
    
    print("=" * 80)
    print("Example 5: Analyze Error Logs and Find Root Cause")
    print("=" * 80)
    
    # Get repository and error log
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python 05_analyze_error_log.py <owner/repo> [error_log_file]")
        print("\nExamples:")
        print("  python 05_analyze_error_log.py jathin-s-ML/fault-injector error.log")
        print("  python 05_analyze_error_log.py jathin-s-ML/fault-injector")
        print("\nIf no error log file is provided, you'll be prompted to paste the error.")
        return
    
    repo = sys.argv[1]
    error_log = None
    
    # Read error log from file or stdin
    if len(sys.argv) >= 3:
        error_log_file = sys.argv[2]
        try:
            with open(error_log_file, 'r') as f:
                error_log = f.read()
            print(f"\n✓ Loaded error log from: {error_log_file}")
        except FileNotFoundError:
            print(f"\n❌ Error log file not found: {error_log_file}")
            return
    else:
        print("\n📋 Paste your error log below (press Ctrl+D when done):")
        print("-" * 80)
        try:
            error_log = sys.stdin.read()
        except KeyboardInterrupt:
            print("\n\n❌ Cancelled")
            return
    
    if not error_log or not error_log.strip():
        print("\n❌ No error log provided")
        return
    
    print("\n" + "=" * 80)
    print(f"Analyzing error log for repository: {repo}")
    print("=" * 80)
    
    # Initialize Auggie SDK
    print("\nInitializing Auggie SDK...")
    sdk = Auggie(model="sonnet4.5")
    
    # Step 1: Analyze the error log (without searching repo yet)
    print("\n🔍 Step 1: Analyzing error log...\n")

    analysis = sdk.run(
        f"""
        Analyze this error log and identify the main issues:

        ERROR LOG:
        ```
        {error_log}
        ```

        Please provide:
        1. What is the main error?
        2. What API endpoint is failing?
        3. What is the error code and message?
        4. What might be the root cause based on the error message?

        Keep your response concise (under 500 words).
        """,
        return_type=str,
        timeout=120
    )

    print("=" * 80)
    print("ANALYSIS:")
    print("=" * 80)
    print(analysis)
    print("=" * 80)

    # Step 2: Search for the specific code
    print("\n🔍 Step 2: Searching repository for the problematic code...\n")

    result = sdk.run(
        f"""
        Based on this error analysis:
        {analysis}

        Search the {repo} repository and find:
        1. The file that makes the POST/PUT request to the SRE API
        2. Show me the exact code that's sending 'configured_duration' as null

        Keep your response focused - just show the relevant file path and code snippet.
        """,
        return_type=str,
        timeout=300
    )

    print("=" * 80)
    print("ROOT CAUSE:")
    print("=" * 80)
    print(result)
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()

