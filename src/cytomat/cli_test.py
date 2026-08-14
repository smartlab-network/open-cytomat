import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from cytomat import cli


class FakePlateHandler:
    def __init__(self) -> None:
        self.last_slot: int | None = None

    def move_plate_from_slot_to_transfer_station(self, slot: int) -> str:
        self.last_slot = slot
        return f"moved-{slot}"

    def open_transfer_door(self) -> str:
        return "door-opened"


class FakeMaintenanceController:
    pass


class FakeClimateController:
    pass


class FakeShakerController:
    pass


class FakeCytomat:
    last_serial_port: str | None = None

    def __init__(self, serial_port: str) -> None:
        self.serial_port = serial_port
        FakeCytomat.last_serial_port = serial_port
        self.plate_handler = FakePlateHandler()
        self.maintenance_controller = FakeMaintenanceController()
        self.climate_controller = FakeClimateController()
        self.shaker_controller = FakeShakerController()


class TestCli:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(cli, "Cytomat", FakeCytomat)
        FakeCytomat.last_serial_port = None

    def test_initialize_writes_config(self, tmp_path: Path) -> None:
        runner = CliRunner()
        config_file = tmp_path / "config.json"

        result = runner.invoke(
            cli.main,
            [
                "action",
                "--config-file",
                str(config_file),
                "initialize",
                "--port",
                "COM11",
            ],
        )

        assert result.exit_code == 0
        payload = json.loads(config_file.read_text(encoding="utf-8"))
        assert payload == {"COM_port": "COM11"}

    def test_plate_handler_command_uses_kebab_case_flag(self) -> None:
        runner = CliRunner()

        result = runner.invoke(
            cli.main,
            [
                "action",
                "--port",
                "COM3",
                "plate-handler",
                "move-plate-from-slot-to-transfer-station",
                "--slot",
                "5",
            ],
        )

        assert result.exit_code == 0
        assert "moved-5" in result.output

    def test_shortcuts_work_for_group_and_command_alias(self) -> None:
        runner = CliRunner()

        result = runner.invoke(cli.main, ["a", "--port", "COM3", "ph", "door-open"])

        assert result.exit_code == 0
        assert "door-opened" in result.output

    def test_auto_detects_single_usable_port_when_port_not_configured(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        runner = CliRunner()
        config_file = tmp_path / "config.json"
        monkeypatch.setattr(cli, "usable_serial_ports", lambda: ["COM42"])

        result = runner.invoke(
            cli.main,
            [
                "action",
                "--config-file",
                str(config_file),
                "plate-handler",
                "move-plate-from-slot-to-transfer-station",
                "--slot",
                "5",
            ],
        )

        assert result.exit_code == 0
        assert "Auto-detected serial port: COM42" in result.output
        assert FakeCytomat.last_serial_port == "COM42"

    def test_fails_when_multiple_usable_ports_found_without_explicit_configuration(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        runner = CliRunner()
        config_file = tmp_path / "config.json"
        monkeypatch.setattr(cli, "usable_serial_ports", lambda: ["COM4", "COM7"])

        result = runner.invoke(
            cli.main,
            [
                "action",
                "--config-file",
                str(config_file),
                "plate-handler",
                "door-open",
            ],
        )

        assert result.exit_code != 0
        assert "Multiple usable serial ports found: COM4, COM7" in result.output

    def test_help_shows_aliases_inline_without_duplicate_entries(self) -> None:
        runner = CliRunner()

        root_help = runner.invoke(cli.main, ["--help"])
        assert root_help.exit_code == 0
        assert "action [a]" in root_help.output

        action_help = runner.invoke(cli.main, ["action", "--help"])
        assert action_help.exit_code == 0
        assert "initialize [init]" in action_help.output
        assert "plate-handler [ph]" in action_help.output
        assert "climate-controller [cc]" in action_help.output
