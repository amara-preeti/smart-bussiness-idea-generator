from typing import List, Optional
from .domain_018_sub_05_models import Domain018Sub05Entity

class Domain018Sub05Repository:
    def __init__(self):
        self._storage: List[Domain018Sub05Entity] = []
        
    def add(self, entity: Domain018Sub05Entity) -> None:
        self._storage.append(entity)
        
    def get_all(self) -> List[Domain018Sub05Entity]:
        return self._storage
        
    def find_by_field_0(self, val: str) -> Optional[Domain018Sub05Entity]:
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
