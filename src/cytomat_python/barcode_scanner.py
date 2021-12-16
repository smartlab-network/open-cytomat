from cytomat_python.serial_port import SerialPort
from cytomat_python.status import OverviewStatus


class BarcodeScanner:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    def read_all_barcodes(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("mv:sc")

    def read_barcodes_in_range(self, start_slot: int, end_slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:sc {start_slot:03} {end_slot:03}")

    def read_barcode_20char(self, slot: int) -> str:
        return self.__serial_port.issue_status_command(f"ch:sc {slot:03}")

    def read_barcode_30char(self, slot: int) -> str:
        return self.__serial_port.issue_status_command(f"ch:sd {slot:03}")

    def abort_barcode_reading(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("rs:sc")

    @property
    def last_barcode_20char(self) -> str:
        return self.__serial_port.issue_status_command("ch:bc")

    @property
    def last_barcode_30char(self) -> str:
        return self.__serial_port.issue_status_command("ch:bd")

    def read_barcode_at_slot(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"ll:hb {slot:03}")

    def read_20char_barcode_at_current_position(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:bc")

    def read_30char_barcode_at_current_position(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:bd")
