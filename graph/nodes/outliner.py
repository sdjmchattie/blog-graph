from typing import Any

from graph.chains import outline_chain
from graph import GraphState

def outliner(state: GraphState) -> dict[str, Any]:
    outline = state.get("outline", "")
    request = state.get("request", "")
    user_feedback = state.get("user_feedback", "")

    outline = outline_chain.invoke(
        {
            "outline": outline,
            "request": request,
            "user_feedback": user_feedback,
        }
    )

    print()
    print(outline)
    print()

    return {"outline": outline, "user_feedback": ""}
