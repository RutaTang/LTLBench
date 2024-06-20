from src.models.base_model import BaseModel
from src.models.ollama_model import OllamaModel
from src.models.openai_model import OpenAIModel


def choose_model(model_name: str) -> BaseModel:
    if model_name in ["gpt-3.5-turbo"]:
        model = OpenAIModel()
        model.reconfig({"model": model_name})
        return model
    elif model_name in ["llama3:70b-instruct", "qwen:72b-chat", "gemma:7b-instruct", "qwen:7b-chat",
                        "mistral:7b-instruct"]:
        model = OllamaModel()
        model.reconfig({"model": model_name})
        return model
    else:
        raise ValueError(f"Unknown model: {model_name}")
