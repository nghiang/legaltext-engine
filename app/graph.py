from config.singleton import SingletonMeta
from langgraph.graph import END, START, StateGraph
from nodes import Nodes
from langchain_config.schema import OverallState


class Workflow(metaclass=SingletonMeta):
    def __init__(self):
        # initiate graph state & nodes
        self.workflow = StateGraph(OverallState)
        self.nodes = Nodes()

        self.workflow.add_node("guardrails", self.nodes.guardrails)
        self.workflow.add_node(
            "answer_legal_questions", self.nodes.answer_legal_questions
        )
        self.workflow.add_node("retrieve_vector", self.nodes.retrieve_vector)
        self.workflow.add_node("retrieve_graph", self.nodes.retrieve_graph)
        self.workflow.add_node("rerank_document", self.nodes.rerank_document)
        self.workflow.add_node("generate_response", self.nodes.generate_response)

        self.workflow.add_edge(START, "guardrails")
        self.workflow.add_conditional_edges(
            "guardrails",
            self.nodes.guardrails_condition,
            {
                "answer_legal_questions": "answer_legal_questions",
                "answer_non_legal_questions": END,
            },
        )
        self.workflow.add_edge("answer_legal_questions", "retrieve_graph")
        self.workflow.add_edge("retrieve_graph", "retrieve_vector")
        self.workflow.add_conditional_edges(
            "retrieve_vector",
            self.nodes.route_based_on_search_strategies,
            {
                "generate_vector_search_response": "generate_response",
                "generate_graph_search_response": "generate_response",
                "generate_hybrid_search_response": "rerank_document",
            },
        )
        self.workflow.add_edge("rerank_document", "generate_response")
        self.workflow.add_edge("generate_response", END)

        self.graph = self.workflow.compile()
