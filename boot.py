import board
import digitalio
import storage

# Only allow code.py updates when turned off
switch = digitalio.DigitalInOut(board.D7)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
storage.remount("/", not switch.value)
