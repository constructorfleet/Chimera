from pathlib import Path


def test_bus_compose_mounts_configs_and_volumes():
    compose_path = (
        Path(__file__).resolve().parents[1] / "backbone" / "docker-compose.bus.yml"
    )
    contents = compose_path.read_text()
    expected_snippets = [
        "source: redis_config",
        "source: nats_config",
        "source: redpanda_config",
        "${REDIS_PORT:-6379}:6379",
        "${NATS_PORT:-4222}:4222",
        "${NATS_HTTP_PORT:-8222}:8222",
        "${REDPANDA_KAFKA_PORT:-9092}:9092",
        "${REDPANDA_ADMIN_PORT:-9644}:9644",
        "redis_data:",
        "redis_config:",
        "nats_data:",
        "nats_config:",
        "redpanda_data:",
        "redpanda_config:",
    ]
    for snippet in expected_snippets:
        assert snippet in contents, f"missing compose snippet: {snippet}"


def test_backup_services_are_configurable_jobs():
    compose_path = (
        Path(__file__).resolve().parents[1] / "backbone" / "docker-compose.bus.yml"
    )
    contents = compose_path.read_text()
    expected_snippets = [
        "data-backup:",
        "config-backup:",
        "DATA_BACKUP_INTERVAL_SECONDS",
        "CONFIG_BACKUP_INTERVAL_SECONDS",
        "backup-data.sh",
        "backup-configs.sh",
        "./:/backbone",
    ]
    for snippet in expected_snippets:
        assert snippet in contents, f"missing backup configuration snippet: {snippet}"
