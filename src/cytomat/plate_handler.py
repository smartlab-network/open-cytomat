from cytomat.serial_port import SerialPort
from cytomat.status import OverviewStatus


class PlateHandler:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port

    def initialize(self) -> OverviewStatus:
        """(Re-) initialize the plate handler"""
        return self.__serial_port.issue_action_command("ll:in")

    def move_plate_from_transfer_station_to_slot(self, slot: int) -> OverviewStatus:
        """
        Move a plate from the transfer station to the given slot

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"mv:ts {slot:03}")

    def move_plate_from_slot_to_transfer_station(self, slot: int) -> OverviewStatus:
        """
        Move a plate from the given slot to the transfer station

        Parameters
        ----------
        slot
            The slot where the plate is located
        """
        return self.__serial_port.issue_action_command(f"mv:st {slot:03}")

    def move_plate_from_transfer_station_to_handler(self) -> OverviewStatus:
        """
        Move a plate from the transfer station to the plate handler shovel
        """
        return self.__serial_port.issue_action_command("mv:tw")

    def move_plate_from_handler_to_transfer_station(self) -> OverviewStatus:
        """
        Move a plate from the plate handler shovel to the transfer station
        """
        return self.__serial_port.issue_action_command("mv:wt")

    def move_plate_from_exposed_position_to_inside(self) -> OverviewStatus:
        """
        Move a plate from the exposed position (above the transfer station) to the neutral position inside the device
        """
        return self.__serial_port.issue_action_command("mv:hw")

    def move_plate_from_inside_to_exposed_position(self) -> OverviewStatus:
        """
        Move a plate from the neutral position inside the device to the exposed position (above the transfer station)
        """
        return self.__serial_port.issue_action_command("mv:wh")

    def move_plate_from_handler_to_slot(self, slot: int) -> OverviewStatus:
        """
        Move a plate from the plate handler shovel to the given slot

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"mv:ws {slot:03}")

    def move_plate_from_slot_to_handler(self, slot: int) -> OverviewStatus:
        """
        Move a plate from the given slot to the plate handler shovel

        Parameters
        ----------
        slot
            The slot where the plate is located
        """
        return self.__serial_port.issue_action_command(f"mv:sw {slot:03}")

    def move_plate_from_exposed_position_to_slot(self, slot: int) -> OverviewStatus:
        """
        Move a plate from the exposed position (above the transfer station) to the given slot

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"mv:hs {slot:03}")

    def move_plate_from_slot_to_exposed_position(self, slot: int) -> OverviewStatus:
        """
        Move a plate from the given slot to the exposed position (above the transfer station)

        Parameters
        ----------
        slot
            The slot where the plate is located
        """
        return self.__serial_port.issue_action_command(f"mv:sh {slot:03}")

    def retract_shovel(self) -> OverviewStatus:
        """
        Retract the plate handler shovel
        """
        return self.__serial_port.issue_action_command("ll:sp 001")

    def extend_shovel(self) -> OverviewStatus:
        """Extend the plate handler shovel"""
        return self.__serial_port.issue_action_command("ll:sp 002")

    def close_transfer_door(self) -> OverviewStatus:
        """Close the transfer door"""
        return self.__serial_port.issue_action_command("ll:gp 001")

    def open_transfer_door(self) -> OverviewStatus:
        """Open the transfer door"""
        return self.__serial_port.issue_action_command("ll:gp 002")

    def reset_handler_position(self) -> OverviewStatus:
        """Reset the handler to the neutral position"""
        return self.__serial_port.issue_action_command("ll:wp")

    def move_handler_below_slot_height(self, slot: int) -> OverviewStatus:
        """
        Move the handler below the given slot (only changes height, not rotation)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"ll:h- {slot:03}")

    def move_handler_above_slot_height(self, slot: int) -> OverviewStatus:
        """
        Move the handler above the given slot (only changes height, not rotation)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"ll:h+ {slot:03}")

    def rotate_handler_to_slot(self, slot: int) -> OverviewStatus:
        """
        Rotate the handler to the given slot (only changes rotation, not height)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"ll:dp {slot:03}")

    def rotate_handler_to_transfer_station(self) -> OverviewStatus:
        """
        Rotate the handler to the transfer station (only changes rotation, not height)
        """
        return self.rotate_handler_to_slot(0)

    def move_x_to_slot(self, slot: int) -> OverviewStatus:
        """
        Move along to the given slot (only moves along the x axis)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.__serial_port.issue_action_command(f"ll: {slot:03}")
