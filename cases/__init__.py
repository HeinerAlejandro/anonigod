from abc import ABC, abstractmethod

class Case(ABC):
    @abstractmethod
    def start(self):
        pass