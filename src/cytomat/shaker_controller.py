from cytomat.serial_port import SerialPort
from cytomat.status import OverviewStatus


class ShakerController:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    def get_shaker_frequency(self, shaker: int) -> int:
        """
        Get the frequency of the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)

        Returns
        -------
        The shaker frequency
        """
        self.__check_shaker_id(shaker)
        return int(self.__serial_port.issue_status_command(f"ch:pb {shaker + 19}"))

    def set_shaker_frequency(self, shaker: int, frequency: int) -> OverviewStatus:
        """
        Set the frequency of the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)
        frequency
            The target frequency
        """
        self.__check_shaker_id(shaker)
        return self.__serial_port.issue_action_command(f"se:pb {shaker + 19} {frequency:04}")

    def initialize_shakers(self) -> OverviewStatus:
        """Initialize the shakers"""
        return self.__serial_port.issue_action_command("ll:vi")

    def start_all_shakers(self) -> OverviewStatus:
        """Start all shakers"""
        return self.__serial_port.issue_action_command("ll:va")

    def start_shaker(self, shaker: int) -> OverviewStatus:
        """
        Start the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)
        """
        self.__check_shaker_id(shaker)
        return self.__serial_port.issue_action_command(f"ll:va {shaker:03}")

    def stop_all_shakers(self) -> OverviewStatus:
        """Stop all shakers"""
        return self.__serial_port.issue_action_command("ll:vd")

    def stop_shaker(self, shaker: int) -> OverviewStatus:
        """
        Stop the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)
        """
        self.__check_shaker_id(shaker)
        return self.__serial_port.issue_action_command(f"ll:vd {shaker:03}")

    @staticmethod
    def __check_shaker_id(shaker: int) -> None:
        if shaker not in (1, 2):
            raise ValueError("Invalid shaker, must be 1 or 2")
