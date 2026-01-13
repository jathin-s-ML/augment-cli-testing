#!/usr/bin/env python3
"""
Example 3: Session Management Demo

This example demonstrates how sessions work in the LangGraph agent.
It shows the difference between tasks with and without sessions.
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


def run_task_with_session(agent, task, task_type="code_review"):
    """Run a task that uses session (for complex tasks)."""
    initial_state = {
        "messages": [HumanMessage(content=task)],
        "task": task,
        "task_type": task_type,  # Force task type to use session
        "augment_result": None,
        "analysis": None,
        "final_output": None,
        "session_id": None,
        "metadata": {}
    }
    
    result = agent.invoke(initial_state)
    return result


def main():
    print("=" * 80)
    print("Example 3: Session Management Demo")
    print("=" * 80)
    
    # Check for GitHub token
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("\n❌ Please set GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
        return
    
    # Create the agent
    print("\n🤖 Creating LangGraph agent...")
    agent = create_agent_graph()
    
    # ========================================================================
    # Demo 1: Simple task (no session)
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 1: Simple Task (No Session)")
    print("=" * 80)
    
    task1 = "List my GitHub repositories (just the names)"
    print(f"\n📝 Task: {task1}")
    print("🔄 Running without session...\n")
    
    result1 = run_task_with_session(agent, task1, task_type="list_repos")
    
    print(f"✅ Result: {result1['final_output'][:200]}...")
    print(f"📊 Session ID: {result1.get('session_id')}")
    print("   (None = no session used)")
    
    # ========================================================================
    # Demo 2: Complex task (with session)
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 2: Complex Task (With Session)")
    print("=" * 80)
    
    task2 = "Review the code quality of my most recent repository"
    print(f"\n📝 Task: {task2}")
    print("🔄 Running with session...\n")
    
    result2 = run_task_with_session(agent, task2, task_type="code_review")
    
    print(f"✅ Result: {result2['final_output'][:200]}...")
    print(f"📊 Session ID: {result2.get('session_id')}")
    print("   (Should have a session ID)")
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    
    print("\n📋 Task Types and Session Usage:")
    print("   • list_repos      → No session (faster, stateless)")
    print("   • general_query   → No session (faster, stateless)")
    print("   • code_review     → With session (maintains context)")
    print("   • error_analysis  → With session (maintains context)")
    
    print("\n💡 Why use sessions?")
    print("   • Maintains conversation context across multiple calls")
    print("   • Useful for multi-step tasks (analyze → fix → test)")
    print("   • Allows follow-up questions without repeating context")
    
    print("\n🎯 When to use sessions:")
    print("   ✅ Code reviews (may need follow-up questions)")
    print("   ✅ Debugging (analyze error → find code → suggest fix)")
    print("   ✅ Multi-step workflows")
    print("   ❌ Simple queries (list repos, get info)")
    print("   ❌ One-off tasks")


if __name__ == "__main__":
    main()

