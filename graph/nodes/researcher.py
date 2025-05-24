from typing import Any, Dict

from graph.chains import research_chain
from graph import GraphState


def researcher(state: GraphState) -> Dict[str, Any]:
    request = state.get("request", "")
    knowledge = "\n".join(state.get("knowledge", []))

    research = research_chain.invoke({ "request": request, "knowledge": knowledge })
    return { "search_queries": research.search_queries }
