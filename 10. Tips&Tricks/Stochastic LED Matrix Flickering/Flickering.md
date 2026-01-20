## Stochastic LED Matrix Flickering

### Reason
During boot, the STM32 is in an undefined state if no valid sketch or bridge firmware is active. The noise on the data lines is then interpreted as random lighting of the matrix. The "inverted figure eight" is part of the default factory firmware.

### Solution

***Flash the Firmware***
 (1) Create:

    adb shell
    cd /home/arduino/.arduino15/packages/arduino/hardware/zephyr/0.52.0/firmwares/
    ln -s zephyr-arduino_uno_q_stm32u585xx.bin zephyr-arduino_uno_q_stm32u585xx.elf-zsk.bin
    sudo mkdir -p /data/local/tmp
    sudo chown -R $USER /data
    exit
(2) Upload the Bootloader 

    `/opt/openocd/bin/openocd -s /opt/openocd -f openocd_gpiod.cfg -c "init; halt; program /home/arduino/.arduino15/packages/arduino/hardware/zephyr/0.52.0/firmwares/zephyr-arduino_uno_q_stm32u585xx.bin 0x08000000 verify reset exit"

 ![upload](./gallery/upload.png)

***Restore The LED Matrix***
In an Arduino shell, you find a LED Matrix example

    cd ~/.arduino15/packages/arduino/hardware/zephyr/0.52.0/libraries/Arduino_LED_Matrix/examples/Basic
(1) First install the library:

    arduino-cli lib install "ArduinoGraphics"
and then
(2) Build and upload the example:

    arduino-cli compile -b arduino:zephyr:unoq /home/arduino/.arduino15/packages/arduino/hardware/zephyr/0.52.0/libraries/Arduino_LED_Matrix/examples/Basic/Basic.ino
and

    arduino-cli upload -p /dev/ttyACM0 -b arduino:zephyr:unoq /home/arduino/.arduino15/packages/arduino/hardware/zephyr/0.52.0/libraries/Arduino_LED_Matrix/examples/Basic/Basic.ino
The result is a textual display on the Led Matrix, not the standard one.



Written with [StackEdit](https://stackedit.io/).

