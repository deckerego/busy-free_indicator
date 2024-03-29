# The Busy/Free Desk Indicator 2021 Edition

A busy/free desktop indicator for the Adafruit Circuit Playground Express.

Button A increments the busy indicator by 15 minutes on each press, button B decrements it by 15. Once the timer has lapsed, the indicator goes back to blue. You can shake to clear the timer, and the switch toggles the lights on or off.


## Hardware Build Instructions

All this build needs is an [Adafruit Circuit Playground Express](https://www.adafruit.com/product/3333), a USB cable, and optionally an [enclosure](https://www.adafruit.com/product/3333) to make it look cool.

Note that CircuitPython 6.1 has an issue with mounting USB storage that causes code to halt if the Circuit Playground is mounted in read-only mode. To avoid this, make sure you have CircuitPython 6.2.0 or higher installed.

See the [hackaday.io Project Page](https://hackaday.io/project/175732-busyfree-desk-indicator) for build instructions.


## Usage

The Playground Express switch allows you to turn the lights on or off. When you first turn the unit on, you should see The Busy/Free Desk Indicator 2021 Edition turn blue to indicate you are idle.

To indicate you are busy, press the “A” button until the unit turns red and the wait indicator is shown. With every press of the “A” button, you will add 15 minutes to the busy timer. After the busy timer has counted all the way back down, Playground Express will turn back to blue and things go back to normal.

While the busy indicator is on, you can press the “B” button to decrement the timeout period by 15 minutes for each press. Shaking Playground Express will remove the timeout period and set you back to idle.

Pressing the "B" button while idle will change the LED animation cycle to something more interesting or annoying.

## Installing

First make sure that your Circuit Playground Express has the
[latest version of CircuitPython installed](https://circuitpython.org/board/adafruit_macropad_rp2040/).
See [https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-quickstart](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-quickstart)
for instructions on how to update the Circuit Playground Express to have the latest version of
CircuitPython.

When installing the Busy/Free Indicator for the first time, extract the latest
[CIRCUITPY.ZIP](https://github.com/deckerego/busy-free_indicator/releases/latest)
into a directory, then copy the contents of that extracted archive
into the CIRCUITPY drive that appears when you plug in your Circuit Playground Express.
Ensure that the contents of the `lib/` subdirectory are also copied - these are
the precompiled Adafruit libraries that power the Playground Express.


## Updating the Software

So that the Playground Express doesn't keep restarting itself while it is mounted/unmounted, the boot.py script will mark the filesystem as read only when the switch is in the "on" position, and read/write in the "off" position. If you want to update code.py, you should first turn the switch to the "off" position and reboot the Playground Express by pressing the reset button in the middle.

After you have updated the code, moving the switch to the "on" position and rebooting the Playground Express will once again set the device to read-only and won't auto-reload.


## Additional Documentation

See the [printable User's Guide](https://docs.google.com/document/d/1Aq5RcLSJUTe7unPQ9NFNM568gAli1XiDiWOW0XTifgc/) if you want more sarcastic documentation.
