# Restore STM32U585 Behavior

## Flash Problems

Using the Arduino Lab, sometimes Flashing won't work anymore. Trying a manual flash is working. Example: 

a) Compile your sketch

    arduino-cli compile --fqbn arduino:zephyr:unoq --output-dir /home/arduino/ArduinoApps/oled/.cache/sketch /home/arduino/ArduinoApps/oled/sketch/sketch.ino

b) Reallocate it:

    /home/arduino/.arduino15/packages/zephyr/tools/arm-zephyr-eabi/0.16.8/bin/arm-zephyr-eabi-objcopy --change-addresses 0x08000000 /home/arduino/ArduinoApps/blink-led/.cache/sketch/sketch.ino_debug.elf /home/arduino/ArduinoApps/blink-led/.cache/sketch/sketch.ino_debug_shifted.elf

c) Upload it:

    arduino-cli upload --fqbn arduino:zephyr:unoq -v /home/arduino/ArduinoApps/blink-led/sketch/
 *(whereby blink-led must be renamed to your sketch)*
Ruńning it in the ** Arduino-Lab**, you may get something like:

> Info : SWD DPIDR 0x0be12477
Error: error running OpenOCD: exit status 1
Error: Failed to write memory at 0x00000000
00000000
Failed uploading: uploading error: exit status 1
>
### The Reason: 
Your Arduino Lab log shows: [stm32u5.cpu] halted due to debug-request, current mode: Handler External Interrupt(61) Error: Failed to write memory at 0x00000000

The problem: The Arduino Lab/IDE is probably trying to access the chip while it's running (or via a soft reset). Since the STM32U585 immediately jumps to interrupt 61, the bus is blocked. OpenOCD then can't write to address 0x00000000 (the alias for the start of flash memory).

### Workaround:
Before flashing with the Arduino-Lab, execute in a Arduino-bash:

    /opt/openocd/bin/openocd -s /opt/openocd -f openocd_gpiod.cfg -c "init; halt; stm32u5x mass_erase 0; exit"

Then flashing is working.
