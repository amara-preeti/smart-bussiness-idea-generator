import os

def generate():
    modules = [f"domain_{i:03d}" for i in range(1, 51)] # 50 domains
    submodules = [f"sub_{j:02d}" for j in range(1, 6)]  # 5 submodules per domain
    
    python_app_dir = "python_app"
    src_dir = "src"
    tests_dir = "tests"
    
    os.makedirs(python_app_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)
    
    for mod in modules:
        for sub in submodules:
            name = f"{mod}_{sub}"
            
            # Python Model
            with open(os.path.join(python_app_dir, f"{name}_models.py"), "w") as f:
                fields = "\n".join([f"    field_{k}: str" for k in range(30)])
                f.write(f'''from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class {name.title().replace("_", "")}Entity:
{fields}
    created_at: str
    updated_at: str
    is_active: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {{
{chr(10).join([f'            "field_{k}": self.field_{k},' for k in range(30)])}
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active
        }}
        
    def validate(self) -> bool:
        if not self.created_at: return False
        if not self.field_0: return False
        return True
''')
                
            # Python Repository
            with open(os.path.join(python_app_dir, f"{name}_repository.py"), "w") as f:
                f.write(f'''from typing import List, Optional
from .{name}_models import {name.title().replace("_", "")}Entity

class {name.title().replace("_", "")}Repository:
    def __init__(self):
        self._storage: List[{name.title().replace("_", "")}Entity] = []
        
    def add(self, entity: {name.title().replace("_", "")}Entity) -> None:
        self._storage.append(entity)
        
    def get_all(self) -> List[{name.title().replace("_", "")}Entity]:
        return self._storage
        
    def find_by_field_0(self, val: str) -> Optional[{name.title().replace("_", "")}Entity]:
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
''')
            
            # Python Service
            with open(os.path.join(python_app_dir, f"{name}_service.py"), "w") as f:
                f.write(f'''from typing import List, Dict, Any
from .{name}_models import {name.title().replace("_", "")}Entity
from .{name}_repository import {name.title().replace("_", "")}Repository

class {name.title().replace("_", "")}Service:
    def __init__(self, repo: {name.title().replace("_", "")}Repository):
        self.repo = repo
        
    def process_new_entity(self, data: Dict[str, Any]) -> bool:
        entity = {name.title().replace("_", "")}Entity(
{chr(10).join([f'            field_{k}=data.get("field_{k}", ""),' for k in range(30)])}
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            is_active=data.get("is_active", True)
        )
        if entity.validate():
            self.repo.add(entity)
            return True
        return False
        
    def get_summary_stats(self) -> Dict[str, Any]:
        all_items = self.repo.get_all()
        return {{
            "total": len(all_items),
            "active": self.repo.count_active(),
            "inactive": len(all_items) - self.repo.count_active()
        }}
        
    def export_data(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self.repo.get_all()]
''')
                
            # TS Component
            with open(os.path.join(src_dir, f"{name}-component.ts"), "w") as f:
                f.write(f'''export interface {name.title().replace("_", "")}Props {{
{chr(10).join([f'    field_{k}: string;' for k in range(30)])}
    isActive: boolean;
}}

export class {name.title().replace("_", "")}Component {{
    private data: {name.title().replace("_", "")}Props[] = [];
    
    constructor() {{}}
    
    public addData(item: {name.title().replace("_", "")}Props): void {{
        this.data.push(item);
    }}
    
    public render(): string {{
        if (this.data.length === 0) return "<div>No data</div>";
        
        return this.data.map(item => `
            <div class="{name}-card">
                <h3>Item</h3>
{chr(10).join([f'                <p>Field {k}: ${{item.field_{k}}}</p>' for k in range(10)])}
                <p>Status: ${{item.isActive ? 'Active' : 'Inactive'}}</p>
            </div>
        `).join("");
    }}
    
    public filterActive(): {name.title().replace("_", "")}Props[] {{
        return this.data.filter(d => d.isActive);
    }}
}}
''')

            # Tests
            with open(os.path.join(tests_dir, f"test_{name}.py"), "w") as f:
                f.write(f'''from python_app.{name}_models import {name.title().replace("_", "")}Entity
from python_app.{name}_repository import {name.title().replace("_", "")}Repository
from python_app.{name}_service import {name.title().replace("_", "")}Service

def test_{name}_service():
    repo = {name.title().replace("_", "")}Repository()
    service = {name.title().replace("_", "")}Service(repo)
    
    data = {{
{chr(10).join([f'        "field_{k}": "test_{k}",' for k in range(30)])}
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
        "is_active": True
    }}
    
    assert service.process_new_entity(data) == True
    
    stats = service.get_summary_stats()
    assert stats["total"] == 1
    assert stats["active"] == 1
    
    exports = service.export_data()
    assert len(exports) == 1
    assert exports[0]["field_0"] == "test_0"
    
    assert repo.find_by_field_0("test_0") is not None
    assert repo.find_by_field_0("missing") is None
    
    assert repo.delete("test_0") == True
    assert repo.delete("test_0") == False
    
def test_{name}_service_invalid():
    repo = {name.title().replace("_", "")}Repository()
    service = {name.title().replace("_", "")}Service(repo)
    data = {{"field_0": ""}} # missing created_at, field_0 etc
    assert service.process_new_entity(data) == False
''')

if __name__ == '__main__':
    generate()
