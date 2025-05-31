from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import END, StateGraph
from .nodes import HumanInput, outliner, researcher, web_search, writer
from .state import GraphState

HUMAN_DRAFT_REVIEW = "human_draft_review"
HUMAN_OUTLINE_REVIEW = "human_outline_review"
OUTLINER = "outliner"
RESEARCHER = "researcher"
REVIEWER = "reviewer"
WEB_SEARCH = "web_search"
WRITER = "writer"


def human_wants_a_new_outline(state: GraphState) -> str:
    """Decide whether to change the post outline.

    Args:
        state (GraphState): The current state of the graph.

    Returns:
        str: The next action to take, either RESEARCHER or OUTLINER.
    """
    if len(state.get("user_feedback", "").strip()) > 0:
        print("User wants another outline: going back to outliner.")
        return OUTLINER
    else:
        print("User is happy with the outline, moving on to researcher.")
        return RESEARCHER

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
    HUMAN_DRAFT_REVIEW,
    HumanInput("What changes do you want to the post, if any? (leave empty if happy) ").get_input,
)
workflow.add_node(
    HUMAN_OUTLINE_REVIEW,
    HumanInput("What changes do you want to the outline, if any? (leave empty if happy) ").get_input,
)
workflow.add_node(OUTLINER, outliner)
workflow.add_node(RESEARCHER, researcher)
workflow.add_node(WEB_SEARCH, web_search)
workflow.add_node(WRITER, writer)

workflow.set_entry_point(OUTLINER)
workflow.add_edge(OUTLINER, HUMAN_OUTLINE_REVIEW)
workflow.add_conditional_edges(HUMAN_OUTLINE_REVIEW, human_wants_a_new_outline)
workflow.add_edge(RESEARCHER, WEB_SEARCH)
workflow.add_edge(WEB_SEARCH, WRITER)
workflow.add_edge(WRITER, HUMAN_DRAFT_REVIEW)
workflow.add_conditional_edges(HUMAN_DRAFT_REVIEW, human_wants_another_draft)

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
