# Debug interface for Arduino (TM32U585)

While using the USB interface for SD card access and Powersupply, we can't use in the netwok mode for serial.println() debugging.

For Arduino-side "debugging", we are using a FTDI connector:

![ftdi](./ftdi.png)

	|USB-TTL  | Uno Q             |
	|TX       | Pin 	0 (RX)    |
	|RX       | Pin 	1 (TX)    |
	|GND      | GND               |
	|VCC      | ❌ do not connect |
	


## Simple Sketch for Testing

In the Arduino Lab /Apps create a new template App and copy the following code into the ino part. Run (Flash) 
and open a serial monitor (here CuteCom with 115200 baud and ttyUSB0 connector:

    void setup() {
	    Serial.begin(115200);
	    while (!Serial) { ; }   // wichtig beim Uno Q
	    Serial.println("Hello from Uno Q!");
	}
	
	void loop() {
		Serial.println("Loop running...");
		delay(1000);
	}


![cutecom](./cutecom.png)

> Written with [StackEdit](https://stackedit.io/).








