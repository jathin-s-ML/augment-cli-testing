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


def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze the user request and determine the task type.
    
    This node examines the task and classifies it to route to
    the appropriate workflow.
    """
    task = state["task"]
    
    # Simple task classification
    task_lower = task.lower()
    
    if "review" in task_lower and ("pr" in task_lower or "pull request" in task_lower):
        task_type = "code_review"
    elif "error" in task_lower or "bug" in task_lower or "debug" in task_lower:
        task_type = "error_analysis"
    elif "list" in task_lower and "repo" in task_lower:
        task_type = "list_repos"
    else:
        task_type = "general_query"
    
    return {
        "task_type": task_type,
        "messages": [AIMessage(content=f"Task classified as: {task_type}")]
    }


def augment_executor_node(state: AgentState) -> Dict[str, Any]:
    """
    Execute the task using Augment SDK with session for conversation continuity.

    This node calls the appropriate Augment SDK method based on
    the task type.
    """
    task = state["task"]
    task_type = state.get("task_type", "general_query")

    # Execute all tasks with session (always enabled)
    if task_type == "general_query" or task_type == "list_repos":
        result = augment_tool.run_task(task, timeout=180)
    else:
        # For complex tasks, use longer timeout
        result = augment_tool.run_task(task, timeout=300)

    session_id = augment_tool.get_session_id()

    return {
        "augment_result": result,
        "session_id": session_id,
        "messages": [AIMessage(content=f"Augment SDK executed task")]
    }


def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze the Augment SDK result.

    This node processes the raw result from Augment and extracts
    key information, adding context and structure.
    """
    augment_result = state.get("augment_result", "")
    task_type = state.get("task_type", "general_query")

    # Process the result based on task type
    if task_type == "code_review":
        # For code reviews, add structured analysis
        analysis = f"""## Code Review Analysis

{augment_result}

### Summary
The code review has been completed using Augment SDK. Please review the findings above and address any issues identified.
"""
    elif task_type == "error_analysis":
        # For error analysis, add debugging context
        analysis = f"""## Error Analysis Report

{augment_result}

### Next Steps
1. Review the root cause identified above
2. Check the suggested fixes
3. Test the solution in a development environment
"""
    elif task_type == "list_repos":
        # For repo listings, add metadata
        try:
            # Try to count repos if result is a list
            import ast
            result_data = ast.literal_eval(str(augment_result))
            if isinstance(result_data, list):
                repo_count = len(result_data)
                analysis = f"""## Repository Listing

Found {repo_count} repositories:

{augment_result}
"""
            else:
                analysis = augment_result
        except:
            # If parsing fails, use raw result
            analysis = augment_result
    else:
        # For general queries, pass through with minimal processing
        analysis = augment_result

    return {
        "analysis": analysis,
        "messages": [AIMessage(content="Analysis complete")]
    }


def formatter_node(state: AgentState) -> Dict[str, Any]:
    """
    Format the final output for the user.

    This node takes the analysis and formats it into a user-friendly
    response with proper formatting and metadata.
    """
    analysis = state.get("analysis", "")
    task_type = state.get("task_type", "general_query")

    # Add final formatting and metadata footer
    if task_type in ["code_review", "error_analysis"]:
        final_output = f"""{analysis}

---
*Generated using Augment SDK via LangGraph Agent*
*Task Type: {task_type}*
"""
    else:
        # For simple queries, just use the analysis as-is
        final_output = analysis

    return {
        "final_output": final_output,
        "messages": [AIMessage(content=final_output)]
    }


def cleanup_node(state: AgentState) -> Dict[str, Any]:
    """
    Cleanup resources (e.g., end Augment session).
    """
    augment_tool.end_session()
    
    return {
        "messages": [AIMessage(content="Session cleaned up")]
    }

