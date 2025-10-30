from src.models.base_model import BaseModel
from src.models.ollama_model import OllamaModel
from src.models.openai_model import OpenAIModel
from src.models.deepseek_model import DeepSeekModel


def choose_model(model_name: str) -> BaseModel:
    """
    Choose the model based on the model name
    :return: a model object
    """
    if model_name in ["gpt-3.5-turbo", 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-5-mini']:
        model = OpenAIModel()
        model.reconfig({"model": model_name})
        return model
    elif model_name in ["llama3:70b-instruct", "qwen:72b-chat", "gemma:7b-instruct-q8_0", "gemma3:12b-it-q8_0",
                        "qwen3:14b", "qwen:7b-chat", "deepseek-r1:14b",
                        "mistral:7b-instruct", "qwen:32b", "qwen3:32b","phi4:14b"]:
        model = OllamaModel()
        model.reconfig({"model": model_name})
        return model
    elif model_name in ["deepseek-chat", "deepseek-reasoner"]:
        model = DeepSeekModel()
        model.reconfig({"model": model_name})
        return model
    else:
        raise ValueError(f"Unknown model: {model_name}")
