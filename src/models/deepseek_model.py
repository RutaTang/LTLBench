import copy
import os
from typing import Dict

import backoff
from openai import OpenAI
from dotenv import find_dotenv, load_dotenv

from src.models.base_model import BaseModel


class DeepSeekModel(BaseModel):

    def __init__(self):
        super().__init__()
        load_dotenv(find_dotenv())
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.config = {
            "model": "deepseek-chat",
            "temperature": 0,
            "max_tokens": 20,
        }

    def reconfig(self, config: Dict[str, any]):
        self.config.update(config)

    @backoff.on_exception(backoff.expo, Exception, max_time=10)
    def chat(self, message: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": message,
            }],
            temperature=self.config["temperature"],
            model=self.config["model"],
            max_tokens=self.config["max_tokens"],
        )
        chat_message = chat_completion.choices[0].message
        return chat_message.content

    def get_model_name(self) -> str:
        return self.config["model"]
