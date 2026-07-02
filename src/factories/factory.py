from typing import Any
from abc import ABC, abstractmethod

class Factory(ABC):
    @abstractmethod
    def create(self) -> Any:
        pass

    @abstractmethod
    def create_as_txt(self, file_path: str) -> None:
        pass
