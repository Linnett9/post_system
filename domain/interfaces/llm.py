from abc import ABC, abstractmethod

class ILLM(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass