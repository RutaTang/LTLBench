import copy
import os
from typing import Dict

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

from src.models.base_model import BaseModel


class OpenAIModel(BaseModel):

    def __init__(self):
        super().__init__()
        load_dotenv(find_dotenv())
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
        self.config = {
            "model": "gpt-3.5-turbo",
            "temperature": 0,
            "max_tokens": 20,
        }

    def reconfig(self, config: Dict[str, any]):
        self.config.update(config)

    def chat(self, message: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": message,
            }],
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
        )
        chat_message = chat_completion.choices[0].message
        return chat_message.content
