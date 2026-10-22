from typing import List, Optional
from .domain_041_sub_03_models import Domain041Sub03Entity

class Domain041Sub03Repository:
    def __init__(self):
        self._storage: List[Domain041Sub03Entity] = []
        
    def add(self, entity: Domain041Sub03Entity) -> None:
        self._storage.append(entity)
        
    def get_all(self) -> List[Domain041Sub03Entity]:
        return self._storage
        
    def find_by_field_0(self, val: str) -> Optional[Domain041Sub03Entity]:
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
