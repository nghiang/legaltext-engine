from config.singleton import SingletonMeta
from langchain_config.chain import Chains
from langchain_config.schema import (
    OverallState,
    GuardrailsOutput,
)
from gateway.neo4j_client import graph
from typing import Literal
from neo4j_graphrag.retrievers import QdrantNeo4jRetriever
from neo4j import GraphDatabase
from gateway.azure_openai import azure_openai_client
from gateway.qdrant import qdrant_client
from langchain_core.runnables import RunnableConfig

from langchain_neo4j import GraphCypherQAChain


class Nodes(metaclass=SingletonMeta):
    def __init__(self):
        self.chains = Chains()

    async def guardrails(self, state: OverallState) -> OverallState:
        guardrails_ouput: (
            GuardrailsOutput
        ) = await self.chains.guardrails_chain().ainvoke(
            {"question": state.get("question")}
        )
        if guardrails_ouput.decision == "non_legal_questions":
            return {
                **state,
                "type": "non_legal_questions",
                "answer": "This question is not related to laws.",
            }  # type: ignore
        return {**state, "type": guardrails_ouput.decision}  # type: ignore

    async def generate_response(self, state: OverallState):
        if state.get("type") == "graph_search":
            final_answer = await self.chains.generate_response_chain().ainvoke(
                {
                    "question": state.get("question"),
                    "results": state.get("graph_search_data"),
                }
            )
            return {"answer": final_answer}  # type: ignore
        elif state.get("type") == "vector_search":
            final_answer = await self.chains.generate_response_chain().ainvoke(
                {
                    "question": state.get("question"),
                    "results": state.get("vector_search_data"),
                }
            )
            return {"answer": final_answer}
        elif state.get("type") == "hybrid_search":
            final_answer = await self.chains.generate_response_chain().ainvoke(
                {
                    "question": state.get("question"),
                    "results": state.get("hybrid_search_data"),
                }
            )
            return {"answer": final_answer}
        return {**state}

    async def rerank_document(self, state: OverallState):
        return {**state}  # type: ignore

    def guardrails_condition(
        self,
        state: OverallState,
    ) -> Literal["answer_legal_questions", "answer_non_legal_questions"]:  # type: ignore
        if state.get("type") == "non_legal_questions":
            return "answer_non_legal_questions"
        return "answer_legal_questions"

    def answer_legal_questions(
        self,
        state: OverallState,
        config: RunnableConfig,
    ):
        return {**state}

    async def retrieve_graph(self, state: OverallState):
        try:
            cypher_chain = self.chains.cypher_chain()
            result = await cypher_chain.ainvoke(
                {
                    "query": state.get("question"),
                }
            )
            return {**state, "graph_search_data": result["result"]}  # type: ignore
        except Exception as e:
            print(f"Error during graph search: {e}")
            return {**state, "graph_search_data": []}

    def route_based_on_search_strategies(
        self,
        state: OverallState,
        config: RunnableConfig,
    ) -> Literal[
        "generate_vector_search_response",
        "generate_graph_search_response",
        "generate_hybrid_search_response",
    ]:
        if state.get("type") == "vector_search":
            return "generate_vector_search_response"
        elif state.get("type") == "graph_search":
            return "generate_graph_search_response"
        else:
            return "generate_hybrid_search_response"

    async def retrieve_vector(self, state: OverallState):
        try:
            with GraphDatabase.driver(
                "bolt://neo4j:7687", auth=("neo4j", "password")
            ) as neo4j_driver:
                retriever = QdrantNeo4jRetriever(
                    driver=neo4j_driver,
                    client=qdrant_client,
                    collection_name="8_seneca",
                    id_property_external="neo4j_id",
                    id_property_neo4j="id",
                )
                embedding = await azure_openai_client.llm_embeddings.aembed_query(
                    state.get("question")
                )
                vector_search_data = retriever.search(query_vector=embedding, top_k=10)
                return {**state, "vector_search_data": vector_search_data}
        except Exception as e:
            print(f"Error during vector search: {e}")
            return {**state, "vector_search_data": []}

    async def answer_non_related_question(self, state: OverallState):
        return {
            **state,
        }  # type: ignore
