from __future__ import annotations

from pathlib import Path

from policygraph.paths import PROJECT_ROOT


def test_fuseki_scripts_reference_expected_endpoint() -> None:
    for script in [
        PROJECT_ROOT / "scripts" / "load_fuseki.sh",
        PROJECT_ROOT / "scripts" / "query_fuseki.sh",
    ]:
        assert script.exists()
        assert "http://localhost:3030/policygraph/sparql" in script.read_text(encoding="utf-8")


def test_docker_compose_exists() -> None:
    assert (PROJECT_ROOT / "docker-compose.yml").exists()
    assert Path(PROJECT_ROOT / "docker-compose.yml").read_text(encoding="utf-8")
