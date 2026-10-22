from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Domain031Sub04Entity:
    field_0: str
    field_1: str
    field_2: str
    field_3: str
    field_4: str
    field_5: str
    field_6: str
    field_7: str
    field_8: str
    field_9: str
    field_10: str
    field_11: str
    field_12: str
    field_13: str
    field_14: str
    field_15: str
    field_16: str
    field_17: str
    field_18: str
    field_19: str
    field_20: str
    field_21: str
    field_22: str
    field_23: str
    field_24: str
    field_25: str
    field_26: str
    field_27: str
    field_28: str
    field_29: str
    created_at: str
    updated_at: str
    is_active: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_0": self.field_0,
            "field_1": self.field_1,
            "field_2": self.field_2,
            "field_3": self.field_3,
            "field_4": self.field_4,
            "field_5": self.field_5,
            "field_6": self.field_6,
            "field_7": self.field_7,
            "field_8": self.field_8,
            "field_9": self.field_9,
            "field_10": self.field_10,
            "field_11": self.field_11,
            "field_12": self.field_12,
            "field_13": self.field_13,
            "field_14": self.field_14,
            "field_15": self.field_15,
            "field_16": self.field_16,
            "field_17": self.field_17,
            "field_18": self.field_18,
            "field_19": self.field_19,
            "field_20": self.field_20,
            "field_21": self.field_21,
            "field_22": self.field_22,
            "field_23": self.field_23,
            "field_24": self.field_24,
            "field_25": self.field_25,
            "field_26": self.field_26,
            "field_27": self.field_27,
            "field_28": self.field_28,
            "field_29": self.field_29,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active
        }
        
    def validate(self) -> bool:
        if not self.created_at: return False
        if not self.field_0: return False
        return True
