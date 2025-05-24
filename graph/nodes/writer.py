from typing import Any, Dict

from graph.chains import writer_chain
from graph import GraphState


def writer(state: GraphState) -> Dict[str, Any]:
    request = state.get("request", "")
    knowledge = "\n".join(state.get("knowledge", []))
    previous_draft = state.get("post_content", "")

    post_content = writer_chain.invoke({ "request": request, "knowledge": knowledge, "previous_draft": previous_draft })
    return { "post_content": post_content }
