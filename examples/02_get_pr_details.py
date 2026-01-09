#!/usr/bin/env python3
"""
Example 2: Get Pull Request Details

This example demonstrates how to fetch details about a specific pull request.

python examples/02_get_pr_details.py jathin-s-ML/augment-cli-testing 1 2>/dev/null

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
    
    # Get PR details from command line
    if len(sys.argv) < 3:
        print("Usage: python 02_get_pr_details.py <owner/repo> <pr_number>")
        print("Example: python 02_get_pr_details.py jathin-s-ML/ai-sre-ops 123")
        return
    
    repo = sys.argv[1]
    pr_number = sys.argv[2]
    
    print("=" * 60)
    print(f"Example 2: Get PR Details for {repo} #{pr_number}")
    print("=" * 60)
    
    # Initialize Auggie SDK
    print("\nInitializing Auggie SDK...")
    sdk = Auggie(model="sonnet4.5")

    try:
        # Get PR details
        print(f"\nFetching PR #{pr_number} details...\n")

        result = sdk.run(
            f"""
            Get details for pull request #{pr_number} in repository {repo}.

            Show:
            - PR title and description
            - Author
            - Status (open/closed/merged)
            - Number of commits
            - Files changed
            - Lines added/removed
            - Comments count
            - Review status

            Format the output in a clean, readable way.
            """,
            return_type=str
        )

        print(result)
        print("\n" + "=" * 60)
    finally:
        # Properly shutdown the SDK
        sdk.stop()

if __name__ == "__main__":
    main()

