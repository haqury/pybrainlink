"""Example: Record EEG session to JSON file"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from pybrainlink import BrainLinkDevice


async def main():
    """Record EEG session"""
    
    device = BrainLinkDevice()
    session_data = []
    
    def on_eeg_data(data):
        """Record each EEG reading"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'data': data.to_dict()
        }
        session_data.append(record)
        
        # Show progress
        if len(session_data) % 10 == 0:
            print(f"\r📝 Recorded {len(session_data)} readings...", end='')
    
    device.on_eeg_data = on_eeg_data
    
    # Scan and connect
    print("🔍 Scanning for BrainLink devices...")
    devices = await device.scan(timeout=10.0)
    
    brainlink_found = False
    for address, name in devices:
        if "BrainLink" in name:
            print(f"\n🔌 Connecting to {name}...")
            if await device.connect(address):
                brainlink_found = True
                break
    
    if not brainlink_found:
        print("❌ No BrainLink device found or failed to connect")
        return
    
    # Record for 30 seconds
    duration = 30
    print(f"\n⏱️  Recording for {duration} seconds...\n")
    
    try:
        await asyncio.sleep(duration)
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording interrupted by user")
    
    # Disconnect
    await device.disconnect()
    
    # Save to file
    output_file = Path(f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'session_info': {
                'start_time': session_data[0]['timestamp'] if session_data else None,
                'end_time': session_data[-1]['timestamp'] if session_data else None,
                'total_readings': len(session_data),
                'duration_seconds': duration
            },
            'readings': session_data
        }, f, indent=2)
    
    print(f"\n\n✅ Session complete!")
    print(f"   Total readings: {len(session_data)}")
    print(f"   Saved to: {output_file.absolute()}")


if __name__ == "__main__":
    print("=" * 60)
    print("PyBrainLink - Session Recorder".center(60))
    print("=" * 60)
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
