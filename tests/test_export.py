from python_app.export import to_csv, to_json, to_markdown
from python_app.models import BusinessIdea


def test_exports_include_idea_content():
    idea = BusinessIdea("Exportable", "Useful description", "Tech", "Easy", "Sales", ("Research",))
    assert "Exportable" in to_json([idea])
    assert "title,industry" in to_csv([idea])
    assert "## Exportable" in to_markdown([idea])