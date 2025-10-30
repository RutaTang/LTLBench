import copy
import os
from typing import Dict
import ollama
from ollama import Client
from dotenv import find_dotenv, load_dotenv

from src.models.base_model import BaseModel


class OllamaModel(BaseModel):

    def __init__(self):
        super().__init__()
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.client = Client(host=ollama_url)

        self.config = {
            "model": "gemma:7b-instruct",
            "temperature": 0,
            "max_tokens": 20,
        }

    def chat(self, message: str) -> str:
        chat_completion = self.client.chat(
            messages=[{
                "role": "user",
                "content": message
            }],
            model=self.config["model"],
            options={
                "temperature": self.config["temperature"],
                "num_predict": self.config["max_tokens"]
            }
        )
        chat_message = chat_completion["message"]["content"]
        return chat_message

    def reconfig(self, config: Dict[str, any]):
        self.config.update(config)

    def get_model_name(self) -> str:
        return self.config["model"]
