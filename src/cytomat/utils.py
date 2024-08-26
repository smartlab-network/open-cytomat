from contextlib import contextmanager
from enum import IntEnum
from threading import Lock
from typing import Dict, Iterator, Tuple, Type, TypeVar
from cytomat import parameters
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
        raise ValueError(f"{n_bits} can only represent numbers <= {max_num_representable_by_n_bits}, got {num}")
    return tuple(bool(num & (2 ** (n_bits - i - 1))) for i in range(n_bits))

class ConvertSteps():
    def mm_to_steps_x(mm: float)-> int:
        return round(parameters.steps_per_mm_x * mm)
    
    def steps_to_mm_x(steps: int)-> float:
        return round(1/(parameters.steps_per_mm_x / steps), 4)
    
    def mm_to_steps_h(mm: float)-> int:
        return round(parameters.steps_per_mm_h * mm)
    
    def steps_to_mm_h(steps: int)-> float:
        return round(1/(parameters.steps_per_mm_h / steps),4)
    
    def mm_to_steps_shovel(mm: float)-> int:
        return round(parameters.steps_per_mm_shovel * mm)
    
    def steps_to_mm_shovel(steps: int)-> float:
        return round(1/(parameters.steps_per_mm_shovel / steps),4)
    
    def deg_to_steps_turn(deg: float)-> int:
        return round(parameters.steps_per_deg_turn * deg)
    
    def steps_to_deg_turn(steps: int)-> float:
        return round(1/(parameters.steps_per_deg_turn / steps),4)