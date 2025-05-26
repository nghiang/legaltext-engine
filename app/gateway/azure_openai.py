from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from config.settings import (
    AZURE_API_KEY,
    AZURE_API_VERSION,
    AZURE_DEPLOYMENT,
    AZURE_ENDPOINT,
    AZURE_MODEL,
    AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT,
)


class AzureOpenAIClient:
    def __init__(self):
        self._chat_model = AzureChatOpenAI(
            api_version=AZURE_API_VERSION,  # type: ignore
            azure_endpoint=AZURE_ENDPOINT,  # type: ignore
            azure_deployment=AZURE_DEPLOYMENT,  # type: ignore
            model=AZURE_MODEL,
            api_key=AZURE_API_KEY,  # type: ignore
            streaming=True,
            temperature=0.0,
        )

        self._llm_embeddings = AzureOpenAIEmbeddings(
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_ENDPOINT,
            azure_deployment=AZURE_OPENAI_EMBED_MODEL_DEPLOYMENT,
            api_key=AZURE_API_KEY,  # type: ignore
            chunk_size=1,
        )

    @property
    def chat_model(self):
        return self._chat_model

    @property
    def llm_embeddings(self):
        return self._llm_embeddings


azure_openai_client = AzureOpenAIClient()
