from cytomat import Cytomat
from cytomat.status import OverviewStatus

def test_status_parse():
    # PDF P. 11
    s = OverviewStatus(busy =True, ready=False, warning=True, error=False,
                       shovel_occupied=False, transfer_door_open=False,
                       device_door_open=True, transfer_station_occupied=True)

    assert OverviewStatus.from_hex_string("0xc5") == s
