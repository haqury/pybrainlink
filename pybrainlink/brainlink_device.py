"""Main BrainLink device class for easy access"""

import asyncio
from typing import Optional, Callable, List, Tuple
from bleak import BleakScanner, BleakClient

from .protocol_parser import BrainLinkProtocolParser
from .models import BrainLinkModel


class BrainLinkDevice:
    """
    High-level interface for BrainLink EEG device
    
    Example:
        >>> device = BrainLinkDevice()
        >>> device.on_eeg_data = lambda data: print(f"Attention: {data.attention}")
        >>> await device.scan()
        >>> await device.connect("CC:36:16:32:7E:49")
    """

    def __init__(self):
        """Initialize BrainLink device"""
        self.client: Optional[BleakClient] = None
        self.is_connected = False
        self.parser = BrainLinkProtocolParser()
        
        # Callbacks
        self.on_eeg_data: Optional[Callable[[BrainLinkModel], None]] = None
        self.on_extend_data: Optional[Callable] = None
        self.on_gyro_data: Optional[Callable[[int, int, int], None]] = None
        self.on_device_found: Optional[Callable[[str, str], None]] = None
        
        # Nordic UART Service UUID
        self.UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
        self.UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
        self.UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    async def scan(self, timeout: float = 10.0) -> List[Tuple[str, str]]:
        """
        Scan for BrainLink devices
        
        Args:
            timeout: Scan duration in seconds
            
        Returns:
            List of (address, name) tuples
        """
        devices = []
        try:
            print("🔍 Scanning for Bluetooth devices...")
            discovered = await BleakScanner.discover(timeout=timeout)
            
            for device in discovered:
                if device.name:
                    devices.append((device.address, device.name))
                    print(f"   Found: {device.name} ({device.address})")
                    
                    if self.on_device_found:
                        self.on_device_found(device.address, device.name)
                        
        except Exception as e:
            print(f"❌ Scan error: {e}")
            
        return devices

    async def connect(self, address: str) -> bool:
        """
        Connect to BrainLink device
        
        Args:
            address: Bluetooth MAC address
            
        Returns:
            True if connected successfully
        """
        try:
            print(f"🔌 Connecting to {address}...")
            self.client = BleakClient(address)
            await self.client.connect()
            
            if not self.client.is_connected:
                print("❌ Failed to connect")
                return False
            
            self.is_connected = True
            print(f"✅ Connected to {address}")
            
            # Start notifications
            await self._start_notifications()
            
            return True
            
        except Exception as e:
            print(f"❌ Connection error: {e}")
            self.is_connected = False
            return False

    async def disconnect(self):
        """Disconnect from device"""
        if self.client and self.is_connected:
            try:
                await self.client.disconnect()
                self.is_connected = False
                print("👋 Disconnected")
            except Exception as e:
                print(f"❌ Disconnect error: {e}")

    async def _start_notifications(self):
        """Start receiving notifications from device"""
        if not self.client:
            return
        
        try:
            # Get all characteristics
            for service in self.client.services:
                for char in service.characteristics:
                    if "notify" in char.properties:
                        print(f"📡 Starting notifications on {char.uuid}")
                        await self.client.start_notify(char.uuid, self._notification_handler)
                        
        except Exception as e:
            print(f"❌ Notification error: {e}")

    def _notification_handler(self, sender, data: bytearray):
        """
        Handle incoming data from device
        
        Args:
            sender: Characteristic that sent the data
            data: Raw data bytes
        """
        try:
            # Parse data (now returns 3 values)
            eeg_data, gyro_data, extend_data = self.parser.parse_data(data)
            
            # Call callbacks
            if eeg_data and self.on_eeg_data:
                self.on_eeg_data(eeg_data)
            
            if extend_data and self.on_extend_data:
                self.on_extend_data(extend_data)
            
            if gyro_data and self.on_gyro_data:
                x, y, z = gyro_data
                self.on_gyro_data(x, y, z)
                
        except Exception as e:
            print(f"❌ Parse error: {e}")

    def __del__(self):
        """Cleanup on deletion"""
        if self.is_connected:
            # Note: Can't use await in __del__, so we just mark as disconnected
            self.is_connected = False
