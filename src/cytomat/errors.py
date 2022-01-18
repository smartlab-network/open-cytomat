from __future__ import annotations


class UnexpectedResponse(Exception):
    pass


class InvalidCommand(Exception):
    pass


class SerialCommunicationError(Exception):
    """Errors corresponding to device responses 'er XX'"""

    @staticmethod
    def from_error_code(code: int) -> SerialCommunicationError:
        error_code_mapping = {
            0x01: DeviceBusy,
            0x02: CommandUnknown,
            0x03: InvalidCommandTelegramStructure,
            0x04: WrongTelegramParameters,
            0x05: UnknownSlotNumber,
            0x11: WrongHandlerPosition,
            0x12: ShovelNotExtended,
            0x21: HandlerOccupied,
            0x22: HandlerEmpty,
            0x31: TransferStationEmpty,
            0x32: TransferStationOccupied,
            0x33: TransferStationNotInPosition,
            0x41: TransferDoorNotConfigured,
            0x42: TransferDoorNotOpen,
            0x51: InternalMemoryAccessError,
            0x52: UnauthorizedAccess,
            0x61: ShakerNotActive,
        }
        try:
            return error_code_mapping[code]()
        except KeyError:
            return UnknownErrorCode(f"Unknown hex error code: {code:x}")


class UnknownErrorCode(SerialCommunicationError):
    pass


class DeviceBusy(SerialCommunicationError):
    pass


class CommandUnknown(SerialCommunicationError):
    pass


class InvalidCommandTelegramStructure(SerialCommunicationError):
    pass


class WrongTelegramParameters(SerialCommunicationError):
    pass


class UnknownSlotNumber(SerialCommunicationError):
    pass


class WrongHandlerPosition(SerialCommunicationError):
    pass


class ShovelNotExtended(SerialCommunicationError):
    pass


class HandlerOccupied(SerialCommunicationError):
    pass


class HandlerEmpty(SerialCommunicationError):
    pass


class TransferStationEmpty(SerialCommunicationError):
    pass


class TransferStationNotInPosition(SerialCommunicationError):
    pass


class TransferDoorNotConfigured(SerialCommunicationError):
    pass


class TransferDoorNotOpen(SerialCommunicationError):
    pass


class TransferStationOccupied(SerialCommunicationError):
    pass


class InternalMemoryAccessError(SerialCommunicationError):
    pass


class UnauthorizedAccess(SerialCommunicationError):
    pass


class InvalidResponseTelegramStructure(SerialCommunicationError):
    pass


class Timeout(SerialCommunicationError):
    pass


class ShakerNotActive(SerialCommunicationError):
    pass
