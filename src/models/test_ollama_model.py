from unittest import TestCase

from src.models.ollama_model import OllamaModel


class TestOllama(TestCase):
    def test_predict(self):
        model = OllamaModel()
        message = "Hello"
        content = model.chat(message)
        self.assertTrue(len(content) > 0)