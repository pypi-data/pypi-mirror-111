from abc import ABC, abstractmethod

class Rule(ABC):
    @abstractmethod
    def fingerprint(target):
        pass
