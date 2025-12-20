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
 ![gdb-server](./gallery/gdb-server.png.png)

Keep this Window open and open another Arduino terminal.


### Start the Debugger

Normally the sketches are located on the Arduino in:
~/ArduinoApps/name of your sketch/.cache/sketch
so you evoke the debugger with
   
    gdb-multiarch ~/ArduinoApps/<name of your sketch>/.cache/sketch/sketch.ino_debug.elf
In _debug.elf, you have the symbols. We get something like this:

 ![gdb-client](./gallery/gdb-multiarch.png)

As an result, you are seeing the debugger shell as (gdb).


### In the (gdb) Debugger Shell:

Connect to the GDB Server

    (gdb) target remote localhost:3333

As a result, you see:

 ![connectingt](./gallery/connecting.png)

### Make GDB understand your program

Once connected:

    (gdb) file ~/ArduinoApps/heartratemonitor/.cache/sketch/sketch.ino_debug.elf

This ensures:
-   symbols are loaded

-   source lines are mapped
    
-   variables are visible

### Verifying the Setup

    (gdb) info files
You get something like this:
 ![info files](./gallery/infofiles.png)


    (gdb) info function loop

You get:

 ![info function](./gallery/infofunction.png)
 
This works also with library functions.

    (gdb) info sources
We get the dependencies of all files included:

 ![info sources](./gallery/infosources.png)


### Debugging

    (gdb) info registers

We get for example:

 ![info register](./gallery/inforegister.png)


### Breakpoint Handling

#### Check for breakpoints

    (gdb) info breakpoint

If nothing is set, we see:
 
 ![no breakpoint](./gallery/nobreakpoint.png)


#### Break at a source line

    (gdb) break sketch.ino:82  (example)
   

break <line number>

#### Removing a Breakpoint

    (gdb) info breakpoints

> Breakpoint 1 at 0x45a: file /home/arduino/ArduinoApps/heartratemonitor/sketch/sketch.ino, line 82.
(gdb) info breakpoints
Num     Type           Disp Enb Address    What
1       breakpoint     keep y   0x0000045a in loop() 
                                           at /home/arduino/ArduinoApps/heartratemonitor/sketch/sketch.ino:82

> 
> 
> Written with [StackEdit](https://stackedit.io/).

