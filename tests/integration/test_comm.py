import pytest

from cytomat import Cytomat, first_usable_serial_port


@pytest.mark.integration
def test_can_connect_to_cytomat() -> None:
    serial_port = first_usable_serial_port()
    if serial_port is None:
        pytest.skip("No usable serial port found; skipping hardware integration test")
    assert serial_port is not None

    cytomat = Cytomat(serial_port)
    assert cytomat is not None
    cytomat.serial_port.close()
