import pathlib


def test_project_skeleton_exists():
    base = pathlib.Path(__file__).resolve().parents[1]
    required = [
        "README.md",
        ".gitignore",
        "backbone/docker-compose.bus.yml",
        "backbone/configs/emqx/emqx.conf",
        "backbone/configs/emqx/acl.conf",
        "backbone/configs/redis/redis.conf",
        "backbone/configs/nats/nats.conf",
        "backbone/configs/redpanda/redpanda.yaml",
        "backbone/backup/backup-configs.sh",
        "backbone/backup/backup-data.sh",
        "ansible/inventory",
        "ansible/bus-stack.yml",
        "ansible/files/docker-compose.bus.yml",
        "ansible/templates/configs/emqx/emqx.conf.j2",
        "ansible/templates/configs/redis/redis.conf.j2",
        "ansible/templates/configs/nats/nats.conf.j2",
        "ansible/templates/configs/redpanda/redpanda.yaml.j2",
        "services/common/pyproject.toml",
        "services/common/src/lattice/__init__.py",
        "services/common/src/lattice/config.py",
        "services/common/src/lattice/mqtt_client.py",
        "services/common/src/lattice/redis_client.py",
        "services/common/src/lattice/nats_client.py",
        "services/audio-router/pyproject.toml",
        "services/audio-router/Dockerfile",
        "services/audio-router/src/vox/__init__.py",
        "services/audio-router/src/vox/main.py",
        "services/vision-router/pyproject.toml",
        "services/vision-router/Dockerfile",
        "services/vision-router/src/gaze/__init__.py",
        "services/vision-router/src/gaze/main.py",
        "services/llm-router/pyproject.toml",
        "services/llm-router/Dockerfile",
        "services/llm-router/src/mind/__init__.py",
        "services/llm-router/src/mind/main.py",
        "docker/base-python/Dockerfile",
        "docker/base-python/requirements.txt",
    ]
    for rel in required:
        assert (base / rel).exists(), f"missing {rel}"


def test_python_versions_declared():
    base = pathlib.Path(__file__).resolve().parents[1]
    pyprojects = [
        base / "services/common/pyproject.toml",
        base / "services/audio-router/pyproject.toml",
        base / "services/vision-router/pyproject.toml",
        base / "services/llm-router/pyproject.toml",
    ]
    for pyproject in pyprojects:
        text = pyproject.read_text()
        assert 'python = "3.14"' in text, f"python version missing in {pyproject}"
