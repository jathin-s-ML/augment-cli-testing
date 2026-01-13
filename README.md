# LangGraph Agent with Augment SDK

A LangGraph-based agent that integrates with Augment SDK to perform GitHub operations, code reviews, and error analysis with session-based conversation continuity and intelligent result detection.

## 🏗️ Architecture

The agent uses a **simplified 3-node workflow** with smart auto-detection:

```
User Input
    ↓
┌─────────────────────────────────┐
│   Augment Executor Node         │  ← Executes via Augment SDK
│   (task → augment_result)       │     • Creates/maintains session
│                                 │     • Passes task to Augment SDK
│                                 │     • Returns raw result
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Analyzer Node                 │  ← Auto-detects & formats
│   (augment_result →             │     • Inspects data structure
│    final_output)                │     • Detects: PRs, repos, reviews, errors
│                                 │     • Adds appropriate headers
│                                 │     • Formats with metadata
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Cleanup Node                  │  ← Ends session
│   (session cleanup)             │     • Releases resources
│                                 │     • Ends Augment SDK session
└────────────┬────────────────────┘
             ↓
        Final Output
```

**Data Flow:**
```
task → augment_result → final_output (auto-detected type)
```

**Key Features:**
- ✅ **No manual classification** - Augment SDK understands intent
- ✅ **Smart detection** - Analyzer inspects data structure to determine type
- ✅ **Session-based** - All tasks use sessions for context continuity
- ✅ **3 nodes only** - Simplified from 5 nodes

## 🎯 Features

- **LangGraph Workflow**: Simplified 3-node agent workflow
- **Augment SDK Integration**: Seamless integration with Augment SDK
- **Session Management**: Maintains conversation context across ALL queries
- **Smart Auto-Detection**: Automatically detects result type by inspecting data structure
  - Pull Requests: Detects `number`, `head_branch`, `state` fields
  - Repositories: Detects `name`, `owner`, `permissions` fields
  - Code Reviews: Detects review-related keywords
  - Error Analysis: Detects error/exception keywords
- **Structured Output**: Formatted results with appropriate headers and metadata
- **Error Handling**: Robust error handling with safe fallbacks

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
## Pull Requests

Found 1 pull request(s):

[{'number': 1, 'title': 'basic sdk', 'state': 'open', 'author': 'jathin-s-ML', ...}]

---
*Generated using Augment SDK via LangGraph Agent*
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

See all 3 nodes in action with detailed state tracking:

```bash
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx python examples/04_node_workflow_demo.py 2>/dev/null
```

This example shows:
- Initial state
- State changes at each node (executor → analyzer → cleanup)
- Data flow through the pipeline
- Auto-detection of result types
- Session management
- Final result with metadata

## 📚 Components

### State (`agent/state.py`)
Defines the agent state schema with the following fields:
- `messages`: Conversation history (accumulated)
- `task`: Current task description
- `augment_result`: Raw result from Augment SDK
- `final_output`: Final formatted output (auto-detected type)
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

#### 1. `augment_executor_node`
- **Input:** `task`
- **Output:** `augment_result`, `session_id`
- **Function:** Executes task via Augment SDK with session (always enabled)
- **Note:** No task classification needed - Augment SDK understands intent

#### 2. `analyzer_node`
- **Input:** `augment_result`
- **Output:** `final_output`
- **Function:** Auto-detects result type and formats output:
  - **Pull Requests**: Detects `number` + `head_branch` fields → "## Pull Requests" header
  - **Repositories**: Detects `name` + `owner` + `permissions` fields → "## Repositories" header
  - **Code Review**: Detects review keywords → "## Code Review Analysis" header
  - **Error Analysis**: Detects error keywords → "## Error Analysis Report" header
  - **General**: Unknown type → passes through as-is
- **Note:** Combines analysis + formatting in one step

#### 3. `cleanup_node`
- **Input:** `session_id`
- **Output:** None
- **Function:** Ends Augment SDK session and releases resources

### Graph (`agent/graph.py`)
- Defines the LangGraph workflow
- Connects nodes in sequence: **executor → analyzer → cleanup** (3 nodes)
- Manages state transitions between nodes

## 🎯 Features

### ✅ Implemented
- **LangGraph state management**: Full state tracking across all nodes
- **Augment SDK integration**: Seamless integration with session support
- **Session continuity**: All tasks use sessions for conversation context
- **Smart auto-detection**: Automatically detects result type from data structure (no manual classification)
- **Result processing**: Analyzer node auto-detects type and enriches results
- **Structured output**: Formatted output with auto-detected headers and metadata
- **Error handling**: Graceful error handling with safe fallbacks
- **Resource cleanup**: Automatic session cleanup
- **Simplified workflow**: 3 nodes instead of 5 (removed planner and formatter)

### ⏳ Coming Soon
- Conditional routing based on task complexity
- Parallel execution for independent tasks
- Human-in-the-loop for approval workflows
- Streaming responses for long-running tasks

## Data Flow Example

Here's how data flows through the simplified 3-node system:

### Example 1: List Pull Requests

```python
# 1. Initial State
{
    "task": "List all the open prs in augment-cli-testing repo",
    "augment_result": None,
    "final_output": None,
    "session_id": None
}

# 2. After Augment Executor Node
{
    "augment_result": "[{'number': 1, 'title': 'basic sdk', 'state': 'open', 'head_branch': 'dev', ...}]",
    "session_id": "abc-123-def"  # ← Session created
}

# 3. After Analyzer Node (auto-detects PRs from 'number' + 'head_branch' fields)
{
    "final_output": """## Pull Requests

Found 1 pull request(s):

[{'number': 1, 'title': 'basic sdk', ...}]

---
*Generated using Augment SDK via LangGraph Agent*
"""
}

# 4. After Cleanup Node
# Session ended, resources cleaned up
```

### Example 2: List Repositories

```python
# 1. Initial State
{
    "task": "List my GitHub repositories",
    "augment_result": None,
    "final_output": None,
    "session_id": None
}

# 2. After Augment Executor Node
{
    "augment_result": "[{'name': 'repo1', 'owner': 'user', 'permissions': {...}, ...}]",
    "session_id": "xyz-456-abc"
}

# 3. After Analyzer Node (auto-detects repos from 'name' + 'owner' + 'permissions' fields)
{
    "final_output": """## Repositories

Found 19 repository(ies):

[{'name': 'repo1', 'owner': 'user', ...}]

---
*Generated using Augment SDK via LangGraph Agent*
"""
}

# 4. After Cleanup Node
# Session ended
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

