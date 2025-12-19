# Debugging with OpenOCD 

On the Linux machine, the **OpenOCD-Debugger** is preinstalled and connects via **SWD (Serial Wire Debug)** with the Arduino processor **STM32U5**) 
For proper usage, we must install first:

    sudo apt update
    sudo apt install gdb-multiarch

The **GDB Server** runs on **Port 3333**.

## Steps

### Arduino Bash
Using the Arduino-Lab or a ssh access.

### Start the GDB Server
In the bash: 

    arduino-debug
The result is:
 
> Open On-Chip Debugger 0.12.0+dev-ge6a2c12f4 (2025-05-22-15:51) Licensed under GNU GPL v2 For bug reports, read http://openocd.org/doc/doxygen/bugs.html debug_level: 2 clock_config Info : Linux GPIOD JTAG/SWD bitbang driver (libgpiod v2) Info : Note: The adapter "linuxgpiod" doesn't support configurable speed Info : SWD DPIDR 0x0be12477 Info : [stm32u5.ap0] Examination succeed Info : [stm32u5.cpu] Cortex-M33 r0p4 processor detected Info : [stm32u5.cpu] target has 8 breakpoints, 4 watchpoints Info : [stm32u5.cpu] Examination succeed Info : [stm32u5.ap0] gdb port disabled Info : [stm32u5.cpu] starting gdb server on 3333 Info : Listening on port 3333 for gdb connections Info : Listening on port 6666 for tcl connections Info : Listening on port 4444 for telnet connections CPU in Non-Secure state [stm32u5.cpu] halted due to breakpoint, current mode: Thread xPSR: 0x09000000 pc: 0x08006374 psp: 0x20034a70. Then, in a second shell, i start gdb-multiarch ~/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf in a gdb shell. Entering **No connections**.

Keep this Window open. The ** The no connection** problem, we are solving in the next steps.


### Start the Debugger

Normally the sketches are located on the Arduino in:
~/ArduinoApps/name of your sketch/.cache/sketch
so you evoke the debugger with
   
    gdb-multiarch ~/ArduinoApps/<name of your sketch>/.cache/sketch/sketch.ino_debug.elf
In _debug.elf, you have the symbols. We get something like this:

> GNU gdb (Debian 16.3-1) 16.3
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "aarch64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf...

As an result, you are seeing the debugger shell as (gdb).


### In the Debugger Shell:

Connect to the GDB Server

    (gdb) target remote localhost:3333

As a result, in the GDB server window, a line is added:

    Info : New GDB Connection: 1, Target stm32u5.cpu, state: halted

### Make GDB understand your program

Once connected:

    (gdb) file ~/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf

This ensures:
-   symbols are loaded

-   source lines are mapped
    
-   variables are visible

### Verifying the Setup

    (gdb) info files
You get something like:

> Symbols from "/home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf".
Remote target using gdb-specific protocol:
	`/home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf', file type elf32-littlearm.
	Entry point: 0x16a4
	0x00000000 - 0x00001b7c is .text
	0x00001b7c - 0x00001d5c is .rodata
	0x00001d5c - 0x00001d74 is .data
	0x00001d74 - 0x00002888 is .bss
	0x00002888 - 0x00002890 is .exported_sym
	0x00002890 - 0x000028a0 is .init_array
	While running this, GDB does not access memory from...
Local exec file:
	`/home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf', file type elf32-littlearm.
	Entry point: 0x16a4
	0x00000000 - 0x00001b7c is .text
	0x00001b7c - 0x00001d5c is .rodata
	0x00001d5c - 0x00001d74 is .data
	0x00001d74 - 0x00002888 is .bss
	0x00002888 - 0x00002890 is .exported_sym
	0x00002890 - 0x000028a0 is .init_array

    (gdb) info functions loop
You get:

> ll functions matching regular expression "loop":

File /home/arduino/ArduinoApps/heartratemonitor/sketch/sketch.ino:
71:	void loop();
(gdb) info sources
/home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf:
(Full debug information has not yet been read for this file.)

/home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch/sketch.ino.cpp, /home/arduino/ArduinoApps/heartratemonitor/sketch/sketch.ino, 
... and so on

    (gdb) info sources

> /home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf:
(Full debug information has not yet been read for this file.)
/home/arduino/ArduinoApps/heartratemonitor/.cache/sketch/sketch/sketch.ino.cpp, /home/arduino/ArduinoApps/heartratemonitor/sketch/sketch.ino, 
/home/arduino/.arduino15/packages/arduino/hardware/zephyr/0.52.0/cores/arduino/zephyrSerial.h, 
... and so on

### Debugging

    (gdb) info registers
We get:

> r0             0x1                 1
r1             0x20034a5c          537086556
r2             0x3580              13696
r3             0x2341              9025
r4             0x20035490          537089168
r5             0x802b6d8           134395608
r6             0x8e98              36504
r7             0x0                 0
r8             0x8021388           134353800
r9             0xa350              41808
r10            0xffffffff          -1
r11            0xffffffff          -1
r12            0x0                 0
sp             0x20034a70          0x20034a70
lr             0x8016e79           134311545
pc             0x8006374           0x8006374
xpsr           0x9000000           150994944
fpscr          0x0                 0
... and so on


### Breakpoint Handling

#### Break at a source line

    (gdb) break sketch.ino:82  (example)
   

break <line number>

#### Removing a Breakpoint

    (gdb) info breakpoints



> Written with [StackEdit](https://stackedit.io/).
