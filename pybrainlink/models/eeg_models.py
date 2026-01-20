"""EEG data models for PyBrainLink"""

from dataclasses import dataclass
from typing import Dict
import json


@dataclass
class BrainLinkModel:
    """
    Model for BrainLink EEG data
    
    Attributes:
        attention: Attention level (0-100)
        meditation: Meditation level (0-100)
        signal: Signal quality
        delta: Delta waves (0.5-4 Hz) - Deep sleep
        theta: Theta waves (4-8 Hz) - Meditation, sleep
        low_alpha: Low Alpha waves (8-10 Hz) - Relaxation
        high_alpha: High Alpha waves (10-12 Hz) - Wakeful rest
        low_beta: Low Beta waves (12-18 Hz) - Active thinking
        high_beta: High Beta waves (18-30 Hz) - Concentration
        low_gamma: Low Gamma waves (30-50 Hz) - Information processing
        high_gamma: High Gamma waves (50+ Hz) - Cognition
    """
    attention: int = 0
    meditation: int = 0
    signal: int = 0
    delta: int = 0
    theta: int = 0
    low_alpha: int = 0
    high_alpha: int = 0
    low_beta: int = 0
    high_beta: int = 0
    low_gamma: int = 0
    high_gamma: int = 0

    def to_dict(self) -> Dict:
        """
        Convert to dictionary
        
        Returns:
            Dictionary representation of EEG data
        """
        return {
            'attention': self.attention,
            'meditation': self.meditation,
            'signal': self.signal,
            'delta': self.delta,
            'theta': self.theta,
            'low_alpha': self.low_alpha,
            'high_alpha': self.high_alpha,
            'low_beta': self.low_beta,
            'high_beta': self.high_beta,
            'low_gamma': self.low_gamma,
            'high_gamma': self.high_gamma
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

    @classmethod
    def from_dict(cls, data: Dict) -> 'BrainLinkModel':
        """
        Create from dictionary
        
        Args:
            data: Dictionary with EEG data
            
        Returns:
            BrainLinkModel instance
        """
        return cls(
            attention=data.get('attention', 0),
            meditation=data.get('meditation', 0),
            signal=data.get('signal', 0),
            delta=data.get('delta', 0),
            theta=data.get('theta', 0),
            low_alpha=data.get('low_alpha', 0),
            high_alpha=data.get('high_alpha', 0),
            low_beta=data.get('low_beta', 0),
            high_beta=data.get('high_beta', 0),
            low_gamma=data.get('low_gamma', 0),
            high_gamma=data.get('high_gamma', 0)
        )

    @classmethod
    def from_json(cls, json_str: str) -> 'BrainLinkModel':
        """
        Create from JSON string
        
        Args:
            json_str: JSON string with EEG data
            
        Returns:
            BrainLinkModel instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)


@dataclass
class BrainLinkExtendModel:
    """
    Extended BrainLink data model
    
    Attributes:
        ap: Access point strength
        electric: Battery level (0-100%)
        version: Device firmware version
        temperature: Device temperature (°C)
        heart_rate: Heart rate (BPM)
    """
    ap: int = 0
    electric: int = 0
    version: str = ""
    temperature: float = 0.0
    heart_rate: int = 0

    def to_dict(self) -> Dict:
        """
        Convert to dictionary
        
        Returns:
            Dictionary representation
        """
        return {
            'ap': self.ap,
            'electric': self.electric,
            'version': self.version,
            'temperature': self.temperature,
            'heart_rate': self.heart_rate
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

    @classmethod
    def from_dict(cls, data: Dict) -> 'BrainLinkExtendModel':
        """
        Create from dictionary
        
        Args:
            data: Dictionary with extended data
            
        Returns:
            BrainLinkExtendModel instance
        """
        return cls(
            ap=data.get('ap', 0),
            electric=data.get('electric', 0),
            version=data.get('version', ''),
            temperature=data.get('temperature', 0.0),
            heart_rate=data.get('heart_rate', 0)
        )
