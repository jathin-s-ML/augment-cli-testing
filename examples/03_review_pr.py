#!/usr/bin/env python3
"""
Example 3: AI-Powered Pull Request Review

This example demonstrates how to use Auggie SDK to perform an AI-powered code review
of a pull request.
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
        print("Usage: python 03_review_pr.py <owner/repo> <pr_number>")
        print("Example: python 03_review_pr.py jathin-s-ML/ai-sre-ops 123")
        return
    
    repo = sys.argv[1]
    pr_number = sys.argv[2]
    
    print("=" * 60)
    print(f"Example 3: AI Code Review for {repo} #{pr_number}")
    print("=" * 60)
    
    # Initialize Auggie SDK
    print("\nInitializing Auggie SDK...")
    sdk = Auggie(model="sonnet4.5")
    
    # Perform code review
    print(f"\nAnalyzing PR #{pr_number}...\n")
    print("This may take a minute...\n")
    
    result = sdk.run(
        f"""
        Review pull request #{pr_number} in repository {repo}.
        
        Analyze the code changes and provide:
        
        1. **Summary**: Brief overview of what the PR does
        
        2. **Code Quality Issues**:
           - Code smells
           - Anti-patterns
           - Maintainability concerns
           - Naming conventions
        
        3. **Security Concerns**:
           - Potential vulnerabilities
           - Security best practices violations
           - Input validation issues
        
        4. **Performance Issues**:
           - Inefficient algorithms
           - N+1 queries
           - Resource usage concerns
        
        5. **Recommendations**:
           - Specific improvements
           - Best practices to follow
        
        For each issue, specify:
        - Severity (Critical/High/Medium/Low)
        - File and line number (if applicable)
        - Description
        - Recommendation
        
        Format the output in a clear, structured way.
        """,
        return_type=str
    )
    
    print(result)
    print("\n" + "=" * 60)
    print("\n💡 Tip: You can use this review to post comments on the PR!")

if __name__ == "__main__":
    main()

