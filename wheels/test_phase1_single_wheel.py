#!/usr/bin/env python3
"""
test_phase1_single_wheel.py
Visual Vectoring v2.3 — Phase 1 Bring-Up Test

PURPOSE: Verify Pi ↔ Teensy serial link, then test each wheel individually.
         Run this FIRST before testing all 4 wheels.

USAGE:
    python3 test_phase1_single_wheel.py

PREREQUISITES:
    - Teensy 4.1 loaded with woundbot_test_firmware.ino
    - Teensy USB-connected to Pi
    - TMC2209 wired to Teensy (STEP/DIR/EN/VIO/GND)
    - 12V applied to TMC2209 VMOT
    - ROBOT WHEELS OFF THE GROUND (or expect it to move!)

pip install pyserial
"""

import serial
import time
import sys
import threading

time.sleep(2) 

# ── Configuration ─────────────────────────────────────────────
PORT = "/dev/ttyACM0"    # Change if your Teensy enumerates differently
BAUD = 115200
TIMEOUT = 0.1

WHEEL_NAMES = {0: "FL (Front-Left)", 1: "FR (Front-Right)",
               2: "RL (Rear-Left)",  3: "RR (Rear-Right)"}


# ── Serial Reader Thread ─────────────────────────────────────
class TeensyReader(threading.Thread):
    """Background thread to print Teensy output."""
    def __init__(self, ser):
        super().__init__(daemon=True)
        self.ser = ser
        self.running = True

    def run(self):
        while self.running:
            try:
                line = self.ser.readline().decode("utf-8", errors="replace").strip()
                if line:
                    print(f"  [Teensy] {line}")
            except Exception:
                pass

    def stop(self):
        self.running = False


# ── Helper Functions ──────────────────────────────────────────
def send(ser, cmd):
    """Send command to Teensy and print it."""
    print(f"  → Sending: {cmd}")
    ser.write(f"{cmd}\n".encode())
    ser.flush()
    time.sleep(0.05)


def wait_for(ser, keyword, timeout=3.0):
    """Wait for a specific keyword in Teensy response."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if keyword in line:
            return True, line
    return False, ""


def flush_input(ser):
    """Drain any pending serial data."""
    ser.reset_input_buffer()
    time.sleep(0.1)
    while ser.in_waiting:
        ser.read(ser.in_waiting)
        time.sleep(0.05)


# ── Test Functions ────────────────────────────────────────────
def test_connectivity(ser):
    """Test 1: Verify serial link with PING/PONG."""
    print("\n" + "="*50)
    print("TEST 1: Serial Connectivity (PING/PONG)")
    print("="*50)

    flush_input(ser)
    ser.write(b"PING\n")
    ok, line = wait_for(ser, "PONG", timeout=2.0)

    if ok:
        print("  ✅ PASS — Teensy responded with PONG")
        return True
    else:
        print("  ❌ FAIL — No PONG received. Check:")
        print("       - Is the Teensy powered and connected via USB?")
        print("       - Is the correct port selected? (try /dev/ttyACM1)")
        print("       - Is the test firmware uploaded?")
        return False


def test_enable_pin(ser):
    """Test 2: Verify EN pin toggles (motors enable/disable)."""
    print("\n" + "="*50)
    print("TEST 2: Motor Enable Pin")
    print("="*50)
    print("  Sending STATUS to check EN pin state...")

    flush_input(ser)
    send(ser, "STATUS")
    time.sleep(0.3)

    # Read all status lines
    lines = []
    while ser.in_waiting:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if line:
            lines.append(line)
            print(f"  [Teensy] {line}")

    print("\n  ✅ If you see 'Motors: DISABLED' and 'EN pin: HIGH', the EN pin is correct.")
    print("  The TMC2209 should be in sleep mode (no holding torque).")
    input("  Press Enter to continue...")
    return True


def test_single_wheel(ser, wheel_idx):
    """Test 3: Spin a single wheel."""
    name = WHEEL_NAMES[wheel_idx]
    print(f"\n{'='*50}")
    print(f"TEST 3: Single Wheel — {name} (index {wheel_idx})")
    print(f"{'='*50}")
    print(f"  ⚠  SAFETY: Ensure the robot is on blocks or wheels are free to spin!")
    print(f"  This will spin wheel {name} at 400 steps/s for 3 seconds.")
    input(f"  Press Enter to start (or Ctrl+C to abort)...")

    flush_input(ser)

    # Forward
    print(f"\n  >>> Spinning {name} FORWARD...")
    send(ser, f"TEST_WHEEL {wheel_idx} 1 400")
    time.sleep(3.0)
    send(ser, "TEST_STOP")
    time.sleep(0.5)

    print(f"  Did {name} spin forward (one direction)?")
    fwd_ok = input("  (y/n): ").strip().lower() == "y"

    # Reverse
    print(f"\n  >>> Spinning {name} REVERSE...")
    send(ser, f"TEST_WHEEL {wheel_idx} 0 400")
    time.sleep(3.0)
    send(ser, "TEST_STOP")
    time.sleep(0.5)

    print(f"  Did {name} spin in the opposite direction?")
    rev_ok = input("  (y/n): ").strip().lower() == "y"

    # Higher speed
    print(f"\n  >>> Spinning {name} FORWARD at 800 steps/s (faster)...")
    send(ser, f"TEST_WHEEL {wheel_idx} 1 800")
    time.sleep(3.0)
    send(ser, "TEST_STOP")
    time.sleep(0.5)

    print(f"  Did it spin noticeably faster?")
    speed_ok = input("  (y/n): ").strip().lower() == "y"

    # Report
    print(f"\n  Results for {name}:")
    print(f"    Forward:   {'✅' if fwd_ok else '❌'}")
    print(f"    Reverse:   {'✅' if rev_ok else '❌'}")
    print(f"    Speed up:  {'✅' if speed_ok else '❌'}")

    if not fwd_ok and not rev_ok:
        print(f"\n  🔧 TROUBLESHOOTING for {name}:")
        print(f"    1. Check STEP wire from Teensy Pin {2 + wheel_idx*2} to TMC2209 STEP")
        print(f"    2. Check DIR wire from Teensy Pin {3 + wheel_idx*2} to TMC2209 DIR")
        print(f"    3. Check TMC2209 VM has 12V (measure with multimeter)")
        print(f"    4. Check VCC_IO has 3.3V from Teensy")
        print(f"    5. Check motor coil wires: A1/A2 to one coil, B1/B2 to other")
        print(f"    6. Check 100µF cap on VMOT")
        print(f"    7. Check VREF pot is not turned fully clockwise (zero current)")

    return fwd_ok and rev_ok


def test_watchdog(ser):
    """Test 4: Verify watchdog stops motor after timeout."""
    print(f"\n{'='*50}")
    print("TEST 4: Watchdog Timeout")
    print("="*50)
    print("  This starts wheel 0 spinning, then STOPS sending commands.")
    print("  The Teensy should auto-stop after 500 ms and print FAULT WATCHDOG.")
    input("  Press Enter to start...")

    flush_input(ser)
    send(ser, "TEST_WHEEL 0 1 400")
    print("  Wheel spinning... waiting for watchdog (should stop in <1 second)...")
    time.sleep(2.0)

    # Read response
    lines = []
    while ser.in_waiting:
        line = ser.readline().decode("utf-8", errors="replace").strip()
        if line:
            lines.append(line)
            print(f"  [Teensy] {line}")

    found_fault = any("FAULT" in l for l in lines)
    found_disabled = any("DISABLED" in l for l in lines)

    if found_fault or found_disabled:
        print("  ✅ PASS — Watchdog triggered, motors disabled")
    else:
        print("  ⚠  Could not confirm watchdog (check Teensy serial output)")

    return found_fault or found_disabled


# ── Main ──────────────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════╗")
    print("║  Visual Vectoring v2.3 — Phase 1 Test       ║")
    print("║  Single Wheel Bring-Up                       ║")
    print("╚══════════════════════════════════════════════╝")

    # Open serial
    print(f"\nOpening {PORT} at {BAUD} baud...")
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        time.sleep(2.0)  # Teensy resets on serial open
        flush_input(ser)
        print("  Serial port opened.\n")
    except Exception as e:
        print(f"  ❌ Cannot open {PORT}: {e}")
        print("  Try: ls /dev/ttyACM*")
        sys.exit(1)

    # Start background reader
    # reader = TeensyReader(ser)
    # reader.start()

    results = {}

    try:
        # Test 1: Connectivity
        results["connectivity"] = test_connectivity(ser)
        if not results["connectivity"]:
            print("\n⛔ Cannot proceed without serial connectivity. Fix and retry.")
            return

        # Test 2: EN pin
        results["enable_pin"] = test_enable_pin(ser)

        # Test 3: Each wheel
        print("\n" + "="*50)
        print("WHEEL-BY-WHEEL TESTING")
        print("="*50)

        for i in range(4):
            name = WHEEL_NAMES[i]
            print(f"\n  Next: {name}")
            go = input(f"  Test this wheel? (y/n/q to quit): ").strip().lower()
            if go == "q":
                break
            if go == "y":
                results[f"wheel_{i}"] = test_single_wheel(ser, i)
            else:
                results[f"wheel_{i}"] = None
                print(f"  Skipped {name}")

        # Test 4: Watchdog
        print("\n")
        go = input("  Test watchdog timeout? (y/n): ").strip().lower()
        if go == "y":
            results["watchdog"] = test_watchdog(ser)

        # Summary
        print("\n" + "="*50)
        print("PHASE 1 TEST SUMMARY")
        print("="*50)
        for key, val in results.items():
            status = "✅ PASS" if val is True else ("❌ FAIL" if val is False else "⏭ SKIPPED")
            print(f"  {key:20s} {status}")
        print("="*50)

        all_pass = all(v is True for v in results.values() if v is not None)
        if all_pass:
            print("\n🎉 All tests passed! Proceed to Phase 2 (test_phase2_all_wheels.py)")
        else:
            print("\n⚠  Some tests failed. Fix issues before proceeding.")

    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        send(ser, "TEST_STOP")
        send(ser, "CMD_STOP")

    finally:
        # reader.stop()
        send(ser, "CMD_STOP")
        ser.close()
        print("Serial port closed.")


if __name__ == "__main__":
    main()
