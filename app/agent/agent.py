from langgraph.graph import StateGraph, START, END
from app.agent.edges.retrieve_edge import retrieval_transition
from app.agent.edges.response_edge import response_transition
from app.agent.nodes.retrieve_node import RetrieveNode
from app.agent.nodes.response_node import ResponseNode
from app.agent.nodes.rewriting_node import RewritingNode
from app.agent.nodes.fallback_node import FallbackNode
from app.agent.enum import AgentStateType


class Agent:

    def __init__(self):
        self.graph = StateGraph(AgentStateType)
        self.initialize_nodes()
        self.compiled_graph = self.compile_graph()

    def initialize_nodes(self):
        self.graph.add_node("retrieve", RetrieveNode())
        self.graph.add_node("response", ResponseNode())
        self.graph.add_node("rewriting", RewritingNode())
        self.graph.add_node("end", FallbackNode())

        self.graph.add_edge(START, "retrieve")
        self.graph.add_conditional_edges(
            "retrieve",
            retrieval_transition,
            {
                "response": "response",
                "end": "end",
            },
        )

        self.graph.add_conditional_edges(
            "response",
            response_transition,
            {
                "rewriting": "rewriting",
                "fallback": "end",
                "end": END,
            },
        )

        self.graph.add_edge("rewriting", "retrieve")
        self.graph.add_edge("end", END)

    def compile_graph(self):
        return self.graph.compile()
