from cytomat_python.serial_port import SerialPort
from cytomat_python.status import OverviewStatus


class PlateHandler:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    def initialize(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:in")

    def move_plate_from_transfer_station_to_slot(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:ts {slot:03}")

    def move_plate_from_slot_to_transfer_station(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:st {slot:03}")

    def move_plate_from_transfer_station_to_handler(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("mv:tw")

    def move_plate_from_handler_to_transfer_station(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("mv:wt")

    def move_plate_from_exposed_position_to_inside(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("mv:hw")

    def move_plate_from_inside_to_exposed_position(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("mv:wh")

    def move_plate_from_handler_to_slot(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:ws {slot:03}")

    def move_plate_from_slot_to_handler(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:sw {slot:03}")

    def move_plate_from_exposed_position_to_slot(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:hs {slot:03}")

    def move_plate_from_slot_to_exposed_position(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"mv:sh {slot:03}")

    def retract_shovel(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:sp 001")

    def extend_shovel(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:sp 002")

    def close_transfer_door(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:gp 001")

    def open_transfer_door(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:gp 002")

    def reset_handler_position(self) -> OverviewStatus:
        return self.__serial_port.issue_action_command("ll:wp")

    def move_handler_below_slot_height(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"ll:h- {slot:03}")

    def move_handler_above_slot_height(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"ll:h+ {slot:03}")

    def rotate_handler_to_slot(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"ll:dp {slot:03}")

    def rotate_handler_to_transfer_station(self) -> OverviewStatus:
        return self.rotate_handler_to_slot(0)

    def move_x_to_slot(self, slot: int) -> OverviewStatus:
        return self.__serial_port.issue_action_command(f"ll: {slot:03}")
