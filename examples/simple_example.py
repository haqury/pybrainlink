"""Simple example of using PyBrainLink"""

import asyncio
from pybrainlink import BrainLinkDevice


async def main():
    """Main example function"""
    
    # Create device
    device = BrainLinkDevice()
    
    # Define data handlers
    def on_eeg_data(data):
        """Handle EEG data"""
        print(f"\n🧠 EEG Data:")
        print(f"   Attention: {data.attention:3d}%")
        print(f"   Meditation: {data.meditation:3d}%")
        print(f"   Delta: {data.delta:6d}")
        print(f"   Theta: {data.theta:6d}")
    
    def on_gyro_data(x, y, z):
        """Handle gyroscope data"""
        print(f"🎯 Gyro: X={x:4d}, Y={y:4d}, Z={z:4d}")
    
    # Set callbacks
    device.on_eeg_data = on_eeg_data
    device.on_gyro_data = on_gyro_data
    
    # Scan for devices
    print("🔍 Scanning for BrainLink devices...")
    devices = await device.scan(timeout=10.0)
    
    if not devices:
        print("❌ No devices found")
        return
    
    print(f"\n✅ Found {len(devices)} device(s)")
    
    # Connect to first BrainLink device
    brainlink_device = None
    for address, name in devices:
        if "BrainLink" in name:
            brainlink_device = (address, name)
            break
    
    if not brainlink_device:
        print("❌ No BrainLink device found")
        return
    
    address, name = brainlink_device
    print(f"\n🔌 Connecting to {name} ({address})...")
    
    success = await device.connect(address)
    
    if not success:
        print("❌ Failed to connect")
        return
    
    print("\n✅ Connected! Receiving data...\n")
    print("Press Ctrl+C to stop\n")
    
    # Receive data for 60 seconds (or until Ctrl+C)
    try:
        await asyncio.sleep(60)
    except KeyboardInterrupt:
        print("\n\n👋 Stopping...")
    
    # Disconnect
    await device.disconnect()
    print("✅ Disconnected")


if __name__ == "__main__":
    print("=" * 60)
    print("PyBrainLink - Simple Example".center(60))
    print("=" * 60)
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
