from auggie_sdk import Auggie

# Simple initialization - no cli_path needed!
# The SDK will auto-detect auggie from PATH
agent = Auggie(model="sonnet4.5")

# Run a task
result = agent.run("What is 2 + 2?", return_type=int)
print(f"Result: {result}")

# Note: You may see async cleanup warnings after this - they're harmless
# and will be fixed in a future SDK version. To hide them, run:
# python3 basicsdk.py 2>/dev/null

# option to add mcp in this sdk.