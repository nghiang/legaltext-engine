from qdrant_client import QdrantClient

qdrant_client = QdrantClient(url="http://qdrant:6333", api_key=None)

from neo4j import GraphDatabase
from qdrant_client.http.models import Distance, VectorParams, PointStruct


class QdrantNeo4jPopulator:
    def __init__(
        self,
        neo4j_uri,
        neo4j_auth,
        qdrant_client,
        collection_name,
        embedding_size=3072,
        distance_metric=Distance.COSINE,
    ):
        """
        Initialize the populator with Neo4j and Qdrant configurations.

        Args:
            neo4j_uri (str): URI for Neo4j database (e.g., "bolt://neo4j:7687")
            neo4j_auth (tuple): Neo4j credentials (username, password)
            qdrant_client (QdrantClient): Initialized Qdrant client
            collection_name (str): Name of the Qdrant collection
            embedding_size (int): Size of the embedding vectors
            distance_metric (Distance): Qdrant distance metric (e.g., Distance.COSINE)
        """
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=neo4j_auth)
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name
        self.embedding_size = embedding_size
        self.distance_metric = distance_metric

    async def populate_collection(
        self, azure_openai_client, neo4j_query="MATCH (n) RETURN n.id, n.content"
    ):
        """
        Create Qdrant collection if it doesn't exist and populate it with Neo4j data embeddings.

        Args:
            azure_openai_client: Client for generating embeddings (must have llm_embeddings.aembed_query)
            neo4j_query (str): Cypher query to fetch data from Neo4j
        """
        try:
            # Create Qdrant collection if it doesn't exist
            if not self.qdrant_client.collection_exists(self.collection_name):
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_size, distance=self.distance_metric
                    ),
                )
                print(f"Created Qdrant collection: {self.collection_name}")

            # Fetch data from Neo4j and generate embeddings
            points = []
            with self.neo4j_driver.session() as session:
                result = session.run(neo4j_query)
                for record in result:
                    neo4j_id = record["n.id"]
                    text = record["n.content"]
                    if not text or not isinstance(text, str) or text.strip() == "":
                        continue
                    print(f"Processing record: {record}")
                    embedding = await azure_openai_client.llm_embeddings.aembed_query(
                        text
                    )
                    # Create point for Qdrant
                    points.append(
                        PointStruct(
                            id=neo4j_id,
                            vector=embedding,
                            payload={"neo4j_id": neo4j_id},
                        )
                    )

            # Upsert points to Qdrant
            if points:
                self.qdrant_client.upsert(
                    collection_name=self.collection_name, points=points
                )
                print(
                    f"Upserted {len(points)} points to Qdrant collection: {self.collection_name}"
                )
            else:
                print("No data retrieved from Neo4j to upsert.")

        except Exception as e:
            print(f"Error populating Qdrant collection: {e}")
            raise

    def close(self):
        """Close the Neo4j driver connection."""
        self.neo4j_driver.close()
