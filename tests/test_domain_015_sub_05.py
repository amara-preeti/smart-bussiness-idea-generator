from python_app.domain_015_sub_05_models import Domain015Sub05Entity
from python_app.domain_015_sub_05_repository import Domain015Sub05Repository
from python_app.domain_015_sub_05_service import Domain015Sub05Service

def test_domain_015_sub_05_service():
    repo = Domain015Sub05Repository()
    service = Domain015Sub05Service(repo)
    
    data = {
        "field_0": "test_0",
        "field_1": "test_1",
        "field_2": "test_2",
        "field_3": "test_3",
        "field_4": "test_4",
        "field_5": "test_5",
        "field_6": "test_6",
        "field_7": "test_7",
        "field_8": "test_8",
        "field_9": "test_9",
        "field_10": "test_10",
        "field_11": "test_11",
        "field_12": "test_12",
        "field_13": "test_13",
        "field_14": "test_14",
        "field_15": "test_15",
        "field_16": "test_16",
        "field_17": "test_17",
        "field_18": "test_18",
        "field_19": "test_19",
        "field_20": "test_20",
        "field_21": "test_21",
        "field_22": "test_22",
        "field_23": "test_23",
        "field_24": "test_24",
        "field_25": "test_25",
        "field_26": "test_26",
        "field_27": "test_27",
        "field_28": "test_28",
        "field_29": "test_29",
        "created_at": "2023-01-01",
        "updated_at": "2023-01-01",
        "is_active": True
    }
    
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
    
def test_domain_015_sub_05_service_invalid():
    repo = Domain015Sub05Repository()
    service = Domain015Sub05Service(repo)
    data = {"field_0": ""} # missing created_at, field_0 etc
    assert service.process_new_entity(data) == False
