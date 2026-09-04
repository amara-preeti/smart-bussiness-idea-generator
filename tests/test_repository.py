from python_app.models import BusinessIdea
from python_app.repository import IdeaRepository


def test_repository_round_trip(tmp_path):
    repository = IdeaRepository(tmp_path / "ideas.json")
    idea = BusinessIdea("Local", "Description", "Tech", "Easy", "Sales", ("Research",))
    repository.save(idea)
    repository.save(idea)
    assert repository.list() == [idea]
    assert repository.remove("Local") is True
    assert repository.list() == []