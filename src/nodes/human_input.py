from typing import Any
from state import GraphState


class HumanInput:
    def __init__(self, question: str):
        self.question = question

    def get_input(self, _state: GraphState) -> dict[str, Any]:
        """Get input from the user."""
        human_input = input(self.question.strip() + " ")

        return {"user_feedback": human_input}
