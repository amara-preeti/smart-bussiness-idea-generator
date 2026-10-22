from typing import List, Optional
from .domain_001_sub_01_models import Domain001Sub01Entity

class Domain001Sub01Repository:
    def __init__(self):
        self._storage: List[Domain001Sub01Entity] = []
        
    def add(self, entity: Domain001Sub01Entity) -> None:
        self._storage.append(entity)
        
    def get_all(self) -> List[Domain001Sub01Entity]:
        return self._storage
        
    def find_by_field_0(self, val: str) -> Optional[Domain001Sub01Entity]:
        for item in self._storage:
            if item.field_0 == val:
                return item
        return None
        
    def delete(self, val: str) -> bool:
        initial_len = len(self._storage)
        self._storage = [x for x in self._storage if x.field_0 != val]
        return len(self._storage) < initial_len
        
    def count_active(self) -> int:
        return sum(1 for x in self._storage if x.is_active)
