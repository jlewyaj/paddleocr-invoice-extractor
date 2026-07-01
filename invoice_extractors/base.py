from abc import ABC, abstractmethod


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, lines):
        pass

    def clean(self, text):
        return " ".join(text.split())