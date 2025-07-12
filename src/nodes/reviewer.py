from typing import Any, Dict

from chains import reviewer_chain
from state import GraphState


def reviewer(state: GraphState) -> Dict[str, Any]:
    review = reviewer_chain.invoke({"post_content": state.get("post_content", "")})

    return {"needs_redraft": not review.acceptable}
