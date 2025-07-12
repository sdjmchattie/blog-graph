from typing import Any, Dict

from chains import writer_chain
from state import GraphState


class Writer:
    def __init__(self, output_file_name: str):
        self.output_file_name = output_file_name

    def writer(self, state: GraphState) -> Dict[str, Any]:
        request = state.get("request", "")
        knowledge = "\n".join(state.get("knowledge", []))
        previous_draft = state.get("post_content", "")
        user_feedback = state.get("user_feedback", "")

        post_content = writer_chain.invoke(
            {
                "request": request,
                "knowledge": knowledge,
                "previous_draft": previous_draft,
                "user_feedback": user_feedback,
            }
        )

        with open(self.output_file_name, "w") as file:
            file.write(post_content)

        return {"post_content": post_content}
