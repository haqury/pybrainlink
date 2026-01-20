"""Gyroscope data models for PyBrainLink"""

from dataclasses import dataclass
from typing import Dict, Tuple
import json


@dataclass
class GyroData:
    """
    Gyroscope data from BrainLink device
    
    Attributes:
        x: Angular velocity around X axis
        y: Angular velocity around Y axis
        z: Angular velocity around Z axis
    """
    x: int = 0
    y: int = 0
    z: int = 0

    def to_dict(self) -> Dict:
        """
        Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'x': self.x,
            'y': self.y,
            'z': self.z
        }

    def to_json(self, indent: int = 2) -> str:
        """
        Convert to JSON string
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)

    def to_tuple(self) -> Tuple[int, int, int]:
        """
        Convert to tuple
        
        Returns:
            Tuple of (x, y, z)
        """
        return (self.x, self.y, self.z)

    @classmethod
    def from_tuple(cls, data: Tuple[int, int, int]) -> 'GyroData':
        """
        Create from tuple
        
        Args:
            data: Tuple of (x, y, z)
            
        Returns:
            GyroData instance
        """
        return cls(x=data[0], y=data[1], z=data[2])

    @classmethod
    def from_dict(cls, data: Dict) -> 'GyroData':
        """
        Create from dictionary
        
        Args:
            data: Dictionary with gyro data
            
        Returns:
            GyroData instance
        """
        return cls(
            x=data.get('x', 0),
            y=data.get('y', 0),
            z=data.get('z', 0)
        )
