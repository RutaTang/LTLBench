import copy
import os
from typing import Dict

import backoff
import openai
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
        # For gpt-5 models, ignore temperature setting
        if self.config["model"].startswith("gpt-5") and "temperature" in config:
            config = {k: v for k, v in config.items() if k != "temperature"}
        self.config.update(config)

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_time=10)
    def chat(self, message: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": message,
            }],
            temperature=self.config["temperature"],
            model=self.config["model"],
            max_completion_tokens=self.config["max_tokens"],
        )
        chat_message = chat_completion.choices[0].message
        return chat_message.content

    def get_model_name(self) -> str:
        return self.config["model"]
