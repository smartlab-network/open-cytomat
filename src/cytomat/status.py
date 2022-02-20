from __future__ import annotations

from enum import IntEnum
from typing import NamedTuple

from cytomat.utils import enum_to_dict, int_to_bits


class OverviewStatus(NamedTuple):
    busy: bool
    ready: bool
    warning: bool
    error: bool
    shovel_occupied: bool
    transfer_door_open: bool
    device_door_open: bool
    transfer_station_occupied: bool

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> OverviewStatus:
        """Create an instance from the hex string (e.g. ``'F1'``)"""
        return cls(*int_to_bits(int(hex_byte, base=16), n_bits=8))


class ErrorStatus(IntEnum):
    NoError = 0x00
    MotorCommunicationDisrupted = 0x01
    PlateNotMountedOnShovel = 0x02
    PlateNotDroppedFromShovel = 0x03
    ShovelNotExtended = 0x04
    ProcedureTimeout = 0x05
    TransferDoorNotOpened = 0x06
    TransferDoorNotClosed = 0x07
    ShovelNotRetracted = 0x08
    StepMotorTemperatureTooHigh = 0x0A
    OtherStepMotorError = 0x0B
    TransferStationNotRotated = 0x0C
    HeatingOrCo2CommunicationDisrupted = 0x0D
    ShakerCommunicationDisrupted = 0x0E
    ShakerConfigurationOutOfOrder = 0x0F
    ShakerNotStarted = 0x10
    ShakerClampNotOpen = 0x13
    ShakerClampNotClosed = 0x14
    Critical = 0xFF


class WarningStatus(IntEnum):
    NoWarning = 0x00
    MotorCommunicationDisrupted = 0x01
    PlateNotMountedOnShovel = 0x02
    PlateNotDroppedFromShovel = 0x03
    ShovelNotExtended = 0x04
    ProcedureTimeout = 0x05
    TransferDoorNotOpened = 0x06
    TransferDoorNotClosed = 0x07
    ShovelNotRetracted = 0x08
    InitialisingDueToOpenedDeviceDoor = 0x09
    TransferStationNotRotated = 0x0C


class ActionType(IntEnum):
    MoveHeightBelowSlot = 0x01
    CheckHeightBelowSlot = 0x02
    MoveHeightAboveSlot = 0x03
    CheckHeightAboveSlot = 0x04
    RotateToSlot = 0x05
    CheckRotation = 0x06
    ExtendShovel = 0x07
    CheckExtendedShovel = 0x08
    CheckShovelExtensionSensor = 0x09
    RetractShovel = 0x0A
    CheckRetractedShovel = 0x0B
    CloseTransferDoor = 0x0C
    CheckTransferDoorClosed = 0x0D
    OpenTransferDoor = 0x0E
    CheckTransferDoorOpened = 0x0F
    MoveSwapStationToPos1 = 0x10
    CheckSwapStationAtPos1 = 0x11
    MoveSwapStationToPos2 = 0x12
    CheckSwapStationAtPos2 = 0x13
    CheckPlateOnShovel = 0x14
    CheckPlateOnTransferStation = 0x15
    MoveToBarcodeReader = 0x16
    CheckHandlerAtBarcodeReader = 0x17
    ReadBarcode = 0x18


class ActionTarget(IntEnum):
    InitPosition = 1
    WaitPosition = 2
    Stacker = 3
    TransferStation = 4


class ActionStatus(NamedTuple):
    type: ActionType
    target: ActionTarget

    @classmethod
    def from_hex_string(cls, hex_byte: str) -> ActionStatus:
        """Create an instance from the hex string (e.g. ``'F1'``)"""
        num = int(hex_byte, base=16)
        type_ = enum_to_dict(ActionType)[(num & 0b11100000) >> 5]
        target = enum_to_dict(ActionTarget)[num & 0b00011111]
        return ActionStatus(type_, target)


class SwapStationStatus(NamedTuple):
    position1_at_door: bool
    occupied_at_door: bool
    occupied_at_user: bool

    @classmethod
    def from_response_string(cls, response: str) -> SwapStationStatus:
        """Create an instance from the response string (e.g. ``'111'``)"""
        return SwapStationStatus(
            position1_at_door=response[0] == "1",
            occupied_at_door=response[1] == "1",
            occupied_at_user=response[2] == "1",
        )
