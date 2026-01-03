from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import classify_intent_node, retrieve_node, generate_answer_node

def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("classify", classify_intent_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_answer_node)

    # Define Edges
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()

# Global app instance
app_agent = create_graph()