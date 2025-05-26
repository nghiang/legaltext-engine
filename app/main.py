from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import Workflow
from gateway.langfuse_client import langfuse_client
from gateway.qdrant import qdrant_client, QdrantNeo4jPopulator
from gateway.azure_openai import azure_openai_client
import asyncio
import uvicorn

app = FastAPI(title="Workflow API")

collection_name = "8_seneca"


class QuestionInput(BaseModel):
    question: str


# Initialize langfuse callback
workflow_callback = langfuse_client.get_callback_handler_from_name(name="workflow")
config = {
    "callbacks": workflow_callback,
}

# Initialize QdrantNeo4jPopulator
populator = QdrantNeo4jPopulator(
    neo4j_uri="bolt://neo4j:7687",
    neo4j_auth=("neo4j", "password"),
    qdrant_client=qdrant_client,
    collection_name=collection_name,
)


@app.on_event("startup")
async def startup_event():
    """Populate Qdrant collection on application startup."""
    try:
        # await populator.populate_collection(azure_openai_client)
        print("Qdrant collection populated successfully.")
    except Exception as e:
        print(f"Failed to populate Qdrant collection: {e}")
        raise  


@app.on_event("shutdown")
async def shutdown_event():
    """Close Neo4j driver on application shutdown."""
    populator.close()
    print("Neo4j driver closed.")


@app.post("/invoke")
async def invoke_workflow(input: QuestionInput):
    try:
        initial_state = {"question": input.question}

        workflow = Workflow()
        with open('graph.png', 'wb') as f:
            f.write(workflow.graph.get_graph().draw_mermaid_png())
        result = await workflow.graph.ainvoke(initial_state, config)
        langfuse_client.update_trace(input_=initial_state, output=result)
        return {"status": "success", "result": result}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error invoking workflow: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
