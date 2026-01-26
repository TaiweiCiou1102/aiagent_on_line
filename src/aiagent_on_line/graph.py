from langgraph.graph import StateGraph, START, END

from state import State
from ai import chatbot

# initialize the graph builder.
graph_builder = StateGraph(State)
# add nodes
graph_builder.add_node("chatbot", chatbot)
# build graph
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
# graph compile
graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream(
        {"messages":[{
            "role" : "user",
            "content" : user_input
        }]}):
        for value in event.values():
            return value['messages'][-1].content