from cytomat.serial_port import SerialPort
from cytomat.status import OverviewStatus


class BarcodeScanner:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    def read_all_barcodes(self) -> OverviewStatus:
        """
        Real all barcodes

        Returns
        -------
        The overview status after command submission
        """
        return self.__serial_port.issue_action_command("mv:sc")

    def read_barcodes_in_range(self, start_slot: int, end_slot: int) -> OverviewStatus:
        """
        Read all barcodes in the given range

        Parameters
        ----------
        start_slot
            The start slot
        end_slot
            The end slot

        Returns
        -------
        The overview status after command submission
        """
        return self.__serial_port.issue_action_command(f"mv:sc {start_slot:03} {end_slot:03}")

    def get_barcode_20char(self, slot: int) -> str:
        """
        Get the barcode at the given slot (for short barcodes)

        Parameters
        ----------
        slot
            The slot number

        Returns
        -------
        The barcode
        """
        return self.__serial_port.issue_status_command(f"ch:sc {slot:03}")

    def get_barcode_30char(self, slot: int) -> str:
        """
        Get the barcode at the given slot (for long barcodes)

        Parameters
        ----------
        slot
            The slot number

        Returns
        -------
        The barcode
        """
        return self.__serial_port.issue_status_command(f"ch:sd {slot:03}")

    def abort_barcode_reading(self) -> OverviewStatus:
        """
        Abort barcode reading

        Returns
        -------
        The overview status after command submission
        """
        return self.__serial_port.issue_action_command("rs:sc")

    @property
    def last_barcode_20char(self) -> str:
        """
        The last read barcode (for short barcodes)

        Returns
        -------
        The last barcode
        """
        return self.__serial_port.issue_status_command("ch:bc")

    @property
    def last_barcode_30char(self) -> str:
        """
        The last read barcode (for short barcodes)

        Returns
        -------
        The last barcode
        """
        return self.__serial_port.issue_status_command("ch:bd")

    def read_barcode_at_slot(self, slot: int) -> OverviewStatus:
        """
        Read the barcode at the given slot

        Parameters
        ----------
        slot
            The slot number

        Returns
        -------
        The overview status after command submission
        """
        return self.__serial_port.issue_action_command(f"ll:hb {slot:03}")

    def read_20char_barcode_at_current_position(self) -> OverviewStatus:
        """
        Read the barcode at the current position (for short barcodes)

        Returns
        -------
        The overview status after command submission
        """
        return self.__serial_port.issue_action_command("ll:bc")

    def read_30char_barcode_at_current_position(self) -> OverviewStatus:
        """
        Read the barcode at the current position (for long barcodes)

        Returns
        -------
        The overview status after command submission
        """
        return self.__serial_port.issue_action_command("ll:bd")
