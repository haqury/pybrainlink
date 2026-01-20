"""Parser for BrainLink Bluetooth protocol using State Machine"""

from enum import Enum
from typing import Optional, Tuple, Callable
from .models import BrainLinkModel, BrainLinkExtendModel


class ParserState(Enum):
    """Parser state machine states"""
    SYNC = 1
    SYNC_CHECK = 2
    PAYLOAD_LENGTH = 3
    PAYLOAD = 4
    PAYLOAD_CONTINUE = 5
    RAW_PAYLOAD = 6
    EXTEND_PAYLOAD = 7
    GYRO_PAYLOAD = 8
    HRV_LENGTH = 9
    HRV_PAYLOAD = 10


class BrainLinkProtocolParser:
    """
    State Machine parser for BrainLink device protocol
    
    This parser processes data byte-by-byte using a state machine,
    identical to the C# SDK implementation for maximum reliability.
    
    Example:
        >>> parser = BrainLinkProtocolParser()
        >>> eeg_data, gyro_data, extend_data = parser.parse_data(raw_bytes)
        >>> if eeg_data:
        >>>     print(f"Attention: {eeg_data.attention}")
    """
    
    # Protocol constants (from C# SDK)
    SYNC_BYTE = 0xAA  # 170
    SYNC_HRV_BYTE = 0xBB  # 187
    PAYLOAD_LENGTH_BYTE = 0x20  # 32 - EEG data
    RAW_LENGTH_BYTE = 0x04  # 4 - Raw data
    GYRO_LENGTH_BYTE = 0x07  # 7 - Gyro data
    SIGNAL_CHECK_BYTE = 0x02
    EEG_CHECK_BYTE = 0x83  # 131
    EEG_LENGTH_BYTE = 0x18  # 24
    ATT_CHECK_BYTE = 0x04
    MED_CHECK_BYTE = 0x05
    AP_CHECK_BYTE = 0x06
    POWER_CHECK_BYTE = 0x07
    FIXED_CHECK_BYTE = 0x08
    FLAG_CHECK_BYTE = 0x55  # 85
    FRAME_TAIL_BYTE = 0x23  # 35
    EXTEND_LENGTH_BYTE = 0x0C  # 12
    HRV_LENGTH_BYTE = 0x0C  # 12
    
    def __init__(self, debug: bool = False):
        """
        Initialize state machine parser
        
        Args:
            debug: Enable debug output
        """
        self.state = ParserState.SYNC
        self.payload = bytearray(128)  # Payload buffer
        self.offset = 0  # Current offset in payload
        self.checksum = 0
        self.debug = debug
        
        # Callbacks (will be set externally)
        self.on_eeg_data: Optional[Callable[[BrainLinkModel], None]] = None
        self.on_extend_data: Optional[Callable[[BrainLinkExtendModel], None]] = None
        self.on_gyro_data: Optional[Callable[[int, int, int], None]] = None
        self.on_raw_data: Optional[Callable[[int], None]] = None
        self.on_hrv_data: Optional[Callable[[list, int], None]] = None
        
        # Last parsed data (for compatibility)
        self._last_eeg: Optional[BrainLinkModel] = None
        self._last_gyro: Optional[Tuple[int, int, int]] = None
        self._last_extend: Optional[BrainLinkExtendModel] = None
    
    def parse_data(self, data: bytearray) -> Tuple[Optional[BrainLinkModel], Optional[Tuple[int, int, int]], Optional[BrainLinkExtendModel]]:
        """
        Parse incoming data from BrainLink device
        
        Args:
            data: Raw bytes from device
            
        Returns:
            Tuple of (EEG data, Gyro data, Extended data) - any can be None if not found
        """
        # Reset last parsed data
        self._last_eeg = None
        self._last_gyro = None
        self._last_extend = None
        
        # Process each byte through state machine
        for byte in data:
            self._parse_byte(byte)
        
        return self._last_eeg, self._last_gyro, self._last_extend
    
    def _parse_byte(self, byte: int):
        """Process a single byte through the state machine"""
        
        if self.state == ParserState.SYNC:
            # Looking for first sync byte (0xAA)
            if byte == self.SYNC_BYTE:
                self.state = ParserState.SYNC_CHECK
        
        elif self.state == ParserState.SYNC_CHECK:
            # Check second sync byte
            if byte == self.SYNC_BYTE:
                # Standard packet (0xAA 0xAA)
                self.state = ParserState.PAYLOAD_LENGTH
            elif byte == self.SYNC_HRV_BYTE:
                # HRV packet (0xAA 0xBB)
                self.state = ParserState.HRV_LENGTH
            else:
                # Not a valid header, back to sync
                self.state = ParserState.SYNC
        
        elif self.state == ParserState.PAYLOAD_LENGTH:
            # Determine packet type by length byte
            self.offset = 0
            
            if byte == self.PAYLOAD_LENGTH_BYTE:  # 0x20 - EEG
                self.state = ParserState.PAYLOAD
            elif byte == self.RAW_LENGTH_BYTE:  # 0x04 - Raw
                self.state = ParserState.RAW_PAYLOAD
            elif byte == self.GYRO_LENGTH_BYTE:  # 0x07 - Gyro
                self.state = ParserState.GYRO_PAYLOAD
            else:
                # Unknown packet type
                self.state = ParserState.SYNC
        
        elif self.state == ParserState.PAYLOAD:
            # Collecting EEG payload (32 bytes + checksum)
            self.payload[self.offset] = byte
            self.offset += 1
            
            if self.offset > 32:
                # Got all payload + checksum
                self.state = ParserState.PAYLOAD_CONTINUE
                self.checksum = byte
                self._parse_eeg_payload()
        
        elif self.state == ParserState.PAYLOAD_CONTINUE:
            # After EEG, check for extended data or sync
            if byte == self.AP_CHECK_BYTE:  # 0x06 - Extended data follows
                self.state = ParserState.EXTEND_PAYLOAD
                self.offset = 1
                self.payload[0] = self.AP_CHECK_BYTE
            elif byte == self.SYNC_BYTE:
                # New packet starting
                self.state = ParserState.SYNC_CHECK
            else:
                self.state = ParserState.SYNC
        
        elif self.state == ParserState.RAW_PAYLOAD:
            # Collecting raw data (4 bytes + checksum)
            self.payload[self.offset] = byte
            self.offset += 1
            
            if self.offset > 4:
                self.state = ParserState.SYNC
                self.checksum = byte
                self._parse_raw_payload()
        
        elif self.state == ParserState.EXTEND_PAYLOAD:
            # Collecting extended data
            self.payload[self.offset] = byte
            self.offset += 1
            
            if byte == self.FLAG_CHECK_BYTE:  # 0x55 - End marker
                self.state = ParserState.SYNC
                self._parse_extend_payload()
        
        elif self.state == ParserState.GYRO_PAYLOAD:
            # Collecting gyro data (8 bytes total: type + 6 data bytes + checksum)
            self.payload[self.offset] = byte
            self.offset += 1
            
            if self.offset > 7:  # > 7 means offset reached 8 (same as C#)
                # Got all gyro data
                self.state = ParserState.SYNC
                self._parse_gyro_payload()
        
        elif self.state == ParserState.HRV_LENGTH:
            # HRV packet length
            self.offset = 0
            if byte == self.HRV_LENGTH_BYTE:  # 0x0C
                self.state = ParserState.HRV_PAYLOAD
            else:
                self.state = ParserState.SYNC
        
        elif self.state == ParserState.HRV_PAYLOAD:
            # Collecting HRV data
            self.payload[self.offset] = byte
            self.offset += 1
            
            if self.offset > 12:
                self.state = ParserState.SYNC
                self._parse_hrv_payload()
    
    def _parse_eeg_payload(self):
        """Parse EEG data from payload buffer"""
        # Verify checksum
        checksum_calc = 0
        for i in range(32):
            checksum_calc += self.payload[i]
        checksum_calc = (~checksum_calc) & 0xFF
        
        if checksum_calc != self.checksum:
            if self.debug:
                print(f"EEG checksum mismatch: {checksum_calc} != {self.checksum}")
            return
        
        # Parse payload
        signal = 0
        attention = 0
        meditation = 0
        delta = 0
        theta = 0
        low_alpha = 0
        high_alpha = 0
        low_beta = 0
        high_beta = 0
        low_gamma = 0
        high_gamma = 0
        
        idx = 0
        while idx < 32:
            code = self.payload[idx]
            idx += 1
            
            if code == self.SIGNAL_CHECK_BYTE:  # 0x02
                signal = self.payload[idx]
                idx += 1
            
            elif code == self.EEG_CHECK_BYTE:  # 0x83 (131)
                length = self.payload[idx]
                idx += 1
                
                if length == self.EEG_LENGTH_BYTE:  # 24 bytes of EEG data
                    # Each wave is 3 bytes (big-endian)
                    delta = self._get_eeg_power(idx)
                    idx += 3
                    theta = self._get_eeg_power(idx)
                    idx += 3
                    low_alpha = self._get_eeg_power(idx)
                    idx += 3
                    high_alpha = self._get_eeg_power(idx)
                    idx += 3
                    low_beta = self._get_eeg_power(idx)
                    idx += 3
                    high_beta = self._get_eeg_power(idx)
                    idx += 3
                    low_gamma = self._get_eeg_power(idx)
                    idx += 3
                    high_gamma = self._get_eeg_power(idx)
                    idx += 3
            
            elif code == self.ATT_CHECK_BYTE:  # 0x04
                attention = self.payload[idx]
                idx += 1
            
            elif code == self.MED_CHECK_BYTE:  # 0x05
                meditation = self.payload[idx]
                idx += 1
        
        # Create model
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
            print(f"\n[OK] EEG Data Parsed:")
            print(f"   Attention: {attention}, Meditation: {meditation}")
            print(f"   Delta: {delta}, Theta: {theta}")
            print(f"   Low Alpha: {low_alpha}, High Alpha: {high_alpha}")
            print(f"   Low Beta: {low_beta}, High Beta: {high_beta}")
            print(f"   Low Gamma: {low_gamma}, High Gamma: {high_gamma}\n")
        
        self._last_eeg = model
        if self.on_eeg_data:
            self.on_eeg_data(model)
    
    def _parse_gyro_payload(self):
        """Parse gyro data from payload buffer"""
        try:
            # Gyro data: [type_byte, X_high, X_low, Y_high, Y_low, Z_high, Z_low, checksum]
            # Payload[0] = 0x03 (type byte)
            # Bytes 1-2: X (signed big-endian)
            x = int.from_bytes(self.payload[1:3], byteorder='big', signed=True)
            
            # Bytes 3-4: Y (signed big-endian)
            y = int.from_bytes(self.payload[3:5], byteorder='big', signed=True)
            
            # Bytes 5-6: Z (signed big-endian)
            z = int.from_bytes(self.payload[5:7], byteorder='big', signed=True)
            
            if self.debug:
                print(f"[OK] Gyro Data: X={x}, Y={y}, Z={z}")
            
            self._last_gyro = (x, y, z)
            if self.on_gyro_data:
                self.on_gyro_data(x, y, z)
        
        except Exception as e:
            if self.debug:
                print(f"Error parsing gyro data: {e}")
    
    def _parse_extend_payload(self):
        """Parse extended data from payload buffer"""
        ap = 0
        electric = 0
        gnaw = 0
        version = "0.0.0"
        temperature = 0.0
        heart_rate = 0
        
        idx = 0
        while idx < 12:
            code = self.payload[idx]
            idx += 1
            
            if code == self.AP_CHECK_BYTE:  # 0x06
                ap = self.payload[idx]
                idx += 1
            
            elif code == self.POWER_CHECK_BYTE:  # 0x07
                electric = self.payload[idx]
                idx += 1
            
            elif code == self.FIXED_CHECK_BYTE:  # 0x08
                # Version (BCD format)
                ver1 = self.payload[idx]
                ver1 = ver1 // 16 + ver1 % 16 // 10
                idx += 1
                
                gnaw = self.payload[idx]
                idx += 1
                
                ver2 = self.payload[idx]
                ver2 = ver2 // 16 * 10 + ver2 % 16
                idx += 1
                
                version = f"{ver1}.{ver2}.0"
                
                # Temperature
                temp_high = self.payload[idx]
                idx += 1
                temp_low = self.payload[idx]
                idx += 1
                
                if temp_high != 255:
                    temperature = temp_high + temp_low / 10.0
                
                # Heart rate
                heart_rate = self.payload[idx]
                idx += 1
                if heart_rate == 255:
                    heart_rate = 0
            
            else:
                idx += 1
        
        model = BrainLinkExtendModel(
            ap=ap,
            electric=electric,
            version=version,
            temperature=temperature,
            heart_rate=heart_rate
        )
        
        if self.debug:
            print(f"\n[OK] Extended Data Parsed:")
            print(f"   AP: {ap}")
            print(f"   Electric (Battery): {electric}")
            print(f"   Version: {version}")
            print(f"   Temperature: {temperature}C")
            print(f"   Heart Rate: {heart_rate} bpm\n")
        
        self._last_extend = model
        if self.on_extend_data:
            self.on_extend_data(model)
    
    def _parse_raw_payload(self):
        """Parse raw data from payload buffer"""
        # Verify checksum
        checksum_calc = 0
        for i in range(4):
            checksum_calc += self.payload[i]
        checksum_calc = (~checksum_calc) & 0xFF
        
        if checksum_calc != self.checksum:
            return
        
        # Extract raw value (signed 16-bit)
        raw_high = self.payload[2]
        raw_low = self.payload[3]
        raw = (raw_high << 8) | raw_low
        raw = raw if raw < 32768 else raw - 65536
        
        if self.debug:
            print(f"[OK] Raw Data: {raw}")
        
        if self.on_raw_data:
            self.on_raw_data(raw)
    
    def _parse_hrv_payload(self):
        """Parse HRV data from payload buffer"""
        # Verify checksum
        checksum_calc = 12
        for i in range(9):
            checksum_calc += self.payload[i]
        checksum_calc &= 0xFF
        
        checksum = self.payload[9]
        if checksum != checksum_calc:
            return
        
        # Extract HRV values
        hrv1 = (self.payload[0] << 8) | self.payload[1]
        hrv2 = (self.payload[2] << 8) | self.payload[3]
        hrv3 = (self.payload[4] << 8) | self.payload[5]
        blink = self.payload[8]
        
        hrv_list = []
        if hrv1 > 0:
            hrv_list.append(hrv1)
        if hrv2 > 0:
            hrv_list.append(hrv2)
        if hrv3 > 0:
            hrv_list.append(hrv3)
        
        if self.debug:
            print(f"[OK] HRV Data: {hrv_list}, Blink: {blink}")
        
        if self.on_hrv_data:
            self.on_hrv_data(hrv_list, blink)
    
    def _get_eeg_power(self, idx: int) -> int:
        """Extract 3-byte EEG power value (big-endian)"""
        high = self.payload[idx]
        mid = self.payload[idx + 1]
        low = self.payload[idx + 2]
        return ((high << 16) | (mid << 8) | low) & 0xFFFFFF
