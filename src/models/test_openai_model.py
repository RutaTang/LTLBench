from unittest import TestCase

from src.models.openai_model import OpenAIModel


class TestOpenAIModel(TestCase):
    def test_model(self):
        model = OpenAIModel()
        message = "Hello, how are you?"
        content = model.chat(message)
        print(content)
        self.assertTrue(len(content) > 0)
