from typing import Any
from langchain_tavily import TavilySearch

from state import GraphState


web_search_tool = TavilySearch(max_results=10)


def web_search(state: GraphState) -> dict[str, Any]:
    knowledge = state.get("knowledge", [])

    for query in state.get("search_queries", []):
        tavily_results = web_search_tool.invoke({"query": query})["results"]
        knowledge.extend([tavily_result["content"] for tavily_result in tavily_results])

    return {"search_queries": [], "knowledge": knowledge}
