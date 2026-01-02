# Debugging with OpenOCD 

On the Linux machine, the **OpenOCD-Debugger** is preinstalled and connects via **SWD (Serial Wire Debug)** with the Arduino processor **STM32U5**) 

## PreWork to be Done

### Generating the **ELF** Outpout

Using the ** arduino-cli** command, we produce:

    arduino-cli compile --fqbn arduino:zephyr:unoq --output-dir /home/arduino/ArduinoApps/blink-led/.cache/sketch /home/arduino/ArduinoApps/blink-led/sketch/sketch.ino

 ![compileoutput](./gallery/compileoutput.png)
 
Now we can have a look to the address table

    /home/arduino/.arduino15/packages/zephyr/tools/arm-zephyr-eabi/0.16.8/bin/arm-zephyr-eabi-objdump -h /home/arduino/ArduinoApps/blink-led/.cache/sketch/sketch.ino_debug.elf
    
 ![addresstable_unshifted](./gallery/addresstable_unshifted.png)

As we see, we start at address 00000000h, but we should start at 08000000h. So we shift with objdump

    /home/arduino/.arduino15/packages/zephyr/tools/arm-zephyr-eabi/0.16.8/bin/arm-zephyr-eabi-objdump -h /home/arduino/ArduinoApps/blink-led/.cache/sketch/sketch.ino_debug_shifted.elf

in our new file *sketch.ino_debug_shifted.elf*

 ![addresstable_shifted](./gallery/addresstable_shifted.png)

A short check gives: 

    /home/arduino/.arduino15/packages/zephyr/tools/arm-zephyr-eabi/0.16.8/bin/arm-zephyr-eabi-readelf -h /home/arduino/ArduinoApps/blink-led/.cache/sketch/sketch.ino_debug_shifted.elf

 ![readelf_shifted](./gallery/readelf_shifted.png)

** Important: ** We have a REL file type! 
This means: only symbole + sections, but no program header. Therefore: 
*Size of program headers: 0    and: 
Number of program headers: 0*. 
So, this file is only a symbol container.


## Steps

### Arduino Bash
Using the Arduino-Lab or a ssh access.

### Start the GDB Server
In the bash: 

    arduino-debug -c "init" -c "reset halt"
    
The **GDB Server** runs on **Port 3333**.


The result is:

 ![gdb-server](./gallery/gdb-server.png)

Keep this Window open and open another Arduino terminal.


### Starting the Debugger

Open a new SSH bash and start the debugger with:

    /home/arduino/.arduino15/packages/zephyr/tools/arm-zephyr-eabi/0.16.8/bin/arm-zephyr-eabi-gdb

We will get the debugger console:

 ![gdb-client](./gallery/gdb.png)

### Load Firmware
With the GDB console, we have to load the board firmware:

    file ~/.arduino15/packages/arduino/hardware/zephyr/0.52.0/firmwares/zephyr-arduino_uno_q_stm32u585xx.elf

Showing:
 ![firmware](./gallery/firmware.png)


###




Normally the sketches are located on the Arduino in:
~/ArduinoApps/name of your sketch/.cache/sketch
so you evoke the debugger with
   

In _debug.elf, you have the symbols. We get something like this:



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

#### Break at a function

By default, GDB prefers **software breakpoints** (patching code).  
On MCUs this sometimes fails.

##### Force hardware breakpoints (STM32U5 supports 8):

    (gdb) hbreak setup
    (gdb) hbreak loop

Loop part of the sketch:

 ![sketch1](./gallery/ino1.png)


 ![hwbreakpoints](./gallery/hwbreakpoints.png)

and
 
 ![hwbreakpoints1](./gallery/ourbreakpoints.png)

Now we have set our breakpoints and restart the MCU

    (gdb)  monitor reset halt

 ![reset](./gallery/reset.png)

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



> Written with [StackEdit](https://stackedit.io/).
