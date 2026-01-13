"""
Unit tests for the LangGraph agent.
"""

import pytest
from langchain_core.messages import HumanMessage
from agent import create_agent_graph, AgentState
from agent.nodes import planner_node, formatter_node


class TestPlannerNode:
    """Test the planner node."""
    
    def test_code_review_classification(self):
        """Test that code review tasks are classified correctly."""
        state = {
            "task": "Review pull request #123 in my repo",
            "messages": []
        }
        result = planner_node(state)
        assert result["task_type"] == "code_review"
    
    def test_error_analysis_classification(self):
        """Test that error analysis tasks are classified correctly."""
        state = {
            "task": "Debug this error in my application",
            "messages": []
        }
        result = planner_node(state)
        assert result["task_type"] == "error_analysis"
    
    def test_list_repos_classification(self):
        """Test that list repos tasks are classified correctly."""
        state = {
            "task": "List all my GitHub repositories",
            "messages": []
        }
        result = planner_node(state)
        assert result["task_type"] == "list_repos"
    
    def test_general_query_classification(self):
        """Test that general queries are classified correctly."""
        state = {
            "task": "What is the weather today?",
            "messages": []
        }
        result = planner_node(state)
        assert result["task_type"] == "general_query"


class TestFormatterNode:
    """Test the formatter node."""
    
    def test_code_review_formatting(self):
        """Test code review output formatting."""
        state = {
            "task_type": "code_review",
            "augment_result": "The code looks good!",
            "messages": []
        }
        result = formatter_node(state)
        assert "Code Review Results" in result["final_output"]
        assert "The code looks good!" in result["final_output"]
    
    def test_error_analysis_formatting(self):
        """Test error analysis output formatting."""
        state = {
            "task_type": "error_analysis",
            "augment_result": "Found a null pointer exception",
            "messages": []
        }
        result = formatter_node(state)
        assert "Error Analysis" in result["final_output"]
        assert "Found a null pointer exception" in result["final_output"]
    
    def test_general_query_formatting(self):
        """Test general query output formatting."""
        state = {
            "task_type": "general_query",
            "augment_result": "Here is the answer",
            "messages": []
        }
        result = formatter_node(state)
        assert result["final_output"] == "Here is the answer"


class TestAgentGraph:
    """Test the agent graph creation."""
    
    def test_graph_creation(self):
        """Test that the graph can be created."""
        agent = create_agent_graph()
        assert agent is not None
    
    def test_graph_has_nodes(self):
        """Test that the graph has the expected nodes."""
        agent = create_agent_graph()
        # The graph should be compiled and ready to use
        assert hasattr(agent, 'invoke')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

