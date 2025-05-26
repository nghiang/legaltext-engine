from config.singleton import SingletonMeta
from langchain_config.prompt_template import PromptConstruction
from langchain_core.runnables import RunnableSequence
from gateway.azure_openai import azure_openai_client
from langchain_config.schema import GuardrailsOutput
from langchain_core.output_parsers import StrOutputParser
from langchain_neo4j import GraphCypherQAChain
from gateway.neo4j_client import graph


class Chains(metaclass=SingletonMeta):
    def __init__(self):
        self.prompt_construction = PromptConstruction()

    def guardrails_chain(self) -> RunnableSequence:
        chain = (
            self.prompt_construction.guardrails_system_prompt_template
            | azure_openai_client.chat_model.with_structured_output(GuardrailsOutput)
        )
        return chain  # type: ignore

    def generate_response_chain(self) -> RunnableSequence:
        chain = (
            self.prompt_construction.generate_response_prompt_template
            | azure_openai_client.chat_model
            | StrOutputParser()
        )
        return chain  # type: ignore

    def cypher_chain(self):
        chain = GraphCypherQAChain.from_llm(
            llm=azure_openai_client.chat_model,
            graph=graph,
            verbose=False,
            return_direct=True,
            validate_cypher=True,
            allow_dangerous_requests=True,
        )
        return chain
