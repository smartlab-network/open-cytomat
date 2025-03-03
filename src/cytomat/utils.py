import json
from contextlib import contextmanager
from enum import IntEnum
from threading import Lock
from typing import Dict, Iterator, Tuple, Type, TypeVar

from .scripts.setup_cytomat import get_config_dir

GenericIntEnum = TypeVar("GenericIntEnum", bound=IntEnum)


@contextmanager
def lock_threading_lock(lock: Lock, *, timeout: float) -> Iterator[None]:
    """Context manager for using a `threading.lock` with a timeout"""
    if not timeout > 0:
        raise ValueError("Timeout must be positive")

    if not lock.acquire(timeout=timeout):
        raise TimeoutError(f"Could not acquire lock after {timeout} seconds")

    try:
        yield
    finally:
        lock.release()


def enum_to_dict(enum: Type[GenericIntEnum]) -> Dict[int, GenericIntEnum]:
    """Converts an enum class to a Dict[value, name]"""
    ret = {}
    for attr in dir(enum):
        item = getattr(enum, attr)
        if not isinstance(item, enum):
            continue
        ret[item.value] = item
    return ret


def int_to_bits(num: int, n_bits: int) -> Tuple[bool, ...]:
    """
    Convert an integer to its bit representation.

    Examples
    --------

    >>> int_to_bits(3, 2)
    (True, True)
    >>> int_to_bits(0xF1, 8)
    (True, True, True, True, False, False, False, True)
    """
    max_num_representable_by_n_bits = 2**n_bits - 1
    if num > max_num_representable_by_n_bits:
        raise ValueError(
            f"{n_bits} can only represent numbers <= {max_num_representable_by_n_bits}, got {num}"
        )
    return tuple(bool(num & (2 ** (n_bits - i - 1))) for i in range(n_bits))


def lazy_load_config_file():
    try:
        config_file = get_config_dir() / "config.json"
        with open(config_file, "r") as f:
            python_data = json.load(f)
            print("Data loaded")
            return python_data
    except Exception as e:

        print(f"Data not loaded due to: {e}")
        print(f"config file: {config_file} not found")
        return None
