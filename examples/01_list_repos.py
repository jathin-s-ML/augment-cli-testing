#!/usr/bin/env python3
"""
Example 1: List GitHub Repositories

This example demonstrates how to use Auggie SDK to list all your GitHub repositories.

run this python program using.
python examples/01_list_repos.py 2>/dev/null

"""

import os
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

    print("=" * 60)
    print("Example 1: List GitHub Repositories")
    print("=" * 60)

    # Initialize Auggie SDK
    print("\nInitializing Auggie SDK...")
    sdk = Auggie(model="sonnet4.5")

    # List all repositories
    print("\nFetching your GitHub repositories...\n")

    result = sdk.run(
        """
        List all my GitHub repositories also include forked repos too.
        For each repository, show:
        - Repository name
        - Visibility (public/private)
        - Description
        - Number of stars

        Format the output in a clean, readable way.
        """,
        return_type=str
    )

    print(result)
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

