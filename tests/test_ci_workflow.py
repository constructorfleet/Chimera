from pathlib import Path


def test_ci_workflow_exists():
    workflow_path = (
        Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
    )
    assert workflow_path.exists(), "CI workflow file is missing"


def test_ci_workflow_commands_present():
    workflow_path = (
        Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
    )
    content = workflow_path.read_text()
    assert "pull_request" in content, "CI workflow should run on pull requests"
    assert "black --check ." in content, "CI workflow should run black formatting check"
    assert "flake8" in content, "CI workflow should run linting"
    assert "pytest" in content, "CI workflow should run test suite"
