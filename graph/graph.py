from langgraph.graph import END, StateGraph
from .state import GraphState

workflow = StateGraph(GraphState)
workflow.set_entry_point(END)

app = workflow.compile()
