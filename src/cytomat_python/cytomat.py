from datetime import datetime, timedelta
import time
from typing import Union

from cytomat_python.barcode_scanner import BarcodeScanner
from cytomat_python.climate_controller import ClimateController
from cytomat_python.maintenance_controller import MaintenanceController
from cytomat_python.plate_handler import PlateHandler
from cytomat_python.serial_port import SerialPort
from cytomat_python.shaker_controller import ShakerController
from cytomat_python.status import OverviewStatus, ErrorStatus, WarningStatus, ActionStatus
from cytomat_python.utils import enum_to_dict


class Cytomat:
    __serial_port: SerialPort
    plate_handler: PlateHandler
    barcode_scanner: BarcodeScanner
    maintenance_controller: MaintenanceController
    climate_controller: ClimateController
    shaker_controller: ShakerController

    def __init__(self, serial_port: Union[str, SerialPort]):
        if isinstance(serial_port, str):
            self.__serial_port = SerialPort(serial_port, timeout=1)
        else:
            self.__serial_port = serial_port

        self.plate_handler = PlateHandler(self.__serial_port)
        self.barcode_scanner = BarcodeScanner(self.__serial_port)
        self.maintenance_controller = MaintenanceController(self.__serial_port)
        self.climate_controller = ClimateController(self.__serial_port)
        self.shaker_controller = ShakerController(self.__serial_port)

    @property
    def overview_status(self) -> OverviewStatus:
        return OverviewStatus.from_hex_string(self.__serial_port.issue_status_command("ch:bs"))

    @property
    def action_status(self) -> ActionStatus:
        return ActionStatus.from_hex_string(self.__serial_port.issue_status_command("ch:ba"))

    @property
    def error_status(self) -> ErrorStatus:
        return enum_to_dict(ErrorStatus)[int(self.__serial_port.issue_status_command("ch:be"), base=16)]
    
    @property
    def warning_status(self) -> WarningStatus:
        return enum_to_dict(WarningStatus)[int(self.__serial_port.issue_status_command("ch:bw"), base=16)]

    def wait_until_not_busy(self, timeout: float, poll_delay: float = 0.5) -> OverviewStatus:
        status = self.overview_status
        end_time = datetime.now() + timedelta(seconds=timeout)
        while status.busy:
            if end_time < datetime.now():
                raise TimeoutError(f"Device still busy after {timeout} seconds")
            time.sleep(poll_delay)
            status = self.overview_status
        return status
