import time
from datetime import datetime, timedelta

from cytomat.barcode_scanner import BarcodeScanner
from cytomat.climate_controller import ClimateController
from cytomat.maintenance_controller import MaintenanceController
from cytomat.plate_handler import PlateHandler
from cytomat.serial_port import SerialPort
from cytomat.shaker_controller import ShakerController
from cytomat.status import ActionStatus, ErrorStatus, OverviewStatus, WarningStatus
from cytomat.utils import enum_to_dict


class Cytomat:
    __serial_port: SerialPort

    plate_handler: PlateHandler
    """
    Exposes functionality related to plate handling
    """
    barcode_scanner: BarcodeScanner
    """
    Exposes functionality of the built-in barcode scanner
    """
    maintenance_controller: MaintenanceController
    """
    Exposes maintenance functionality
    """
    climate_controller: ClimateController
    """
    Exposes functionality related to temperature and CO2
    """
    shaker_controller: ShakerController
    """
    Exposes tower shaker functionality
    """

    def __init__(self, serial_port: str):
        self.__serial_port = SerialPort(serial_port, timeout=1)

        self.plate_handler = PlateHandler(self.__serial_port)
        self.barcode_scanner = BarcodeScanner(self.__serial_port)
        self.maintenance_controller = MaintenanceController(self.__serial_port)
        self.climate_controller = ClimateController(self.__serial_port)
        self.shaker_controller = ShakerController(self.__serial_port)

    @property
    def overview_status(self) -> OverviewStatus:
        """Status overview"""
        return OverviewStatus.from_hex_string(self.__serial_port.issue_status_command("ch:bs"))

    @property
    def action_status(self) -> ActionStatus:
        """Action status"""
        return ActionStatus.from_hex_string(self.__serial_port.issue_status_command("ch:ba"))

    @property
    def error_status(self) -> ErrorStatus:
        """Error status"""
        return enum_to_dict(ErrorStatus)[int(self.__serial_port.issue_status_command("ch:be"), base=16)]

    @property
    def warning_status(self) -> WarningStatus:
        """Warning status"""
        return enum_to_dict(WarningStatus)[int(self.__serial_port.issue_status_command("ch:bw"), base=16)]

    def wait_until_not_busy(self, timeout: float, poll_interval: float = 0.5) -> OverviewStatus:
        """
        Block the current thread until the device is not busy anymore.

        Parameters
        ----------
        timeout
            The timeout in seconds
        poll_interval
            The polling interval in seconds

        Raises
        ------
        TimeoutError
            If the device is still busy after the given timeout duration
        """
        status = self.overview_status
        end_time = datetime.now() + timedelta(seconds=timeout)
        while status.busy:
            if end_time < datetime.now():
                raise TimeoutError(f"Device still busy after {timeout} seconds")
            time.sleep(poll_interval)
            status = self.overview_status
        return status
