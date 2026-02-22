"""
Utility for robust xArm USB connection.

The blue arm (serial D30F103095D182300023D4D4) has a flaky cold-start: it takes
several USB-level power cycles before it fully enumerates. Once connected, the
arm's onboard watchdog disconnects it after ~26s of inactivity.

This module provides:
  - connect_arm(): retries Controller() until the HID device appears
  - ArmConnection: wrapper that keeps the arm alive and reconnects on drop
"""

import time
import threading
import xarm


BLUE_SERIAL  = "D30F103095D182300023D4D4"
BLACK_SERIAL = "5306101095D182300023D4D4"

# Watchdog fires at ~26s; ping every 20s to stay safe
_KEEPALIVE_INTERVAL = 20.0


def connect_arm(serial, retries=30, retry_delay=1.0, label="arm"):
    """
    Open an xarm.Controller, retrying until the USB device enumerates.

    The blue arm often takes 5–15 seconds and several USB power cycles before
    it appears as a HID device. This function keeps trying so callers don't
    need to handle that themselves.

    Args:
        serial:      USB serial string, e.g. "D30F103095D182300023D4D4".
                     Pass "" or None to connect to the first available arm.
        retries:     Maximum number of attempts before raising.
        retry_delay: Seconds to wait between attempts.
        label:       Human-readable name for log messages.

    Returns:
        xarm.Controller instance

    Raises:
        RuntimeError if all retries are exhausted.
    """
    port = "USB" + (serial or "")
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            ctrl = xarm.Controller(port)
            print(f"[arm_connect] {label}: connected on attempt {attempt}")
            return ctrl
        except Exception as e:
            last_error = e
            if attempt < retries:
                print(f"[arm_connect] {label}: attempt {attempt}/{retries} failed ({e}), retrying in {retry_delay}s...")
                time.sleep(retry_delay)
    raise RuntimeError(
        f"[arm_connect] {label}: failed to connect after {retries} attempts. Last error: {last_error}"
    )


class ArmConnection:
    """
    Wraps xarm.Controller with automatic keepalive and reconnection.

    The arm's onboard watchdog disconnects the USB device if no HID command
    arrives within ~26 seconds. This class sends a periodic getBatteryVoltage()
    ping to prevent that, and reconnects automatically if the arm drops.

    Usage:
        with ArmConnection(BLUE_SERIAL, label="blue") as arm:
            arm.setPosition(xarm.Servo(2, 500))
    """

    def __init__(self, serial, label="arm", connect_retries=30, connect_delay=1.0):
        self._serial = serial
        self._label = label
        self._connect_retries = connect_retries
        self._connect_delay = connect_delay
        self._ctrl = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._keepalive_thread = None

    def connect(self):
        self._ctrl = connect_arm(
            self._serial,
            retries=self._connect_retries,
            retry_delay=self._connect_delay,
            label=self._label,
        )
        self._stop_event.clear()
        self._keepalive_thread = threading.Thread(
            target=self._keepalive_loop, daemon=True
        )
        self._keepalive_thread.start()
        return self

    def disconnect(self):
        self._stop_event.set()
        if self._keepalive_thread:
            self._keepalive_thread.join(timeout=5)
        self._ctrl = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, *_):
        self.disconnect()

    def _keepalive_loop(self):
        while not self._stop_event.wait(_KEEPALIVE_INTERVAL):
            try:
                with self._lock:
                    if self._ctrl is not None:
                        self._ctrl.getBatteryVoltage()
            except Exception as e:
                print(f"[arm_connect] {self._label}: keepalive failed ({e}), reconnecting...")
                self._reconnect()

    def _reconnect(self):
        for delay in [2, 4, 8, 16]:
            try:
                ctrl = connect_arm(
                    self._serial,
                    retries=5,
                    retry_delay=delay,
                    label=self._label,
                )
                with self._lock:
                    self._ctrl = ctrl
                print(f"[arm_connect] {self._label}: reconnected")
                return
            except RuntimeError:
                pass
        print(f"[arm_connect] {self._label}: reconnection failed; will retry on next keepalive")

    # ------------------------------------------------------------------ #
    # Proxy the Controller API so callers don't need to touch self._ctrl  #
    # ------------------------------------------------------------------ #

    def setPosition(self, *args, **kwargs):
        with self._lock:
            return self._ctrl.setPosition(*args, **kwargs)

    def getPosition(self, *args, **kwargs):
        with self._lock:
            return self._ctrl.getPosition(*args, **kwargs)

    def getBatteryVoltage(self):
        with self._lock:
            return self._ctrl.getBatteryVoltage()

    def servoOff(self, *args, **kwargs):
        with self._lock:
            return self._ctrl.servoOff(*args, **kwargs)
