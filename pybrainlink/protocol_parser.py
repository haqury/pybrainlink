"""Parser for BrainLink Bluetooth protocol"""

from typing import Optional, Tuple
from .models import BrainLinkModel


class BrainLinkProtocolParser:
    """
    Parser for BrainLink device protocol
    
    Parses raw Bluetooth data packets into structured EEG and Gyroscope data.
    
    Example:
        >>> parser = BrainLinkProtocolParser()
        >>> eeg_data, gyro_data = parser.parse_data(raw_bytes)
        >>> if eeg_data:
        >>>     print(f"Attention: {eeg_data.attention}")
    """
    
    HEADER = bytes([0xAA, 0xAA])
    SEPARATOR = bytes([0x23, 0x23])
    
    # Packet types
    TYPE_SHORT = bytes([0x04, 0x80, 0x02])
    TYPE_LONG_EEG = bytes([0x20, 0x02])
    TYPE_GYRO = bytes([0x07, 0x03])
    TYPE_EXTEND = bytes([0xBB, 0x0C, 0x02])
    
    def __init__(self, debug: bool = False):
        """
        Initialize parser
        
        Args:
            debug: Enable debug output
        """
        self.buffer = bytearray()
        self.debug = debug
    
    def parse_data(self, data: bytearray) -> Tuple[Optional[BrainLinkModel], Optional[Tuple[int, int, int]]]:
        """
        Parse incoming data from BrainLink device
        
        Args:
            data: Raw bytes from device
            
        Returns:
            Tuple of (EEG data, Gyro data) - either can be None if not found
        """
        self.buffer.extend(data)
        
        eeg_data = None
        gyro_data = None
        
        # Look for long EEG packets (type 0x2002)
        eeg_data = self._parse_eeg_packet()
        
        # Look for gyro packets (type 0x0703)
        gyro_data = self._parse_gyro_packet()
        
        # Keep only recent data in buffer (last 2000 bytes)
        if len(self.buffer) > 2000:
            self.buffer = self.buffer[-2000:]
        
        return eeg_data, gyro_data
    
    def _parse_eeg_packet(self) -> Optional[BrainLinkModel]:
        """Parse EEG data packet from buffer"""
        idx = 0
        while idx < len(self.buffer) - 60:
            # Look for AAAA 2002 pattern
            if (idx + 5 < len(self.buffer) and 
                self.buffer[idx] == 0xAA and 
                self.buffer[idx+1] == 0xAA and
                self.buffer[idx+2] == 0x20 and
                self.buffer[idx+3] == 0x02):
                
                try:
                    packet_start = idx + 4
                    
                    if packet_start + 50 <= len(self.buffer):
                        data = self.buffer[packet_start:packet_start + 50]
                        
                        # Extract values
                        attention = data[2]
                        meditation = data[4] if len(data) > 4 else 0
                        
                        # Wave data in big-endian format (3 bytes each)
                        delta = int.from_bytes(data[6:9], 'big') if len(data) > 8 else 0
                        theta = int.from_bytes(data[9:12], 'big') if len(data) > 11 else 0
                        low_alpha = int.from_bytes(data[12:15], 'big') if len(data) > 14 else 0
                        high_alpha = int.from_bytes(data[15:18], 'big') if len(data) > 17 else 0
                        low_beta = int.from_bytes(data[18:21], 'big') if len(data) > 20 else 0
                        high_beta = int.from_bytes(data[21:24], 'big') if len(data) > 23 else 0
                        low_gamma = int.from_bytes(data[24:27], 'big') if len(data) > 26 else 0
                        high_gamma = int.from_bytes(data[27:30], 'big') if len(data) > 29 else 0
                        
                        model = BrainLinkModel(
                            attention=attention,
                            meditation=meditation,
                            delta=delta,
                            theta=theta,
                            low_alpha=low_alpha,
                            high_alpha=high_alpha,
                            low_beta=low_beta,
                            high_beta=high_beta,
                            low_gamma=low_gamma,
                            high_gamma=high_gamma
                        )
                        
                        if self.debug:
                            print(f"\n✅ EEG Data Parsed:")
                            print(f"   Attention: {attention}, Meditation: {meditation}")
                            print(f"   Delta: {delta}, Theta: {theta}")
                            print(f"   Low Alpha: {low_alpha}, High Alpha: {high_alpha}")
                            print(f"   Low Beta: {low_beta}, High Beta: {high_beta}")
                            print(f"   Low Gamma: {low_gamma}, High Gamma: {high_gamma}\n")
                        
                        return model
                        
                except Exception as e:
                    if self.debug:
                        print(f"Error parsing EEG packet: {e}")
            
            idx += 1
        
        return None
    
    def _parse_gyro_packet(self) -> Optional[Tuple[int, int, int]]:
        """Parse gyro data packet from buffer"""
        idx = 0
        while idx < len(self.buffer) - 15:
            if (idx + 10 < len(self.buffer) and
                self.buffer[idx] == 0xAA and
                self.buffer[idx+1] == 0xAA and
                self.buffer[idx+2] == 0x07 and
                self.buffer[idx+3] == 0x03):
                
                try:
                    # Gyro data in signed big-endian format
                    x = int.from_bytes(self.buffer[idx+4:idx+6], 'big', signed=True)
                    y = int.from_bytes(self.buffer[idx+6:idx+8], 'big', signed=True)
                    z = int.from_bytes(self.buffer[idx+8:idx+10], 'big', signed=True)
                    
                    if self.debug:
                        print(f"✅ Gyro Data: X={x}, Y={y}, Z={z}")
                    
                    return (x, y, z)
                except:
                    pass
            
            idx += 1
        
        return None
