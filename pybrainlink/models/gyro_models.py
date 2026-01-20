"""Gyroscope data models for PyBrainLink"""

from dataclasses import dataclass


@dataclass
class GyroData:
    """
    Gyroscope data from BrainLink device
    
    Use `dataclasses.asdict(model)` to convert to dictionary.
    Use `json.dumps(dataclasses.asdict(model))` to convert to JSON.
    
    Attributes:
        x: Angular velocity around X axis
        y: Angular velocity around Y axis
        z: Angular velocity around Z axis
    """
    x: int = 0
    y: int = 0
    z: int = 0
