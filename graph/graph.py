from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import END, StateGraph
from .nodes import researcher, reviewer, web_search, writer
from .state import GraphState

RESEARCHER = "researcher"
REVIEWER = "reviewer"
WEB_SEARCH = "web_search"
WRITER = "writer"

def check_draft_quality(state: GraphState) -> str:
    """Decide whether to do more research or to output the post.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        str: The next action to take, either RESEARCHER or END.
    """
    if state.get("needs_redraft", False):
        print("Post needs redrafting, going back to researcher.")
        return RESEARCHER
    else:
        return END

workflow = StateGraph(GraphState)
workflow.add_node(RESEARCHER, researcher)
workflow.add_node(REVIEWER, reviewer)
workflow.add_node(WEB_SEARCH, web_search)
workflow.add_node(WRITER, writer)

workflow.set_entry_point(RESEARCHER)
workflow.add_edge(RESEARCHER, WEB_SEARCH)
workflow.add_edge(WEB_SEARCH, WRITER)
workflow.add_edge(WRITER, REVIEWER)
workflow.add_conditional_edges(
    REVIEWER,
    check_draft_quality
)

app = workflow.compile()

def invoke(initial_state: GraphState = None):
    """
    Invoke the graph with the given input state.

    Args:
        input (GraphState): The initial state of the graph.
    """
    if not initial_state:
        initial_state = GraphState(
            request = input("Enter the blog topic: "),
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
