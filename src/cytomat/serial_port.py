import logging
import re
from threading import Lock

from serial import Serial
from serial.serialutil import PARITY_NONE, SerialException
from serial.tools import list_ports

from cytomat.errors import InvalidCommand, SerialCommunicationError, UnexpectedResponse
from cytomat.status import PlateShuttleSystemStatus
from cytomat.utils import lock_threading_lock

logger = logging.getLogger(__name__)


def usable_serial_ports(*, timeout: float = 1.0) -> list[str]:
    usable_ports: list[str] = []
    for port in list_ports.comports():
        logger.debug(f"Checking serial port candidate: {port.device}")
        try:
            serial_port = SerialPort(port.device, timeout=timeout)
        except (SerialException, PermissionError) as exc:
            logger.debug(f"Skipping serial port {port.device}: {exc}")
            continue

        serial_port.close()
        usable_ports.append(port.device)

    if usable_ports:
        logger.info(f"Usable serial ports: {', '.join(usable_ports)}")
    else:
        logger.debug("No usable serial ports found")

    return usable_ports


def first_usable_serial_port(*, timeout: float = 1.0) -> str | None:
    ports = usable_serial_ports(timeout=timeout)
    return ports[0] if ports else None


class SerialPort:
    port: Serial
    lock: Lock
    timeout: float

    def __init__(self, port: str, *, timeout: float) -> None:
        """
        Wraps a plain serial connection to simplify communication with Cytomat devices

        Parameters
        ----------
        port : str
            The address of the port (e.g. "COM3" on Windows or "/dev/ttyACM0" on Unix)
        timeout: float, seconds
            A :class:`TimeoutError` is raised when read or write operations
            take longer than this duration
        """
        self.port = Serial(
            port,
            baudrate=9600,
            bytesize=8,
            stopbits=1,
            parity=PARITY_NONE,
            timeout=timeout,
            write_timeout=timeout,
        )
        self.lock = Lock()
        self.timeout = timeout

    def close(self) -> None:
        self.port.close()

    def open(self) -> None:
        self.port.open()

    def communicate(self, command: str) -> str:
        """
        Send a command to the port and return the response string

        Parameters
        ----------
        command: str
            The command to send

        Returns
        -------
        str
            The response

        Raises
        ------
        TimeoutError
            If a read or write operation took too long
        SerialCommunicationError
            If there were unread bytes in the input buffer before sending the command
        """
        with lock_threading_lock(self.lock, timeout=self.timeout):
            if self.port.in_waiting:
                raise SerialCommunicationError(
                    "There were unread bytes in the input buffer"
                )

            raw_command: bytes = command.encode("ascii") + b"\r"
            raw_response: bytes = b""
            self.port.write(raw_command)
            while not raw_response.endswith(b"\r"):
                char = self.port.read()
                raw_response += char
                if not char:
                    raise TimeoutError(
                        "Query: "
                        f"{command}, "
                        "Error: captured "
                        f"{char!r} as the last character of "
                        f"{raw_response!r}."
                    )

        response: str = raw_response[:-1].decode("ascii")
        return response

    @staticmethod
    def check_prefix_and_strip(response: str, expected_prefix: str) -> str:
        """
        Check if the response has the expected prefix, strip the prefix and whitespace

        Parameters
        ----------
        response: str
            A response as sent by the device
        expected_prefix: str
            The expected prefix

        Returns
        -------
        str
            The response without the prefix and surrounding whitespace

        Raises
        ------
        UnexpectedResponse
            If the prefix did not match
        """
        if response.startswith(expected_prefix):
            return response[len(expected_prefix) :].strip()
        raise UnexpectedResponse(
            f"Expected response prefix '{expected_prefix}', got response '{response}'"
        )

    def issue_action_command(self, command: str) -> PlateShuttleSystemStatus:
        """
        Issue a command which results in 'ok XX' or 'er XX'.

        Parameters
        ----------
        command: str
            The command

        Returns
        -------
        PlateShuttleSystemStatus
            The current device status, as given by the response 'ok XX'

        Raises
        ------
        SerialCommunicationError
            If the response was 'er XX'
        UnexpectedResponse
            If the response did not match 'ok XX' or 'er XX'
        """
        response = self.communicate(command)

        if response.startswith("ok"):
            return PlateShuttleSystemStatus.from_hex_string(
                self.check_prefix_and_strip(response, "ok")
            )
        if response.startswith("er"):
            raise SerialCommunicationError.from_error_code(
                int(self.check_prefix_and_strip(response, "er"), base=16)
            )
        raise UnexpectedResponse(
            f"Expected response like 'ok XX' or 'er XX', got '{response}'"
        )

    def issue_status_command(self, command: str) -> str:
        """
        Issue a status command in the form of 'ch:xx' or 'ch:xx ...',
        which results in responses like 'xx ...'.
        Returns the response without the prefix

        Parameters
        ----------
        command: str
            The command

        Returns
        -------
        str
            The response without the prefix

        Raises
        ------
        InvalidCommand
            If the command did not match 'ch:xx' or 'ch:xx ...'

        Examples
        --------
        >>> self.issue_action_command("ch:bs")
        '01'  # full response was 'bs 01'
        """
        if not re.fullmatch("ch:[a-z]{2}.*", command):
            raise InvalidCommand(
                f"Expected command like 'ch:xx' or 'ch:xx ...', got '{command}'"
            )

        try:
            response = self.check_prefix_and_strip(
                self.communicate(command), expected_prefix=command[3:5]
            )
        except UnexpectedResponse as e:
            print(f"Unexpected response while checking status: {e}. Trying again.")
            response = self.check_prefix_and_strip(
                self.communicate(command), expected_prefix=command[3:5]
            )

        return response
