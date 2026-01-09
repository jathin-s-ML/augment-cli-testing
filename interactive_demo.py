#!/usr/bin/env python3
"""
Interactive GitHub + Auggie SDK Demo

This script provides an interactive interface to explore GitHub operations
using Auggie SDK and natural language.
"""

import os
import sys
from pathlib import Path
from auggie_sdk import Auggie

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass  # dotenv not installed, will use system env vars

def print_header():
    """Print welcome header."""
    print("\n" + "=" * 70)
    print(" " * 15 + "GitHub + Auggie SDK Interactive Demo")
    print("=" * 70)
    print("\nAsk me anything about your GitHub repositories!")
    print("Examples:")
    print("  - List my repositories")
    print("  - Show my most starred repos")
    print("  - Review PR #123 in owner/repo")
    print("  - Search for 'TODO' in my code")
    print("\nType 'quit' or 'exit' to stop.")
    print("=" * 70 + "\n")

def check_setup():
    """Check if GitHub token is set."""
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        print("❌ ERROR: GITHUB_PERSONAL_ACCESS_TOKEN not set!\n")
        print("Please set your GitHub token:")
        print("  export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here\n")
        return False
    print(f"✓ GitHub token found: {token[:10]}...\n")
    return True

def main():
    """Run interactive demo."""
    print_header()
    
    # Check setup
    if not check_setup():
        sys.exit(1)
    
    # Initialize Auggie SDK
    print("Initializing Auggie SDK...")
    try:
        sdk = Auggie(model="sonnet4.5")
        print("✓ Auggie SDK ready!\n")
    except Exception as e:
        print(f"❌ Failed to initialize Auggie SDK: {e}")
        sys.exit(1)
    
    # Interactive loop
    while True:
        try:
            # Get user input
            print("-" * 70)
            query = input("\n🤖 Your question: ").strip()
            
            # Check for exit
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            
            # Skip empty input
            if not query:
                continue
            
            # Process query
            print("\n🔍 Processing...\n")
            result = sdk.run(query, return_type=str)
            
            # Display result
            print("=" * 70)
            print("RESULT:")
            print("=" * 70)
            print(result)
            print("=" * 70)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("Please try again with a different question.\n")

if __name__ == "__main__":
    main()

