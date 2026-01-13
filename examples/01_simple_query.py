#!/usr/bin/env python3
"""
Example 1: Simple Query using LangGraph + Augment SDK

This example demonstrates a basic query to list GitHub repositories.
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
    print("=" * 80)
    print("Example 1: Simple Query - List GitHub Repositories")
    print("=" * 80)
    
    # Check for GitHub token
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("\n❌ Please set GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
        return
    
    # Create the agent
    print("\n🤖 Creating LangGraph agent...")
    agent = create_agent_graph()
    
    # Define the task
    # task = "List all my GitHub repositories. Show name, visibility, and stars."
    # task = "List all my github repositories in which i have read access only"
    # task = "List all the open prs in augment-cli-testing repo"

    # task = """Review pull request for pr number 1 in repository augment-cli-testing.

    # Please analyze:
    # 1. Code quality and style
    # 2. Potential bugs or issues
    # 3. Security concerns
    # 4. Performance implications
    # 5. Test coverage

    # Provide specific, actionable feedback."""

    # task = "list GitHub issues (bug reports, not pull requests) in fault-injector repo"    
    # task = "can u identify any issue in augment-cli-testing"    
    task = "Review pull request #1 in the augment-cli-testing repository and add a comment if there are any improvements needed. Analyze the code changes and provide specific, actionable feedback on code quality, potential bugs, or best practices."
    
# # Step 1: Analyze
# task1 = "Analyze this error: 422 validation error on configured_duration. Keep under 200 words."

# # Step 2: Find code
# task2 = "In fault-injector repo, find the file with configured_duration. Show only: file path, function name, 5-line snippet."

# # Step 3: Git history
# task3 = "Show the 3 most recent commits that modified [that file]. Brief summary only."
    
    print(f"\n📝 Task: {task}")
    print("\n🔄 Running agent workflow...\n")
    
    # Run the agent
    initial_state = {
        "messages": [HumanMessage(content=task)],
        "task": task,
        "augment_result": None,
        "final_output": None,
        "session_id": None,
        "metadata": {}
    }
    
    try:
        # Execute the workflow
        result = agent.invoke(initial_state)
        
        # Print the final output
        print("=" * 80)
        print("RESULT:")
        print("=" * 80)
        print(result["final_output"])
        print("\n" + "=" * 80)
        
        # Print workflow metadata
        print("\n📊 Workflow Metadata:")
        print(f"   Session ID: {result.get('session_id')}")
        print(f"   Messages: {len(result.get('messages', []))} messages")

        # Detect result type from output
        final_output = result.get('final_output', '')
        if '## Pull Requests' in final_output:
            detected_type = 'Pull Requests'
        elif '## Repositories' in final_output:
            detected_type = 'Repositories'
        elif '## Error Analysis' in final_output:
            detected_type = 'Error Analysis'
        elif '## Code Review' in final_output:
            detected_type = 'Code Review'
        else:
            detected_type = 'General Query'
        print(f"   Detected Type: {detected_type}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

