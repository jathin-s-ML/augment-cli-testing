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
    task = "List all the open prs in augment-cli-testing repo"
    
    print(f"\n📝 Task: {task}")
    print("\n🔄 Running agent workflow...\n")
    
    # Run the agent
    initial_state = {
        "messages": [HumanMessage(content=task)],
        "task": task,
        "task_type": None,
        "augment_result": None,
        "analysis": None,
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
        print(f"   Task Type: {result.get('task_type')}")
        print(f"   Session ID: {result.get('session_id')}")
        print(f"   Messages: {len(result.get('messages', []))} messages")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

