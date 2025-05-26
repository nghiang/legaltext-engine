from typing import Any, Union
from langfuse import Langfuse
from langfuse.client import StatefulClient
from langfuse.callback.langchain import LangchainCallbackHandler


class LangfuseClient:
    def __init__(self):
        self._langfuse = Langfuse(
            public_key="",
            secret_key="",
            host="http://langfuse:3000",
        )

    @property
    def langfuse(self):
        return self._langfuse

    def init_trace(self, name: str) -> Union[StatefulClient, None]:
        initialized_trace = None
        initialized_trace = self._langfuse.trace(
            name=name,
        )

        return initialized_trace

    def update_trace(self, input_: Any, output: Any) -> Union[StatefulClient, None]:
        updated_trace = None
        current_trace_id = self._langfuse.get_trace_id()
        updated_trace = self._langfuse.trace(
            id=current_trace_id, input=input_, output=output
        )

        return updated_trace

    def get_langfuse_handler(
        self, trace: StatefulClient
    ) -> Union[LangchainCallbackHandler, None]:
        langfuse_handler = None
        langfuse_handler = trace.get_langchain_handler()  # type: ignore

        return langfuse_handler

    def get_callback_handler_from_name(
        self, name: str
    ) -> list[LangchainCallbackHandler]:
        trace = self.init_trace(name)
        handler = self.get_langfuse_handler(trace)  # type: ignore
        callbacks = [handler] if handler else []

        return callbacks


langfuse_client = LangfuseClient()
