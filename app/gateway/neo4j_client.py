from langchain_neo4j import Neo4jGraph


graph = Neo4jGraph(
    url="bolt://neo4j:7687",
    username="neo4j",
    password="password",
    enhanced_schema=True,
)
