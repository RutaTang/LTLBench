from abc import ABC, abstractmethod
from typing import Dict


class BaseModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def chat(self, message: str) -> str:
        pass

    @abstractmethod
    def reconfig(self, config: Dict[str, any]):
        pass
