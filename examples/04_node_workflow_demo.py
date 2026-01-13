#!/usr/bin/env python3
"""
Example 4: Complete Node Workflow Demo

This example demonstrates how all 5 nodes work together in the LangGraph workflow.
It shows the state changes as data flows through each node.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent import create_agent_graph, AgentState
from langchain_core.messages import HumanMessage

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def print_state(node_name: str, state: dict, step: int):
    """Print the state after each node execution."""
    print(f"\n{'='*80}")
    print(f"Step {step}: {node_name}")
    print(f"{'='*80}")
    
    print(f"\n📋 State Overview:")
    print(f"   Task Type: {state.get('task_type', 'Not set')}")
    print(f"   Session ID: {state.get('session_id', 'Not set')}")
    print(f"   Messages: {len(state.get('messages', []))} messages")
    
    if state.get('augment_result'):
        result_preview = str(state['augment_result'])[:150]
        print(f"\n🔍 Augment Result Preview:")
        print(f"   {result_preview}...")
    
    if state.get('analysis'):
        print(f"\n📊 Analysis:")
        print(f"   {state['analysis']}")
    
    if state.get('final_output'):
        output_preview = str(state['final_output'])[:200]
        print(f"\n✅ Final Output Preview:")
        print(f"   {output_preview}...")


def main():
    print("=" * 80)
    print("Example 4: Complete Node Workflow Demo")
    print("=" * 80)
    print("\nThis example shows how data flows through all 5 nodes:")
    print("  1. Planner Node      → Classifies the task")
    print("  2. Augment Executor  → Executes via Augment SDK")
    print("  3. Analyzer Node     → Processes the results")
    print("  4. Formatter Node    → Formats the output")
    print("  5. Cleanup Node      → Cleans up resources")
    
    # Check for GitHub token
    if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
        print("\n❌ Please set GITHUB_PERSONAL_ACCESS_TOKEN environment variable")
        return
    
    # Create the agent
    print("\n🤖 Creating LangGraph agent...")
    agent = create_agent_graph()
    
    # Define the task
    task = "List my top 5 GitHub repositories by stars"
    
    print(f"\n📝 User Task: {task}")
    print("\n🔄 Starting workflow execution...\n")
    
    # Create initial state
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
    
    print("=" * 80)
    print("Initial State")
    print("=" * 80)
    print(f"\n📋 Initial State:")
    print(f"   Task: {task}")
    print(f"   Task Type: None (will be classified)")
    print(f"   Session ID: None (will be created)")
    print(f"   Messages: 1 message (user input)")
    
    try:
        # Execute the workflow with streaming to see each node
        print("\n\n" + "🚀" * 40)
        print("WORKFLOW EXECUTION")
        print("🚀" * 40)
        
        # Stream through the workflow to see each step
        step = 1
        for event in agent.stream(initial_state):
            for node_name, node_state in event.items():
                print_state(node_name, node_state, step)
                step += 1
        
        # Get final result
        final_result = agent.invoke(initial_state)
        
        # Print final summary
        print("\n\n" + "=" * 80)
        print("FINAL RESULT")
        print("=" * 80)
        
        print(f"\n📊 Workflow Summary:")
        print(f"   ✅ Task Type: {final_result.get('task_type')}")
        print(f"   ✅ Session ID: {final_result.get('session_id')}")
        print(f"   ✅ Total Messages: {len(final_result.get('messages', []))}")
        print(f"   ✅ Nodes Executed: 5 (Planner → Executor → Analyzer → Formatter → Cleanup)")
        
        print(f"\n📄 Final Output:")
        print("=" * 80)
        print(final_result['final_output'])
        print("=" * 80)
        
        # Explain what happened
        print("\n\n" + "💡" * 40)
        print("WHAT HAPPENED?")
        print("💡" * 40)
        
        print("\n1️⃣  PLANNER NODE:")
        print("    • Received user task")
        print("    • Classified as 'list_repos' task type")
        print("    • Added classification to state")
        
        print("\n2️⃣  AUGMENT EXECUTOR NODE:")
        print("    • Received task and task_type")
        print("    • Created Augment SDK session")
        print("    • Executed task via Augment SDK")
        print("    • Stored result and session_id in state")
        
        print("\n3️⃣  ANALYZER NODE:")
        print("    • Received Augment result")
        print("    • Processed the raw result")
        print("    • Added analysis to state")
        
        print("\n4️⃣  FORMATTER NODE:")
        print("    • Received analyzed result")
        print("    • Formatted output based on task_type")
        print("    • Created user-friendly final output")
        
        print("\n5️⃣  CLEANUP NODE:")
        print("    • Ended Augment SDK session")
        print("    • Released resources")
        print("    • Workflow complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

