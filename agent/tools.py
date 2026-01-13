"""
Augment SDK tool wrapper for LangGraph integration.
"""

from typing import Optional
from auggie_sdk import Auggie


class AugmentTool:
    """
    Wrapper around Augment SDK for use in LangGraph workflows.

    Provides methods to interact with Augment SDK while managing
    sessions and error handling.
    """

    def __init__(self, model: str = "sonnet4.5"):
        """
        Initialize the Augment tool.

        Args:
            model: Model to use (default: sonnet4.5)
        """
        self.sdk = Auggie(model=model)
        self._session_context = None
        self._session_instance = None

    def run_task(
        self,
        task: str,
        timeout: int = 300
    ) -> str:
        """
        Run a task using Augment SDK with session for conversation continuity.

        Args:
            task: Task description/prompt
            timeout: Timeout in seconds

        Returns:
            Result from Augment SDK
        """
        try:
            # Use session for conversation continuity
            if self._session_context is None:
                # Create the context manager
                self._session_context = self.sdk.session()
                # Enter the context and get the session instance (which is self.sdk)
                self._session_instance = self._session_context.__enter__()

            # Run the task using the session instance
            result = self._session_instance.run(task, timeout=timeout)

            return result
        except Exception as e:
            return f"Error executing task: {str(e)}"

    def end_session(self):
        """End the current session if one exists."""
        if self._session_context is not None:
            try:
                self._session_context.__exit__(None, None, None)
            except:
                pass
            finally:
                self._session_context = None
                self._session_instance = None

    def get_session_id(self) -> Optional[str]:
        """Get the current session ID."""
        if self._session_instance is not None:
            return self._session_instance.session_id
        return None


# Specialized Augment operations
class AugmentGitHubOps:
    """GitHub-specific operations using Augment SDK."""
    
    def __init__(self, augment_tool: AugmentTool):
        self.tool = augment_tool
    
    def get_pr_details(self, repo: str, pr_number: int, timeout: int = 120) -> str:
        """Get PR details from GitHub."""
        task = f"""
        Get details for pull request #{pr_number} in repository {repo}.
        Include: title, description, status, files changed, and review status.
        Keep response concise (under 500 words).
        """
        return self.tool.run_task(task, timeout=timeout)

    def review_pr(self, repo: str, pr_number: int, timeout: int = 300) -> str:
        """Perform code review on a PR."""
        task = f"""
        Review pull request #{pr_number} in repository {repo}.
        Analyze code quality, security, and performance issues.
        Provide specific recommendations.
        """
        return self.tool.run_task(task, timeout=timeout)

    def analyze_error_log(self, repo: str, error_log: str, timeout: int = 300) -> str:
        """Analyze error log and find root cause."""
        task = f"""
        Analyze this error log from repository {repo}:

        ```
        {error_log}
        ```

        Identify:
        1. Main error
        2. Failing endpoints/functions
        3. Root cause

        Keep response under 500 words.
        """
        return self.tool.run_task(task, timeout=timeout)

    def find_bug_location(self, repo: str, error_analysis: str, timeout: int = 300) -> str:
        """Find the code location causing the bug."""
        task = f"""
        Based on this error analysis:
        {error_analysis}

        Search repository {repo} and find:
        1. Exact file and line number
        2. Code snippet causing the issue
        3. Suggested fix

        Be specific and concise.
        """
        return self.tool.run_task(task, timeout=timeout)

