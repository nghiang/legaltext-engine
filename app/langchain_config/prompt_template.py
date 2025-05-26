from config.singleton import SingletonMeta
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_config.prompt import (
    guardrails_system_prompt,
    generate_response_human_prompt,
    cypher_generation_prompt,
)


class PromptConstruction(metaclass=SingletonMeta):

    def __init__(self):
        self.guardrails_system_prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", guardrails_system_prompt),
                ("human", "{question}"),
            ]
        )

        self.generate_response_prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant",
                ),
                (
                    "human",
                    generate_response_human_prompt,
                ),
            ]
        )

        self.cypher_generation_prompt_template = PromptTemplate(
            input_variables=["schema", "question"], template=cypher_generation_prompt
        )
