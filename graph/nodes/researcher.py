from typing import Any, Dict

from graph.chains import research_chain
from graph import GraphState


def researcher(state: GraphState) -> Dict[str, Any]:
    request = state.get("request", "")
    knowledge = "\n".join(state.get("knowledge", []))
    blog_draft = state.get("post_content", "")

    research = research_chain.invoke({ "request": request, "knowledge": knowledge, "blog_draft": blog_draft })
    return { "search_queries": research.search_queries }
