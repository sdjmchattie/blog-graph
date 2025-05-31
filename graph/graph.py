from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import END, StateGraph
from .nodes import HumanInput, researcher, reviewer, web_search, writer
from .state import GraphState

HUMAN_REVIEW = "human_review"
RESEARCHER = "researcher"
REVIEWER = "reviewer"
WEB_SEARCH = "web_search"
WRITER = "writer"


def human_wants_another_draft(state: GraphState) -> str:
    """Decide whether to do further drafts or to finish.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        str: The next action to take, either RESEARCHER or END.
    """
    if len(state.get("user_feedback", "").strip()) > 0:
        print("User wants another draft, going back to researcher.")
        return RESEARCHER
    else:
        print("User is happy with the draft, finishing.")
        return END


workflow = StateGraph(GraphState)
workflow.add_node(
    HUMAN_REVIEW,
    HumanInput("What changes do you want, if any? (leave empty if happy)").get_input,
)
workflow.add_node(RESEARCHER, researcher)
workflow.add_node(WEB_SEARCH, web_search)
workflow.add_node(WRITER, writer)

workflow.set_entry_point(RESEARCHER)
workflow.add_edge(RESEARCHER, WEB_SEARCH)
workflow.add_edge(WEB_SEARCH, WRITER)
workflow.add_edge(WRITER, HUMAN_REVIEW)
workflow.add_conditional_edges(HUMAN_REVIEW, human_wants_another_draft)

app = workflow.compile()


def invoke(initial_state: GraphState = None):
    """
    Invoke the graph with the given input state.

    Args:
        input (GraphState): The initial state of the graph.
    """
    if not initial_state:
        initial_state = GraphState.create(
            request=input("Enter the blog topic: "),
        )

    return app.invoke(input=initial_state)


def test_search():
    """
    Test the search functionality of the graph.
    """
    input = GraphState.create(
        request="Test search",
        search_queries=["xbox", "nintendo switch"],
        knowledge=[],
        post_content="",
    )

    result = web_search(input)
    print(result)
