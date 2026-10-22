from typing import List, Dict, Any
from .domain_039_sub_03_models import Domain039Sub03Entity
from .domain_039_sub_03_repository import Domain039Sub03Repository

class Domain039Sub03Service:
    def __init__(self, repo: Domain039Sub03Repository):
        self.repo = repo
        
    def process_new_entity(self, data: Dict[str, Any]) -> bool:
        entity = Domain039Sub03Entity(
            field_0=data.get("field_0", ""),
            field_1=data.get("field_1", ""),
            field_2=data.get("field_2", ""),
            field_3=data.get("field_3", ""),
            field_4=data.get("field_4", ""),
            field_5=data.get("field_5", ""),
            field_6=data.get("field_6", ""),
            field_7=data.get("field_7", ""),
            field_8=data.get("field_8", ""),
            field_9=data.get("field_9", ""),
            field_10=data.get("field_10", ""),
            field_11=data.get("field_11", ""),
            field_12=data.get("field_12", ""),
            field_13=data.get("field_13", ""),
            field_14=data.get("field_14", ""),
            field_15=data.get("field_15", ""),
            field_16=data.get("field_16", ""),
            field_17=data.get("field_17", ""),
            field_18=data.get("field_18", ""),
            field_19=data.get("field_19", ""),
            field_20=data.get("field_20", ""),
            field_21=data.get("field_21", ""),
            field_22=data.get("field_22", ""),
            field_23=data.get("field_23", ""),
            field_24=data.get("field_24", ""),
            field_25=data.get("field_25", ""),
            field_26=data.get("field_26", ""),
            field_27=data.get("field_27", ""),
            field_28=data.get("field_28", ""),
            field_29=data.get("field_29", ""),
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
        return {
            "total": len(all_items),
            "active": self.repo.count_active(),
            "inactive": len(all_items) - self.repo.count_active()
        }
        
    def export_data(self) -> List[Dict[str, Any]]:
        return [item.to_dict() for item in self.repo.get_all()]
