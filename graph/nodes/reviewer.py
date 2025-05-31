from typing import Any, Dict

from graph.chains import reviewer_chain
from graph import GraphState


def reviewer(state: GraphState) -> Dict[str, Any]:
    review = reviewer_chain.invoke(
        {"post_content": state.get("post_content", "")}
    )

    return {"needs_redraft": not review.acceptable}
