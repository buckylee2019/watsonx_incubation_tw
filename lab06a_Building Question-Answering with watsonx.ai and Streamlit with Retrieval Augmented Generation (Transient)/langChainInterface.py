
from typing import Any, List, Mapping, Optional,Dict

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from ibm_watson_machine_learning.foundation_models import Model
from langchain.llms.utils import enforce_stop_tokens

# define LangChainInterface model
class LangChainInterface(LLM):
    credentials: Optional[Dict] = None
    model: Optional[str] = None
    params: Optional[Dict] = None
    project_id : Optional[str]=None
    @property
    def _llm_type(self) -> str:
        return "IBM WATSONX"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the WatsonX model"""
        params = self.params or {}
        model = Model(model_id=self.model, params=params, credentials=self.credentials, project_id=self.project_id)
        text = model.generate_text(prompt)
        if stop is not None:
            text = enforce_stop_tokens(text, stop)
        return text
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        
        _params = self.params or {}
        return {
            **{"model": self.model},
            **{"params": _params},
        }