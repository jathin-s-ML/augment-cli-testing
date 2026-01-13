# LangGraph Agent with Augment SDK

A LangGraph-based agent that integrates with Augment SDK to perform GitHub operations, code reviews, and error analysis with session-based conversation continuity.

## 🏗️ Architecture

The agent uses a 5-node workflow with proper data flow:

```
User Input
    ↓
┌─────────────────────────┐
│    Planner Node         │  ← Classifies task type
│  (task → task_type)     │     (list_repos, code_review, error_analysis, general_query)
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│  Augment Executor Node  │  ← Executes via Augment SDK with session
│  (task → augment_result)│     Creates/maintains session for continuity
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│    Analyzer Node        │  ← Processes and enriches results
│  (augment_result →      │     • list_repos: Counts repos, adds metadata
│   analysis)             │     • code_review: Adds structured headers
│                         │     • error_analysis: Adds next steps
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│   Formatter Node        │  ← Formats final output
│  (analysis →            │     Adds metadata footer for complex tasks
│   final_output)         │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│    Cleanup Node         │  ← Ends Augment SDK session
│  (session cleanup)      │     Releases resources
└───────────┬─────────────┘
            ↓
       Final Output
```

**Data Flow:**
```
task → task_type → augment_result → analysis → final_output
```

## 📦 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Augment SDK

Follow the setup from `../github-auggie-sdk/README.md`:

```bash
# Install Auggie CLI
npm install -g @augmentcode/auggie@prerelease

# Login
auggie login

# Configure GitHub MCP
auggie mcp add github \
  --transport stdio \
  --command "docker" \
  --args "run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN mcp/github"
```

### 3. Set Environment Variables

Create a `.env` file:

```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your_token_here
```

## 🚀 Usage

### Example 1: Simple Query

List GitHub repositories with read-only access:

```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx python examples/01_simple_query.py 2>/dev/null
```

**Output:**
```
## Repository Listing

Found 1 repositories:

[{'name': 'fault-injector', 'owner': 'maplelabs', ...}]
```

### Example 2: Code Review (Coming Soon)

```bash
python examples/02_code_review.py owner/repo 123
```

### Example 3: Error Analysis (Coming Soon)

```bash
python examples/03_error_analysis.py owner/repo error.log
```

### Example 4: Complete Node Workflow Demo

See all 5 nodes in action with detailed state tracking:

```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx python examples/04_node_workflow_demo.py 2>/dev/null
```

This example shows:
- Initial state
- State changes at each node
- Data flow through the pipeline
- Session management
- Final result with metadata

## 📚 Components

### State (`agent/state.py`)
Defines the agent state schema with the following fields:
- `messages`: Conversation history (accumulated)
- `task`: Current task description
- `task_type`: Classified task type (list_repos, code_review, error_analysis, general_query)
- `augment_result`: Raw result from Augment SDK
- `analysis`: Processed and enriched result from analyzer
- `final_output`: Final formatted output for user
- `session_id`: Augment SDK session ID for conversation continuity
- `metadata`: Additional context

### Tools (`agent/tools.py`)

#### `AugmentTool`
Wrapper around Augment SDK with session management:
- `run_task(task, timeout)`: Executes task with automatic session creation
- `get_session_id()`: Returns current session ID
- `end_session()`: Cleans up session resources

**Note:** Sessions are **always enabled** for all tasks to maintain conversation continuity.

#### `AugmentGitHubOps`
GitHub-specific operations using Augment SDK:
- `get_pr_details(repo, pr_number)`: Get PR details
- `review_pr(repo, pr_number)`: Perform code review
- `analyze_error_log(repo, error_log)`: Analyze error logs
- `find_bug_location(repo, error_analysis)`: Find bug location in code

### Nodes (`agent/nodes.py`)

#### 1. `planner_node`
- **Input:** `task`
- **Output:** `task_type`
- **Function:** Classifies task into: list_repos, code_review, error_analysis, or general_query

#### 2. `augment_executor_node`
- **Input:** `task`, `task_type`
- **Output:** `augment_result`, `session_id`
- **Function:** Executes task via Augment SDK with session (always enabled)

#### 3. `analyzer_node`
- **Input:** `augment_result`, `task_type`
- **Output:** `analysis`
- **Function:** Processes and enriches results:
  - `list_repos`: Counts repositories and adds metadata header
  - `code_review`: Adds "Code Review Analysis" header + summary
  - `error_analysis`: Adds "Error Analysis Report" header + next steps
  - `general_query`: Passes through as-is

#### 4. `formatter_node`
- **Input:** `analysis`, `task_type`
- **Output:** `final_output`
- **Function:** Formats final output with metadata footer for complex tasks

#### 5. `cleanup_node`
- **Input:** `session_id`
- **Output:** None
- **Function:** Ends Augment SDK session and releases resources

### Graph (`agent/graph.py`)
- Defines the LangGraph workflow
- Connects nodes in sequence: planner → executor → analyzer → formatter → cleanup
- Manages state transitions between nodes

## 🎯 Features

### ✅ Implemented
- **LangGraph state management**: Full state tracking across all nodes
- **Augment SDK integration**: Seamless integration with session support
- **Session continuity**: All tasks use sessions for conversation context
- **Task classification**: Automatic routing based on task type
- **Result processing**: Analyzer node enriches results with context
- **Structured output**: Formatted output with headers and metadata
- **Error handling**: Graceful error handling in all nodes
- **Resource cleanup**: Automatic session cleanup

### ⏳ Coming Soon
- Conditional routing based on task complexity
- Parallel execution for independent tasks
- Human-in-the-loop for approval workflows
- Streaming responses for long-running tasks

## Data Flow Example

Here's how data flows through the system for a "list repos" task:

```python
# 1. Initial State
{
    "task": "List my GitHub repositories",
    "task_type": None,
    "augment_result": None,
    "analysis": None,
    "final_output": None,
    "session_id": None
}

# 2. After Planner Node
{
    "task_type": "list_repos"  # ← Classified
}

# 3. After Augment Executor Node
{
    "augment_result": "[{'name': 'repo1', 'stars': 10}, ...]",  # ← Raw result
    "session_id": "abc-123-def"  # ← Session created
}

# 4. After Analyzer Node
{
    "analysis": """## Repository Listing

Found 2 repositories:

[{'name': 'repo1', 'stars': 10}, ...]"""  # ← Enriched with metadata
}

# 5. After Formatter Node
{
    "final_output": """## Repository Listing

Found 2 repositories:

[{'name': 'repo1', 'stars': 10}, ...]"""  # ← Final formatted output
}

# 6. After Cleanup Node
# Session ended, resources released
```

## 🔐 Session Management

The agent **always uses sessions** for all tasks to maintain conversation continuity:

- **Session Creation**: Automatically created on first `run_task()` call
- **Session Reuse**: Same session used for multiple calls within workflow
- **Session Cleanup**: Automatically cleaned up by `cleanup_node`
- **Session ID Tracking**: Stored in state for debugging and monitoring

**Benefits:**
- Conversation context maintained across multiple queries
- Better results from Augment SDK with context awareness
- Ability to ask follow-up questions in future enhancements

## Learn More

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Augment SDK Guide](../github-auggie-sdk/README.md)
- [Examples](./examples/)

## 🤝 Contributing

Contributions welcome! Please see the main project README.

## 📄 License

MIT

