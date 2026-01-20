"""EEG data models for PyBrainLink"""

from dataclasses import dataclass


@dataclass
class BrainLinkModel:
    """
    Model for BrainLink EEG data
    
    Use `dataclasses.asdict(model)` to convert to dictionary.
    Use `json.dumps(dataclasses.asdict(model))` to convert to JSON.
    
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


@dataclass
class BrainLinkExtendModel:
    """
    Extended BrainLink data model
    
    Use `dataclasses.asdict(model)` to convert to dictionary.
    Use `json.dumps(dataclasses.asdict(model))` to convert to JSON.
    
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
