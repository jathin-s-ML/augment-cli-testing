#!/usr/bin/env python3
"""
Example 6: Session Management with Session IDs

This example demonstrates how to use session IDs in Auggie SDK to maintain
conversation continuity across multiple requests.
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
    pass

def main():
    print("=" * 80)
    print("Example 6: Session Management with Session IDs")
    print("=" * 80)
    
    # Initialize Auggie SDK
    print("\nInitializing Auggie SDK...")
    agent = Auggie(model="sonnet4.5")
    
    # ========================================================================
    # Demo 1: Without Session - No Memory
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 1: WITHOUT Session - Each call is independent (no memory)")
    print("=" * 80)
    
    print("\n📝 First call: Create a function")
    result1 = agent.run("Create a Python function called add_numbers that adds two numbers")
    print(result1)
    
    print("\n📝 Second call: Try to test it")
    result2 = agent.run("Now test the add_numbers function with 5 and 3")
    print(result2)
    print("\n❌ Notice: It doesn't remember the function from the first call!")
    
    # ========================================================================
    # Demo 2: With Session - Has Memory
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 2: WITH Session - Calls share context (has memory)")
    print("=" * 80)
    
    with agent.session() as session:
        print(f"\n🔑 Session ID: {session.session_id}")
        
        print("\n📝 First call: Create a function")
        result1 = session.run("Create a Python function called multiply_numbers that multiplies two numbers")
        print(result1)
        
        print("\n📝 Second call: Test it")
        result2 = session.run("Now test the multiply_numbers function with 4 and 7")
        print(result2)
        
        print("\n📝 Third call: Modify it")
        result3 = session.run("Add error handling to the multiply_numbers function")
        print(result3)
        
        print("\n✅ Notice: All calls remember the previous context!")
    
    # ========================================================================
    # Demo 3: Custom Session IDs - Work on Different Tasks
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 3: Custom Session IDs - Separate contexts for different tasks")
    print("=" * 80)
    
    # Backend work
    print("\n🔧 Working on backend...")
    with agent.session("backend-work") as backend:
        print(f"🔑 Backend Session ID: {backend.session_id}")
        backend.run("Create a simple REST API endpoint for user registration")
    
    # Frontend work
    print("\n🎨 Working on frontend...")
    with agent.session("frontend-work") as frontend:
        print(f"🔑 Frontend Session ID: {frontend.session_id}")
        frontend.run("Create a React component for a login form")
    
    # Resume backend work
    print("\n🔧 Resuming backend work...")
    with agent.session("backend-work") as backend:
        print(f"🔑 Backend Session ID: {backend.session_id}")
        result = backend.run("Add validation to the user registration endpoint")
        print(result)
        print("\n✅ Notice: It remembers the registration endpoint from before!")
    
    # ========================================================================
    # Demo 4: Session ID Property
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 4: Accessing Session ID Property")
    print("=" * 80)
    
    print(f"\n🔍 Session ID outside context: {agent.session_id}")
    print("   (Returns None when not in a session)")
    
    with agent.session() as session:
        print(f"\n🔍 Session ID inside context: {session.session_id}")
        print("   (Returns the actual session ID)")
    
    # ========================================================================
    # Demo 5: Practical Use Case - Multi-Step Code Generation
    # ========================================================================
    print("\n" + "=" * 80)
    print("Demo 5: Practical Use Case - Multi-Step Code Generation")
    print("=" * 80)
    
    with agent.session("code-generation") as session:
        print(f"\n🔑 Session ID: {session.session_id}")
        
        print("\n📝 Step 1: Create the main function")
        session.run("Create a Python function called calculate_fibonacci that returns the nth Fibonacci number")
        
        print("\n📝 Step 2: Add error handling")
        session.run("Add error handling for negative numbers and non-integers")
        
        print("\n📝 Step 3: Optimize it")
        session.run("Optimize the fibonacci function using memoization")
        
        print("\n📝 Step 4: Write tests")
        result = session.run("Write pytest tests for the calculate_fibonacci function")
        print(result)
        
        print("\n✅ All steps completed in one continuous session!")
    
    print("\n" + "=" * 80)
    print("✅ Session Management Demo Complete!")
    print("=" * 80)
    
    print("\n📚 Key Takeaways:")
    print("   1. Without session: Each run() call is independent")
    print("   2. With session: Calls share context and remember previous interactions")
    print("   3. Custom session IDs: Work on different tasks in parallel")
    print("   4. Session ID property: Access the current session ID")
    print("   5. Practical use: Multi-step tasks that build on each other")

if __name__ == "__main__":
    main()

