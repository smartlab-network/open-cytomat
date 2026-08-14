from cytomat.status import PlateShuttleSystemStatus


def test_status_parse() -> None:
    # PDF P. 11
    status = PlateShuttleSystemStatus(
        busy=True,
        ready=False,
        warning=True,
        error=False,
        shovel_occupied=False,
        transfer_door_open=False,
        device_door_open=True,
        transfer_station_occupied=True,
    )

    assert PlateShuttleSystemStatus.from_hex_string("0xc5") == status
