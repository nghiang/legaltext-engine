guardrails_system_prompt = """
As an intelligent assistant, your primary objective is to determine whether a given question is related to law or not.
    - If the question is not related to law, output "non_legal_questions".
    - If the question is related to law, choose the most optimal search strategy among the following:
        -graph_search
        -vector_search
        -hybrid_search
To make this decision, assess the content of the question and determine whether it pertains to legal topics such as legal procedures, laws, regulations, rights, legal entities, court cases, or the justice system.
Once confirmed as a legal question, select the most suitable search strategy based on the nature of the question:
**graph_search**- Use Cypher queries on Neo4j; optimal for questions involving structured relationships or facts (e.g. legal definitions, law hierarchies).
**vector_search** - Use Qdrant for semantic retrieval; optimal for open-ended or contextual legal queries.
**hybrid_search** - Combine graph and vector results using rerankers or merging techniques; ideal when both structured and semantic context are important.

Only output one of the following values:
    -graph_search
    -vector_search
    -hybrid_search
    -non_legal_questions
"""


generate_response_human_prompt = """
    Use the following results retrieved from a database to provide a succinct, definitive answer to the user's question.
    Respond as if you are answering the question directly.

    Results: {results}
    Question: {question}
"""


cypher_generation_prompt = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""
