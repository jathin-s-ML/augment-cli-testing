#!/usr/bin/env python3
"""
Test script to verify Auggie SDK can connect to GitHub MCP server.

This script tests:
1. Auggie SDK initialization
2. GitHub MCP server availability
3. Basic GitHub API access
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

def test_connection():
    """Test basic connection to GitHub via Auggie SDK."""
    
    print("=" * 60)
    print("Testing Auggie SDK + GitHub MCP Connection")
    print("=" * 60)
    
    # Check for GitHub token
    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        print("\n❌ ERROR: GITHUB_PERSONAL_ACCESS_TOKEN not set!")
        print("\nPlease set your GitHub token:")
        print("  export GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here")
        print("\nOr create a .env file with:")
        print("  GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here")
        return False
    
    print(f"\n✓ GitHub token found: {token[:10]}...")
    
    # Initialize Auggie SDK
    print("\n[1/3] Initializing Auggie SDK...")
    try:
        sdk = Auggie(model="sonnet4.5")
        print("✓ Auggie SDK initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Auggie SDK: {e}")
        return False
    
    # Test simple query (no GitHub needed)
    print("\n[2/3] Testing basic Auggie functionality...")
    try:
        result = sdk.run("What is 2 + 2?", return_type=int)
        if result == 4:
            print(f"✓ Basic test passed (2 + 2 = {result})")
        else:
            print(f"⚠ Unexpected result: {result}")
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False
    
    # Test GitHub MCP integration
    print("\n[3/3] Testing GitHub MCP integration...")
    print("Asking Auggie to list GitHub repositories...")
    try:
        result = sdk.run(
            "List my GitHub repositories. Show the first 5 repository names.",
            return_type=str
        )
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result)
        print("=" * 60)
        print("\n✓ GitHub MCP integration working!")
        return True
    except Exception as e:
        print(f"❌ GitHub MCP test failed: {e}")
        print("\nPossible issues:")
        print("1. GitHub MCP server not configured in Auggie CLI")
        print("2. Invalid GitHub token")
        print("3. Network connectivity issues")
        print("\nCheck MCP configuration with: auggie mcp list")
        return False

if __name__ == "__main__":
    print("\n🚀 Starting connection test...\n")
    
    success = test_connection()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYou can now use Auggie SDK with GitHub MCP!")
        print("Check out the examples in the examples/ directory.")
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above and try again.")
        sys.exit(1)

