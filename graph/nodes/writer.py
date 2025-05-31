from typing import Any, Dict

from graph.chains import writer_chain
from graph import GraphState


def writer(state: GraphState) -> Dict[str, Any]:
    request = state.get("request", "")
    knowledge = "\n".join(state.get("knowledge", []))
    outline = state.get("outline", "")
    previous_draft = state.get("post_content", "")
    user_feedback = state.get("user_feedback", "")

    post_content = writer_chain.invoke(
        {
            "request": request,
            "knowledge": knowledge,
            "outline": outline,
            "previous_draft": previous_draft,
            "user_feedback": user_feedback,
        }
    )

    with open("output/blog_post.md", "w") as file:
        file.write(post_content)

    return {"post_content": post_content}
