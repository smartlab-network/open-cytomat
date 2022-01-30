from cytomat.serial_port import SerialPort


class ClimateController:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    @property
    def current_temperature(self) -> float:
        """The current temperature, in °C (read-only)"""
        return float(self.__serial_port.issue_status_command("ch:it").split()[1])

    @property
    def target_temperature(self) -> float:
        """The target temperature, in °C (can be set)"""
        return float(self.__serial_port.issue_status_command("ch:it").split()[0])

    @target_temperature.setter
    def target_temperature(self, target: float) -> None:
        if target > 100 or target < 0:
            raise ValueError("Temperature must be > 0 and < 100")
        self.__serial_port.issue_action_command(f"ll:it {target:04.1f}")

    @property
    def current_co2(self) -> float:
        """The current CO2 level (read-only)"""
        return float(self.__serial_port.issue_status_command("ch:ic").split()[1])

    @property
    def target_co2(self) -> float:
        """The target CO2 level (can be set)"""
        return float(self.__serial_port.issue_status_command("ch:ic").split()[0])

    @target_co2.setter
    def target_co2(self, target: float) -> None:
        if target > 100 or target < 0:
            raise ValueError("CO2 must be > 0 and < 100")
        self.__serial_port.issue_action_command(f"ll:ic {target:04.1f}")
