from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import END, StateGraph
from .nodes import researcher, web_search
from .state import GraphState

RESEARCHER = "researcher"
WEB_SEARCH = "web_search"

def search_or_write(state: GraphState) -> str:
    """Decide whether to search for more knowledge, or write the blog post.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        str: The next action to take, either WEB_SEARCH or END.
    """
    print(state)
    print(len(state.get("knowledge", [])))
    if len(state.get("search_queries", [])) > 0 and len(state.get("knowledge", [])) < 30:
        return WEB_SEARCH
    else:
        return END

workflow = StateGraph(GraphState)
workflow.add_node(RESEARCHER, researcher)
workflow.add_node(WEB_SEARCH, web_search)

workflow.set_entry_point(RESEARCHER)
workflow.add_conditional_edges(
    RESEARCHER,
    search_or_write
)
workflow.add_edge(WEB_SEARCH, RESEARCHER)

app = workflow.compile()

def invoke(initial_state: GraphState = None):
    """
    Invoke the graph with the given input state.

    Args:
        input (GraphState): The initial state of the graph.
    """
    if not initial_state:
        initial_state = GraphState(
            request = "Using LazyGit to manage repositories" # input("Enter the blog topic: "),
        )

    return app.invoke(input = initial_state)

def test_search():
    """
    Test the search functionality of the graph.
    """
    input = GraphState(
        request = "Test search",
        search_queries = ["xbox", "nintendo switch"],
        knowledge = [],
        post_content = ""
    )

    result = web_search(input)
    print(result)
