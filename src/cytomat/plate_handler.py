from zipfile import stringEndArchive

from cytomat.convert_steps import ConvertSteps as CS
from cytomat.serial_port import SerialPort
from cytomat.status import PlateShuttleSystemStatus


class PlateHandler:
    serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.serial_port = serial_port
        self.warning: bool = True

    def initialize(self) -> PlateShuttleSystemStatus:
        """(Re-) initialize the plate handler"""
        return self.serial_port.issue_action_command("ll:in")

    def move_plate_from_transfer_station_to_slot(
        self, slot: int
    ) -> PlateShuttleSystemStatus:
        """
        Move a plate from the transfer station to the given slot

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"mv:ts {slot:03}")

    def move_plate_from_slot_to_transfer_station(
        self, slot: int
    ) -> PlateShuttleSystemStatus:
        """
        Move a plate from the given slot to the transfer station

        Parameters
        ----------
        slot
            The slot where the plate is located
        """
        return self.serial_port.issue_action_command(f"mv:st {slot:03}")

    def execute_low_level(self, cmd: str) -> PlateShuttleSystemStatus:
        """
        Execute the given low-level command

        Parameters
        ----------
        cmd
            The command to be executed e.g. ll:gp 001
        """
        return self.serial_port.issue_action_command(cmd)

    def move_plate_from_transfer_station_to_handler(self) -> PlateShuttleSystemStatus:
        """
        Move a plate from the transfer station to the plate handler shovel
        """
        return self.serial_port.issue_action_command("mv:tw")

    def move_plate_from_handler_to_transfer_station(self) -> PlateShuttleSystemStatus:
        """
        Move a plate from the plate handler shovel to the transfer station
        """
        return self.serial_port.issue_action_command("mv:wt")

    def move_plate_from_exposed_position_to_inside(self) -> PlateShuttleSystemStatus:
        """
        Move a plate from the exposed position (above the transfer station) to the neutral position inside the device
        """
        return self.serial_port.issue_action_command("mv:hw")

    def move_plate_from_inside_to_exposed_position(self) -> PlateShuttleSystemStatus:
        """
        Move a plate from the neutral position inside the device to the exposed position (above the transfer station)
        """
        return self.serial_port.issue_action_command("mv:wh")

    def move_plate_from_handler_to_slot(self, slot: int) -> PlateShuttleSystemStatus:
        """
        Move a plate from the plate handler shovel to the given slot

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"mv:ws {slot:03}")

    def move_plate_from_slot_to_handler(self, slot: int) -> PlateShuttleSystemStatus:
        """
        Move a plate from the given slot to the plate handler shovel

        Parameters
        ----------
        slot
            The slot where the plate is located
        """
        return self.serial_port.issue_action_command(f"mv:sw {slot:03}")

    def move_plate_from_exposed_position_to_slot(
        self, slot: int
    ) -> PlateShuttleSystemStatus:
        """
        Move a plate from the exposed position (above the transfer station) to the given slot

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"mv:hs {slot:03}")

    def move_plate_from_slot_to_exposed_position(
        self, slot: int
    ) -> PlateShuttleSystemStatus:
        """
        Move a plate from the given slot to the exposed position (above the transfer station)

        Parameters
        ----------
        slot
            The slot where the plate is located
        """
        return self.serial_port.issue_action_command(f"mv:sh {slot:03}")

    def retract_shovel(self) -> PlateShuttleSystemStatus:
        """
        Retract the plate handler shovel
        """
        return self.serial_port.issue_action_command("ll:sp 001")

    def extend_shovel(self) -> PlateShuttleSystemStatus:
        """Extend the plate handler shovel"""
        return self.serial_port.issue_action_command("ll:sp 002")

    def close_transfer_door(self) -> PlateShuttleSystemStatus:
        """Close the transfer door"""
        return self.serial_port.issue_action_command("ll:gp 001")

    def open_transfer_door(self) -> PlateShuttleSystemStatus:
        """Open the transfer door"""
        return self.serial_port.issue_action_command("ll:gp 002")

    def reset_handler_position(self) -> PlateShuttleSystemStatus:
        """Reset the handler to the neutral position"""
        return self.serial_port.issue_action_command("ll:wp")

    def move_handler_below_slot_height(self, slot: int) -> PlateShuttleSystemStatus:
        """
        Move the handler below the given slot (only changes height, not rotation)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"ll:h- {slot:03}")

    def move_handler_above_slot_height(self, slot: int) -> PlateShuttleSystemStatus:
        """
        Move the handler above the given slot (only changes height, not rotation)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"ll:h+ {slot:03}")

    def rotate_handler_to_slot(self, slot: int) -> PlateShuttleSystemStatus:
        """
        Rotate the handler to the given slot (only changes rotation, not height)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"ll:dp {slot:03}")

    def rotate_handler_to_transfer_station(self) -> PlateShuttleSystemStatus:
        """
        Rotate the handler to the transfer station (only changes rotation, not height)
        """
        return self.rotate_handler_to_slot(0)

    def move_x_to_slot(self, slot: int) -> PlateShuttleSystemStatus:
        """
        Move along to the given slot (only moves along the x axis)

        Parameters
        ----------
        slot
            The target slot
        """
        return self.serial_port.issue_action_command(f"ll:xp {slot:03}")

    """commands to direct via absolute and relative steps.WARNING!!! 
       The following comands do not check if the handler is in a safe position.
       This can cause crashes. Make sure when entering these commands if its safe to run"""

    def warning_msg(self):
        print(
            """
    WARNING!!! This command does not check if the handler is in a safe position.
    This can cause crashes. Make sure it is safe to run."""
        )
        inp = input(
            """
            To deactivate this warning message and execute the command: press Y
            To just execute the command: press N
            To exit the script: press E"""
        )

        match inp.upper():
            case "Y":
                self.warning = False
            case "N":
                self.warning = True
            case "E":
                exit()
            case _:
                self.warning_msg()

    # lengh steps/cm ~ 172 // range of usable values: 0-24000 steps (self messured Values)
    def run_shovel_in_absolute_mm(self, mm: float) -> PlateShuttleSystemStatus:
        """
        run the shovel in absolute steps from the point zero

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_shovel(mm)
        return self.serial_port.issue_action_command(f"sb:sa {steps:05}")

    def run_shovel_in_relative_mm(self, mm: float) -> PlateShuttleSystemStatus:
        """
        run the shovel in relative steps from the current position

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_shovel(mm)
        return self.serial_port.issue_action_command(f"sb:sr {steps:05}")

    # rotation steps/deg ~ 173 // range of usable values: 0-180 deg (self measured Values)
    def run_turn_in_absolute_degrees(self, deg: float) -> PlateShuttleSystemStatus:
        """
        run turn in absolute steps from the point zero

        Parameters
        ----------
        deg
            degrees
        """
        if self.warning:
            self.warning_msg()
        steps = CS.deg_to_steps_turn(deg)
        return self.serial_port.issue_action_command(f"sb:da {steps:05}")

    def goto_lid_drop_position(self) -> PlateShuttleSystemStatus:

        self.reset_handler_position()
        self.move_x_to_slot(17)
        self.rotate_handler_to_slot(1)
        self.run_height_in_absolute_mm(26)

    def drop_lid(self) -> PlateShuttleSystemStatus:
        self.goto_lid_drop_position()
        self.run_shovel_in_absolute_mm(145)
        self.run_height_in_absolute_mm(18)

    def pick_lid(self) -> PlateShuttleSystemStatus:
        self.goto_lid_drop_position()
        self.run_height_in_absolute_mm(18)
        self.run_shovel_in_absolute_mm(150)
        self.run_height_in_absolute_mm(26)

    def run_turn_in_relative_degrees(self, deg: float) -> PlateShuttleSystemStatus:
        """
        run turn in relative steps from the current position

        Parameters
        ----------
        deg
            degrees
        """
        if self.warning:
            self.warning_msg()
        steps = CS.deg_to_steps_turn(deg)
        return self.serial_port.issue_action_command(f"sb:dr {steps:05}")

    # height steps/mm ~ 170 (self measured Values)
    def run_height_in_absolute_mm(self, mm: float) -> PlateShuttleSystemStatus:
        """
        run height in absolute steps from the point zero

        Parameters
        ----------
        mm
            millimeters
        """

        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_h(mm)
        return self.serial_port.issue_action_command(f"sb:ha {steps:05}")

    def run_height_in_relative_mm(self, mm: float) -> PlateShuttleSystemStatus:
        """
        run height in relative steps from the current position

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_h(mm)
        return self.serial_port.issue_action_command(f"sb:hr {steps:05}")

    def run_turntable_in_absolute_mm(self, mm: int) -> PlateShuttleSystemStatus:
        """
        run turntable in absolute steps from the point zero

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_turntable(mm)
        return self.serial_port.issue_action_command(f"sb:ka {steps:05}")

    def run_turntable_in_relative_mm(self, mm: int) -> PlateShuttleSystemStatus:
        """
        run turntable in relative steps from the current position

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_turntable(mm)
        return self.serial_port.issue_action_command(f"sb:kr {steps:05}")

    # width steps/mm ~ 2432 // right stacker ~ at 15500 steps, left stacker ~ at 317000 steps (self measured Values)
    def run_x_axis_in_absolute_mm(self, mm: float) -> PlateShuttleSystemStatus:
        """
        run x-axis in absolute steps from the point zero

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_x(mm)
        return self.serial_port.issue_action_command(f"sb:xa {steps:05}")

    def run_x_axis_in_relative_mm(self, mm: float) -> PlateShuttleSystemStatus:
        """
        run x-axis in relative steps from the current position

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_x(mm)
        return self.serial_port.issue_action_command(f"sb:xr {steps:05}")

    def run_transfer_station_in_absolute_mm(
        self, mm: int
    ) -> PlateShuttleSystemStatus:
        """
        run transfer station in absolute steps from the point zero

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_ts(mm)
        return self.serial_port.issue_action_command(f"sb:ta {steps:05}")

    def run_transfer_station_in_relative_mm(
        self, mm: int
    ) -> PlateShuttleSystemStatus:
        """
        run transfer station in relative steps from the current position

        Parameters
        ----------
        mm
            millimeters
        """
        if self.warning:
            self.warning_msg()
        steps = CS.mm_to_steps_ts(mm)
        return self.serial_port.issue_action_command(f"sb:tr {steps:05}")