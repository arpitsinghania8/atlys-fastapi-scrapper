from abc import ABC, abstractmethod
import json
from typing import List, Dict

class StorageStrategy(ABC):
    @abstractmethod
    def save_products(self, products: List[Dict]) -> None:
        pass

    @abstractmethod
    def get_products(self) -> List[Dict]:
        pass

class JSONStorage(StorageStrategy):
    def __init__(self, file_path: str = "products.json"):
        self.file_path = file_path

    def save_products(self, products: List[Dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(products, f, indent=2)

    def get_products(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
