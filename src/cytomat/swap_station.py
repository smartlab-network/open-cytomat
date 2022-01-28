from cytomat.serial_port import SerialPort
from cytomat.status import OverviewStatus, SwapStationStatus


class SwapStation:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    @property
    def status(self) -> SwapStationStatus:
        """The swap station status"""
        return SwapStationStatus.from_response_string(self.__serial_port.issue_status_command("ch:sw"))

    def rotate_to_position_1(self) -> OverviewStatus:
        """Rotate to position 1"""
        return self.__serial_port.issue_action_command("ll:tp 001")

    def rotate_to_position_2(self) -> OverviewStatus:
        """Rotate to position 2"""
        return self.__serial_port.issue_action_command("ll:tp 002")
