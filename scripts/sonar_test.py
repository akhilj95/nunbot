import serial
import time

# ---------- Configuration ----------
SERIAL_PORT = "/dev/ttyUSB0"  # Adjust as needed for your system
BAUD_RATE = 19200             # Must match device setting
DEVICE_ID = 0x13             # Default address is 0x11 (17 decimal)
MODE = "distance"          # "temperature" or "distance"
READ_INTERVAL = 1             # seconds between readings

# -------- Helper Functions --------

def calc_checksum(packet):
    return sum(packet) & 0xFF

def build_cmd(address, cmd):
    # Build 6-byte command packet:
    # Header(0x55, 0xAA), Address, 0x00, Command, checksum
    packet = bytearray([0x55, 0xAA, address, 0x00, cmd])
    cs = calc_checksum(packet)
    packet.append(cs)
    return packet

def trigger_reading(ser, address):
    # Send command 0x01 to trigger distance reading
    cmd_packet = build_cmd(address, 0x01)
    ser.write(cmd_packet)
    print(f"Triggered reading for device 0x{address:02x}")

def read_distance(ser, address):
    # Send command 0x02 to read distance
    cmd_packet = build_cmd(address, 0x02)
    ser.write(cmd_packet)
    print(f"Requested distance for device 0x{address:02x}")

def read_temperature(ser, address):
    # Send command 0x03 to read temperature
    cmd_packet = build_cmd(address, 0x03)
    ser.write(cmd_packet)
    print(f"Requested temperature for device 0x{address:02x}")

def parse_response(data):
    # Parse according to protocol: 
    # Expected: header(2), address(1), length(1), cmd(1), payload(2), checksum(1)
    if len(data) < 8:
        return None

    header = data[0:2]
    address = data[2]
    length = data[3]
    cmd = data[4]

    if header != b'\x55\xaa' or length != 2:
        return None

    high = data[5]
    low = data[6]
    checksum = data[7]
    calsum = sum(data[0:7]) & 0xFF

    if checksum != calsum:
        print(f"Checksum mismatch: expected {calsum:02x}, got {checksum:02x}")
        return None

    # Decode sensor data
    value = high * 255 + low

    if cmd == 0x02:
        return ("distance", value)
    elif cmd == 0x03:
        temp = value / 10.0
        return ("temperature", temp)
    else:
        return None

# ------------ Main --------------

def main():
    ser = serial.Serial(
        port=SERIAL_PORT,
        baudrate=BAUD_RATE,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=2
    )
    time.sleep(3)  # allow connection init

    print(f"Starting sensor reading with device address 0x{DEVICE_ID:02x}")

    try:
        while True:
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            if MODE == "distance":
                # Trigger then read distance
                trigger_reading(ser, DEVICE_ID)
                time.sleep(0.1)
                read_distance(ser, DEVICE_ID)
            elif MODE == "temperature":
                # Only read temperature command (C# code doesn't trigger temperature)
                read_temperature(ser, DEVICE_ID)

            time.sleep(0.3)  # Give device some time to respond

            data = ser.read(8)
            if data:
                print("Raw response:", data.hex())
                result = parse_response(data)
                if result:
                    typ, val = result
                    print(f"{typ.capitalize()} reading: {val}")
                else:
                    print("Invalid or unrecognized response.")
            else:
                print("No response received.")

            time.sleep(READ_INTERVAL)

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        ser.close()

if __name__ == "__main__":
    main()
