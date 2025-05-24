from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import END, StateGraph
from .nodes import researcher, web_search
from .state import GraphState

RESEARCHER = "researcher"
WEB_SEARCH = "web_search"

workflow = StateGraph(GraphState)
workflow.add_node(RESEARCHER, researcher)
workflow.set_entry_point(RESEARCHER)

workflow.add_edge(RESEARCHER, END)

app = workflow.compile()

def invoke(input: GraphState = None):
    """
    Invoke the graph with the given input state.

    Args:
        input (GraphState): The initial state of the graph.
    """
    input = input or GraphState(
        request="Using LazyGit to perform git operations",
    )

    return app.invoke(input=input)

def test_search():
    """
    Test the search functionality of the graph.
    """
    input = GraphState(
        request="Test search",
        search_queries=["xbox", "nintendo switch"],
        knowledge=[],
        post_content=""
    )

    result = web_search(input)
    print(result)
