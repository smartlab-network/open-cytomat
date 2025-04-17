from cytomat.serial_port import SerialPort
from cytomat.status import PlateShuttleSystemStatus


class ShakerController:
    serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.serial_port = serial_port

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
        self.check_shaker_id(shaker)
        return int(self.serial_port.issue_status_command(f"ch:pb {shaker + 19}"))

    def set_shaker_frequency(
        self, shaker: int, frequency: int
    ) -> PlateShuttleSystemStatus:
        """
        Set the frequency of the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)
        frequency
            The target frequency
        """
        self.check_shaker_id(shaker)
        return self.serial_port.issue_action_command(
            f"se:pb {shaker + 19} {frequency:04}"
        )

    def initialize_shakers(self) -> PlateShuttleSystemStatus:
        """Initialize the shakers"""
        return self.serial_port.issue_action_command("ll:vi")

    def start_all_shakers(self) -> PlateShuttleSystemStatus:
        """Start all shakers"""
        return self.serial_port.issue_action_command("ll:va")

    def start_shaker(self, shaker: int) -> PlateShuttleSystemStatus:
        """
        Start the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)
        """
        self.check_shaker_id(shaker)
        return self.serial_port.issue_action_command(f"ll:va {shaker:03}")

    def stop_all_shakers(self) -> PlateShuttleSystemStatus:
        """Stop all shakers"""
        return self.serial_port.issue_action_command("ll:vd")

    def stop_shaker(self, shaker: int) -> PlateShuttleSystemStatus:
        """
        Stop the given shaker

        Parameters
        ----------
        shaker
            The shaker number (1-based)
        """
        self.check_shaker_id(shaker)
        return self.serial_port.issue_action_command(f"ll:vd {shaker:03}")

    @staticmethod
    def check_shaker_id(shaker: int) -> None:
        if shaker not in (1, 2):
            raise ValueError("Invalid shaker, must be 1 or 2")
