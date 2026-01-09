#!/usr/bin/env python3
"""
Example 4: Search Code Across Repositories

This example demonstrates how to search for code patterns across all your repositories.
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
    
    # Get search query from command line
    if len(sys.argv) < 2:
        print("Usage: python 04_search_code.py <search_query>")
        print("Example: python 04_search_code.py 'TODO'")
        print("Example: python 04_search_code.py 'def main'")
        return
    
    query = " ".join(sys.argv[1:])
    
    print("=" * 60)
    print(f"Example 4: Search Code for '{query}'")
    print("=" * 60)
    
    # Initialize Auggie SDK
    print("\nInitializing Auggie SDK...")
    sdk = Auggie(model="sonnet4.5")
    
    # Search code
    print(f"\nSearching for '{query}' across your repositories...\n")
    
    result = sdk.run(
        f"""
        Search for the code pattern: "{query}" across all my GitHub repositories.
        
        For each match, show:
        - Repository name
        - File path
        - Line number
        - Code snippet (with context)
        
        Limit to the first 20 matches.
        Format the output in a clean, readable way.
        """,
        return_type=str
    )
    
    print(result)
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()

