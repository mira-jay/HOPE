#!/usr/bin/env python3
"""
test_phase2_all_wheels.py
Visual Vectoring v2.3 — Phase 2 Bring-Up Test

PURPOSE: Test all 4 wheels together using CMD_VEL (mecanum kinematics).
         Validates forward, strafe, rotate, diagonal, and watchdog.
         Run this AFTER Phase 1 passes for all individual wheels.

USAGE:
    python3 test_phase2_all_wheels.py

PREREQUISITES:
    - Phase 1 passed for all 4 wheels
    - Robot on blocks OR in an open area (it WILL move)
    - 12V power applied, E-Stop within reach

pip install pyserial
"""

import serial
import time
import sys
import threading

# ── Configuration ─────────────────────────────────────────────
PORT = "/dev/ttyACM0"
BAUD = 115200
TIMEOUT = 0.1

# How long to run each motion test (seconds)
TEST_DURATION = 2.5

# Keep-alive interval: Teensy watchdog is 500ms, so send every 200ms
KEEPALIVE_HZ = 5  # 200ms interval


# ── Serial Helpers ────────────────────────────────────────────
class TeensyLink:
    """Manages serial connection with background reader and keep-alive."""

    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout=TIMEOUT)
        time.sleep(2.0)  # Teensy resets on open
        self.ser.reset_input_buffer()
        self.odom_lines = []
        self.fault = False
        self._reader_running = True
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    def _read_loop(self):
        while self._reader_running:
            try:
                line = self.ser.readline().decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                if line.startswith("ODOM"):
                    self.odom_lines.append(line)
                    # Only keep last 20
                    if len(self.odom_lines) > 20:
                        self.odom_lines = self.odom_lines[-20:]
                elif "FAULT" in line:
                    self.fault = True
                    print(f"  ⚠ [Teensy] {line}")
                else:
                    print(f"  [Teensy] {line}")
            except Exception:
                pass

    def send(self, cmd):
        self.ser.write(f"{cmd}\n".encode())
        self.ser.flush()

    def send_vel(self, vx, vy, omega, duration):
        """Send CMD_VEL repeatedly for `duration` seconds (keep-alive)."""
        cmd = f"CMD_VEL {vx:.4f} {vy:.4f} {omega:.4f}"
        interval = 1.0 / KEEPALIVE_HZ
        t0 = time.time()
        while time.time() - t0 < duration:
            self.ser.write(f"{cmd}\n".encode())
            self.ser.flush()
            time.sleep(interval)

    def stop(self):
        self.send("CMD_STOP")
        time.sleep(0.2)

    def ping(self):
        self.ser.reset_input_buffer()
        self.send("PING")
        t0 = time.time()
        while time.time() - t0 < 2.0:
            line = self.ser.readline().decode("utf-8", errors="replace").strip()
            if "PONG" in line:
                return True
        return False

    def get_last_odom(self):
        """Parse last ODOM line → dict."""
        if not self.odom_lines:
            return None
        parts = self.odom_lines[-1].split()
        if len(parts) >= 7:
            return {
                "x": float(parts[1]), "y": float(parts[2]), "yaw": float(parts[3]),
                "vx": float(parts[4]), "vy": float(parts[5]), "omega": float(parts[6]),
            }
        return None

    def close(self):
        self._reader_running = False
        self.send("CMD_STOP")
        time.sleep(0.3)
        self.ser.close()


# ── Motion Tests ──────────────────────────────────────────────
# Each test: (name, description, vx, vy, omega, expected_wheels)
# expected_wheels describes what the user should observe

MOTION_TESTS = [
    {
        "name": "Forward",
        "desc": "All 4 wheels spin to drive the robot FORWARD (+X)",
        "vx": 0.10, "vy": 0.0, "omega": 0.0,
        "expect": "All wheels spin same direction. Robot moves forward.",
    },
    {
        "name": "Backward",
        "desc": "All 4 wheels spin to drive the robot BACKWARD (-X)",
        "vx": -0.10, "vy": 0.0, "omega": 0.0,
        "expect": "All wheels spin opposite to forward. Robot moves backward.",
    },
    {
        "name": "Strafe Left",
        "desc": "Mecanum strafe: robot slides LEFT (+Y) without rotating",
        "vx": 0.0, "vy": 0.10, "omega": 0.0,
        "expect": "FL and RR spin backward, FR and RL spin forward.\nRobot slides sideways to the left.",
    },
    {
        "name": "Strafe Right",
        "desc": "Mecanum strafe: robot slides RIGHT (-Y) without rotating",
        "vx": 0.0, "vy": -0.10, "omega": 0.0,
        "expect": "FL and RR spin forward, FR and RL spin backward.\nRobot slides sideways to the right.",
    },
    {
        "name": "Rotate CCW",
        "desc": "Spin in place counter-clockwise (+omega)",
        "vx": 0.0, "vy": 0.0, "omega": 0.30,
        "expect": "Left wheels spin backward, right wheels spin forward.\nRobot rotates in place counter-clockwise.",
    },
    {
        "name": "Rotate CW",
        "desc": "Spin in place clockwise (-omega)",
        "vx": 0.0, "vy": 0.0, "omega": -0.30,
        "expect": "Left wheels spin forward, right wheels spin backward.\nRobot rotates in place clockwise.",
    },
    {
        "name": "Diagonal (Forward + Left)",
        "desc": "Combined forward + left strafe",
        "vx": 0.08, "vy": 0.08, "omega": 0.0,
        "expect": "FR and RL spin fast, FL and RR barely move (or stop).\nRobot moves diagonally forward-left.",
    },
    {
        "name": "Arc (Forward + Rotate)",
        "desc": "Drive forward while turning",
        "vx": 0.08, "vy": 0.0, "omega": 0.20,
        "expect": "All wheels spin but at different speeds.\nRobot drives in a curved arc.",
    },
]


def run_motion_test(link, test, test_num, total):
    """Run a single motion test and collect user feedback."""
    print(f"\n{'─'*50}")
    print(f"  TEST {test_num}/{total}: {test['name']}")
    print(f"  {test['desc']}")
    print(f"  CMD_VEL: vx={test['vx']:.2f}  vy={test['vy']:.2f}  ω={test['omega']:.2f}")
    print(f"  Duration: {TEST_DURATION}s")
    print(f"{'─'*50}")
    print(f"  Expected behavior:")
    for line in test["expect"].split("\n"):
        print(f"    → {line}")
    print()
    input("  Press Enter to run (Ctrl+C to abort)...")

    # Clear odom
    link.odom_lines.clear()
    link.fault = False

    # Run motion
    print(f"  🔄 Running: {test['name']}...")
    link.send_vel(test["vx"], test["vy"], test["omega"], TEST_DURATION)
    link.stop()

    # Check fault
    if link.fault:
        print("  ⚠ FAULT detected during test!")
        return False

    # Show odometry delta
    odom = link.get_last_odom()
    if odom:
        print(f"  📍 Odometry: x={odom['x']:.3f}  y={odom['y']:.3f}  yaw={odom['yaw']:.2f}")

    # User confirms
    ok = input("  Did the motion match the expected behavior? (y/n): ").strip().lower()
    return ok == "y"


def test_emergency_stop(link):
    """Test that CMD_STOP works instantly."""
    print(f"\n{'─'*50}")
    print("  TEST: Emergency Stop (CMD_STOP)")
    print("  Robot will drive forward, then CMD_STOP is sent.")
    print(f"{'─'*50}")
    input("  Press Enter to run...")

    print("  🔄 Driving forward...")
    link.send_vel(0.10, 0.0, 0.0, 1.5)

    print("  🛑 Sending CMD_STOP...")
    link.stop()
    time.sleep(0.5)

    ok = input("  Did the robot stop immediately? (y/n): ").strip().lower()
    return ok == "y"


def test_watchdog(link):
    """Test that watchdog stops motors after timeout."""
    print(f"\n{'─'*50}")
    print("  TEST: Watchdog Timeout")
    print("  Robot will start moving, then Pi STOPS sending commands.")
    print("  Teensy should auto-stop within 500ms.")
    print(f"{'─'*50}")
    input("  Press Enter to run...")

    # Send a few commands to get moving
    for _ in range(5):
        link.send("CMD_VEL 0.10 0.0 0.0")
        time.sleep(0.1)

    print("  🔄 Moving... now going silent (no more commands)...")
    print("  Waiting for watchdog...")
    time.sleep(2.0)

    # Read any fault messages
    ok = input("  Did the robot stop on its own within ~1 second? (y/n): ").strip().lower()
    return ok == "y"


def test_odom_sanity(link):
    """Test that odometry values are reasonable."""
    print(f"\n{'─'*50}")
    print("  TEST: Odometry Sanity Check")
    print("  Robot will drive forward for 3 seconds at 0.10 m/s.")
    print("  Expected: ~0.30m of forward travel in odometry.")
    print(f"{'─'*50}")
    input("  Press Enter to run...")

    # Reset by noting current odom
    link.odom_lines.clear()
    time.sleep(0.2)

    odom_before = link.get_last_odom()
    x0 = odom_before["x"] if odom_before else 0.0

    link.send_vel(0.10, 0.0, 0.0, 3.0)
    link.stop()
    time.sleep(0.3)

    odom_after = link.get_last_odom()
    if odom_after:
        dx = odom_after["x"] - x0
        print(f"  📍 Odom delta X: {dx:.3f} m (expected ~0.30)")
        print(f"  📍 Odom Y:       {odom_after['y']:.3f} m (expected ~0.00)")
        print(f"  📍 Odom Yaw:     {odom_after['yaw']:.3f} rad (expected ~0.00)")

        reasonable = 0.15 < abs(dx) < 0.50
        if reasonable:
            print("  ✅ Odometry is in a reasonable range")
        else:
            print("  ⚠  Odometry seems off — check WHEEL_RADIUS and MICROSTEPS in firmware")
        return reasonable
    else:
        print("  ❌ No odometry data received")
        return False


# ── Main ──────────────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════╗")
    print("║  Visual Vectoring v2.3 — Phase 2 Test       ║")
    print("║  All Wheels + Mecanum Motion Patterns        ║")
    print("╚══════════════════════════════════════════════╝")
    print()
    print("⚠  SAFETY REMINDERS:")
    print("   • Keep E-Stop within arm's reach")
    print("   • Robot WILL move during these tests")
    print("   • Clear the area around the robot")
    print("   • If anything goes wrong, hit E-Stop or Ctrl+C")
    print()

    # Connect
    print(f"Opening {PORT} at {BAUD} baud...")
    try:
        link = TeensyLink(PORT, BAUD)
    except Exception as e:
        print(f"  ❌ Cannot open {PORT}: {e}")
        sys.exit(1)

    # Ping
    if not link.ping():
        print("  ❌ No PONG from Teensy. Run Phase 1 first.")
        link.close()
        sys.exit(1)
    print("  ✅ Teensy connected\n")

    # Set safe mode
    link.send("CMD_MODE SAFE")
    time.sleep(0.2)

    results = {}

    try:
        # ── Motion pattern tests ──
        print("\n" + "="*50)
        print("MECANUM MOTION PATTERN TESTS")
        print("="*50)

        for i, test in enumerate(MOTION_TESTS):
            go = input(f"\n  Run '{test['name']}' test? (y/n/q): ").strip().lower()
            if go == "q":
                break
            if go == "y":
                passed = run_motion_test(link, test, i+1, len(MOTION_TESTS))
                results[test["name"]] = passed
                if not passed:
                    print(f"\n  🔧 '{test['name']}' failed. Troubleshooting:")
                    print(f"    - If no wheels moved: check EN pin, 12V rail, VREF")
                    print(f"    - If wrong direction: swap motor coil wires on that wheel")
                    print(f"    - If wrong wheel spins: STEP/DIR wires are swapped between drivers")
                    print(f"    - If strafe doesn't work: check mecanum wheel roller orientation")
            else:
                results[test["name"]] = None

        # ── Emergency stop ──
        go = input("\n  Run emergency stop test? (y/n): ").strip().lower()
        if go == "y":
            results["Emergency Stop"] = test_emergency_stop(link)

        # ── Watchdog ──
        go = input("\n  Run watchdog test? (y/n): ").strip().lower()
        if go == "y":
            results["Watchdog"] = test_watchdog(link)

        # ── Odometry ──
        go = input("\n  Run odometry sanity check? (y/n): ").strip().lower()
        if go == "y":
            results["Odometry"] = test_odom_sanity(link)

        # ── Summary ──
        print("\n" + "="*50)
        print("PHASE 2 TEST SUMMARY")
        print("="*50)
        for key, val in results.items():
            if val is True:
                status = "✅ PASS"
            elif val is False:
                status = "❌ FAIL"
            else:
                status = "⏭  SKIP"
            print(f"  {key:25s} {status}")
        print("="*50)

        passed = [v for v in results.values() if v is not None]
        num_pass = sum(1 for v in passed if v)
        print(f"\n  {num_pass}/{len(passed)} tests passed")

        if all(v for v in passed):
            print("\n🎉 All tests passed! Base platform is validated.")
            print("   Next steps:")
            print("   1. Load production firmware (woundbot_teensy41.ino)")
            print("   2. Test ROS 2 Nav2 integration (twist_to_teensy.py)")
            print("   3. Test arm (xArm 1S LX-15D servos)")
        else:
            print("\n⚠  Some tests failed. Fix issues and re-run.")

    except KeyboardInterrupt:
        print("\n\n  Aborted! Stopping motors...")
        link.stop()

    finally:
        link.close()
        print("  Serial port closed.")


if __name__ == "__main__":
    main()
