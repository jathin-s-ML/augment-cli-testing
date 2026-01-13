"""
Node functions for the LangGraph agent.
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from .state import AgentState
from .tools import AugmentTool, AugmentGitHubOps


# Initialize tools
augment_tool = AugmentTool()
github_ops = AugmentGitHubOps(augment_tool)


# Planner node removed - Augment SDK handles task understanding

def augment_executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute the task using Augment SDK with session for conversation continuity.

    Augment SDK is smart enough to understand the intent and return
    appropriate results without explicit task classification.
    """
    task = state["task"]

    # Execute task with session (always enabled)
    # Use standard timeout for all tasks
    result = augment_tool.run_task(task, timeout=180)

    session_id = augment_tool.get_session_id()

    return {
        "augment_result": result,
        "session_id": session_id,
        "messages": [AIMessage(content=f"Augment SDK executed task")]
    }


def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze and format the Augment SDK result.

    This node auto-detects the result type by inspecting the data structure,
    then formats it appropriately with headers and metadata.
    Combines analysis and formatting in one step.
    """
    augment_result = state.get("augment_result", "")

    # Convert dict/object results to string for processing
    if isinstance(augment_result, dict):
        import json
        augment_result = json.dumps(augment_result, indent=2)
    elif not isinstance(augment_result, str):
        augment_result = str(augment_result)

    # Auto-detect the result type by inspecting the data
    result_type = _detect_result_type(augment_result)

    # Format based on detected type (includes final formatting)
    if result_type == "pull_requests":
        final_output = _format_pull_requests(augment_result)
    elif result_type == "repositories":
        final_output = _format_repositories(augment_result)
    elif result_type == "code_review":
        final_output = _format_code_review(augment_result)
    elif result_type == "error_analysis":
        final_output = _format_error_analysis(augment_result)
    else:
        # Unknown type - just pass through
        final_output = augment_result

    # Ensure final_output is a string for AIMessage
    if not isinstance(final_output, str):
        import json
        final_output = json.dumps(final_output, indent=2) if isinstance(final_output, dict) else str(final_output)

    return {
        "final_output": final_output,
        "messages": [AIMessage(content=final_output)]
    }


def _detect_result_type(result: str) -> str:
    """
    Auto-detect what type of data the result contains by inspecting structure.
    """
    try:
        import ast
        data = ast.literal_eval(str(result))

        # Check if it's a list
        if isinstance(data, list) and len(data) > 0:
            first_item = data[0]

            # Check for PR indicators
            if isinstance(first_item, dict):
                # PR has: number, head_branch, base_branch, state
                if 'number' in first_item and ('head_branch' in first_item or 'state' in first_item):
                    return "pull_requests"
                # Repository has: name, owner/full_name, permissions
                elif 'name' in first_item and ('permissions' in first_item or 'owner' in first_item or 'full_name' in first_item):
                    return "repositories"

        # Check for code review keywords in text
        result_lower = str(result).lower()
        if any(word in result_lower for word in ['code quality', 'issues found', 'recommendations', 'security']):
            return "code_review"

        # Check for error analysis keywords
        if any(word in result_lower for word in ['error', 'exception', 'stack trace', 'root cause', 'traceback']):
            return "error_analysis"

    except:
        pass

    return "general"


def _format_pull_requests(result: str) -> str:
    """Format pull request data with header and metadata."""
    try:
        import ast
        data = ast.literal_eval(str(result))
        count = len(data) if isinstance(data, list) else 1

        return f"""## Pull Requests

Found {count} pull request(s):

{result}

---
*Generated using Augment SDK via LangGraph Agent*
"""
    except:
        return result


def _format_repositories(result: str) -> str:
    """Format repository data with header and metadata."""
    try:
        import ast
        data = ast.literal_eval(str(result))
        count = len(data) if isinstance(data, list) else 1

        return f"""## Repositories

Found {count} repository(ies):

{result}

---
*Generated using Augment SDK via LangGraph Agent*
"""
    except:
        return result


def _format_code_review(result: str) -> str:
    """Format code review results with structured headers."""
    return f"""## Code Review Analysis

{result}

### Summary
The code review has been completed using Augment SDK. Please review the findings above and address any issues identified.

---
*Generated using Augment SDK via LangGraph Agent*
"""


def _format_error_analysis(result: str) -> str:
    """Format error analysis results with next steps."""
    return f"""## Error Analysis Report

{result}

### Next Steps
1. Review the root cause identified above
2. Check the suggested fixes
3. Test the solution in a development environment

---
*Generated using Augment SDK via LangGraph Agent*
"""


# Formatter node removed - merged into analyzer_node


def cleanup_node(state: AgentState) -> Dict[str, Any]:
    """
    Cleanup resources (e.g., end Augment session).
    """
    session_id = state.get("session_id")
    augment_tool.end_session()

    return {
        "messages": [AIMessage(content=f"Session {session_id} cleaned up")]
    }

