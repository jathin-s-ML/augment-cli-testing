#!/usr/bin/env python3
"""
Example 2: Code Review using LangGraph + Augment SDK

This example demonstrates how to review a GitHub pull request.

Usage:
    python examples/02_code_review.py owner/repo pr_number
    
Example:
    python examples/02_code_review.py jathin-s-ML/augment-cli-testing 1
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent import create_agent_graph
from langchain_core.messages import HumanMessage

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def main():
    if len(sys.argv) < 3:
        print("Usage: python 02_code_review.py owner/repo pr_number")
        print("Example: python 02_code_review.py facebook/react 12345")
        sys.exit(1)
    
    repo = sys.argv[1]
    pr_number = sys.argv[2]
    
    print("=" * 80)
    print(f"Example 2: Code Review - PR #{pr_number} in {repo}")
    print("=" * 80)
    
    # Check for GitHub token
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("\n❌ Please set GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
        return
    
    # Create the agent
    print("\n🤖 Creating LangGraph agent...")
    agent = create_agent_graph()
    
    # Define the task
    task = f"""
    Review pull request #{pr_number} in repository {repo}.
    
    Please analyze:
    1. Code quality and style
    2. Potential bugs or issues
    3. Security concerns
    4. Performance implications
    5. Test coverage
    
    Provide specific, actionable feedback.
    """
    
    print(f"\n📝 Task: Review PR #{pr_number}")
    print("\n🔄 Running agent workflow (this may take a few minutes)...\n")
    
    # Run the agent
    initial_state = {
        "messages": [HumanMessage(content=task)],
        "task": task,
        "task_type": None,
        "augment_result": None,
        "analysis": None,
        "final_output": None,
        "session_id": None,
        "metadata": {
            "repo": repo,
            "pr_number": pr_number
        }
    }
    
    try:
        # Execute the workflow
        result = agent.invoke(initial_state)
        
        # Print the final output
        print("=" * 80)
        print("CODE REVIEW RESULTS:")
        print("=" * 80)
        print(result["final_output"])
        print("\n" + "=" * 80)
        
        # Print workflow metadata
        print("\n📊 Workflow Metadata:")
        print(f"   Repository: {repo}")
        print(f"   PR Number: #{pr_number}")
        print(f"   Task Type: {result.get('task_type')}")
        print(f"   Session ID: {result.get('session_id')}")
        print(f"   Messages: {len(result.get('messages', []))} messages")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

