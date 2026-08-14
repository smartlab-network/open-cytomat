import pytest

from cytomat.status import ErrorStatus, WarningStatus


class TestErrorStatus:
    @pytest.mark.parametrize(
        "hex_byte,expected",
        [
            ("00", ErrorStatus.NoError),
            ("01", ErrorStatus.MotorCommunicationDisrupted),
            ("FF", ErrorStatus.Critical),
        ],
    )
    def test_maps_known_hex_codes(self, hex_byte: str, expected: ErrorStatus) -> None:
        assert ErrorStatus.from_hex_string(hex_byte) is expected

    def test_raises_for_unknown_hex_code(self) -> None:
        with pytest.raises(ValueError):
            ErrorStatus.from_hex_string("11")


class TestWarningStatus:
    @pytest.mark.parametrize(
        "hex_byte,expected",
        [
            ("00", WarningStatus.NoWarning),
            ("09", WarningStatus.InitialisingDueToOpenedDeviceDoor),
            ("0C", WarningStatus.TransferStationNotRotated),
        ],
    )
    def test_maps_known_hex_codes(self, hex_byte: str, expected: WarningStatus) -> None:
        assert WarningStatus.from_hex_string(hex_byte) is expected

    def test_raises_for_unknown_hex_code(self) -> None:
        with pytest.raises(ValueError):
            WarningStatus.from_hex_string("0A")
