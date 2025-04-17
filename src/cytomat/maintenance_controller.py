from cytomat.serial_port import SerialPort
from cytomat.status import PlateShuttleSystemStatus


class MaintenanceController:
    serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.serial_port = serial_port

    def reset_error_status(self) -> PlateShuttleSystemStatus:
        """Reset the error status"""
        return self.serial_port.issue_action_command("rs:be")

    def restart_device(self) -> PlateShuttleSystemStatus:
        """Restart the device"""
        return self.serial_port.issue_action_command("se:ns")

    def set_pitch(self, stacker: int, pitch: int) -> PlateShuttleSystemStatus:
        """
        Set the pitch of the given stacker

        Parameters
        ----------
        stacker
            The stacker index (1-based)
        pitch
            The pitch (in steps)
        """
        return self.serial_port.issue_action_command(f"se:cs {stacker:03} {pitch:03}")

    def send_barcode_scanner_data_via_rs232(self) -> PlateShuttleSystemStatus:
        """Send barcode scanner data via the RS-232 interface"""
        return self.serial_port.issue_action_command("se:c1")

    def send_temperate_co2_via_rs232(self) -> PlateShuttleSystemStatus:
        """Send barcode scanner data via the RS-232 interface"""
        return self.serial_port.issue_action_command("se:c2")
