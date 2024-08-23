from cytomat.serial_port import SerialPort
from cytomat.status import OverviewStatus


class PlateHandler:
    __serial_port: SerialPort

    def __init__(self, serial_port: SerialPort) -> None:
        self.__serial_port = serial_port
        self.warning: bool = True

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
        return self.__serial_port.issue_action_command(f"ll:xp {slot:03}")
    

    """commands to direct via absolute and relative steps.WARNING!!! 
       The following comands do not check if the handler is in a safe position.
       This can cause crashes. Make sure when entering these commands if its safe to run"""
       
    def warning_msg(self):
            print("""
    WARNING!!! This command does not check if the handler is in a safe position.
    This can cause crashes. Make sure it is safe to run.""")
            inp = int(input("""
            To deactivate this warning message and execute the command: press 0
            To just execute the command: press 1
            To exit the script: press 2"""))
        
            match inp:
                case 0:
                    self.warning = False
                case 1:
                    self.warning = True
                case 2:
                    exit()
                case _:
                    self.warning_msg()
                    
    #lengh steps/cm ~ 1727 // range of usable values: 0-24000 steps
    def run_shovel_in_absolute_steps(self, steps:int) -> OverviewStatus:
        """
        run the shovel in absolute steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:sa {steps:05}")
    
    def run_shovel_in_relative_steps(self, steps:int) -> OverviewStatus:
        """
        run the shovel in relative steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:sr {steps:05}")
    
    #rotation steps/deg ~ 173 // range of usable values: 0-180 deg
    def run_turn_in_absolute_steps(self, steps:int) -> OverviewStatus:
        """ 
        run turn in absolute steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:da {steps:05}")
    
    def run_turn_in_relative_steps(self, steps:int) -> OverviewStatus:
        """ 
        run turn in relative steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:dr {steps:05}")
    
    #height steps/cm ~ 1700 
    def run_height_in_absolute_steps(self, steps:int) -> OverviewStatus:
        """ 
        run height in absolute steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:ha {steps:05}")

    def run_height_in_relative_steps(self, steps:int) -> OverviewStatus:
        """ 
        run height in relative steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:hr {steps:05}")
    
    def run_turntable_in_absolute_steps(self, steps:int) -> OverviewStatus:
        """ 
        run turntable in absolute steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:ka {steps:05}")
    
    def run_turntable_in_relative_steps(self, steps:int) -> OverviewStatus:
        """ 
        run turntable in relative steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:kr {steps:05}")
   
    #widh steps/cm ~ 24315 // right stacker ~ 15500 steps, left stacker ~ 317000 steps
    def run_x_axis_in_absolute_steps(self, steps:int) -> OverviewStatus:
        """ 
        run x-axis in absolute steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:xa {steps:05}")
    
    def run_x_axis_in_relative_steps(self, steps:int) -> OverviewStatus:
        """ 
        run x-axis in relative steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:xr {steps:05}")
    
    def run_transfer_station_in_absolute_steps(self, steps:int) -> OverviewStatus:
        """ 
        run transfer statiom in absolute steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:ta {steps:05}")
    
    def run_transfer_station_in_relative_steps(self, steps:int) -> OverviewStatus:
        """ 
        run transfer statiom in relative steps from the point zero
        
        Parameters
        ----------
        steps
            Motor Steps xxxxx
        """
        if self.warning:
            self.warning_msg
        return self.__serial_port.issue_action_command(f"sb:tr {steps:05}")