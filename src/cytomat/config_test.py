import json
from pathlib import Path

from cytomat.config import CytomatConfig, load_config, save_config


class TestCytomatConfig:
    def test_load_returns_empty_config_when_file_missing(self, tmp_path: Path) -> None:
        config = load_config(tmp_path / "missing.json")

        assert config.com_port is None

    def test_load_parses_legacy_com_port_key(self, tmp_path: Path) -> None:
        config_file = tmp_path / "legacy.json"
        config_file.write_text(
            json.dumps({"COM_port": "COM9", "steps_per_mm_h": 170}),
            encoding="utf-8",
        )

        config = load_config(config_file)

        assert config.com_port == "COM9"

    def test_save_writes_com_port_alias(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.json"

        save_config(CytomatConfig(COM_port="COM7"), config_file)

        payload = json.loads(config_file.read_text(encoding="utf-8"))
        assert payload == {"COM_port": "COM7"}

    def test_save_omits_com_port_when_unset(self, tmp_path: Path) -> None:
        config_file = tmp_path / "config.json"

        save_config(CytomatConfig(), config_file)

        payload = json.loads(config_file.read_text(encoding="utf-8"))
        assert payload == {}
