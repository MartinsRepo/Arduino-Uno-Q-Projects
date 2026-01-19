#include <SPI.h>
#include "Arduino_RouterBridge.h"

// -------------------------------------------------
// Pin definitions for the ST7789 display
// -------------------------------------------------
const int PIN_CS  = 10; // Chip Select (active LOW)
const int PIN_RES = 9;  // Hardware reset pin
const int PIN_DC  = 8;  // Data/Command select pin

// -------------------------------------------------
// ST7789 command definitions
// -------------------------------------------------
#define SWRESET   0x01  // Software reset
#define SLPOUT    0x11  // Exit sleep mode
#define COLMOD    0x3A  // Color mode
#define MADCTL    0x36  // Memory access control
#define CASET     0x2A  // Column address set
#define RASET     0x2B  // Row address set
#define RAMWR     0x2C  // Memory write
#define DISPON    0x29  // Display on

// -------------------------------------------------
// Display resolution
// -------------------------------------------------
#define TFT_WIDTH  280
#define TFT_HEIGHT 250

// -------------------------------------------------
// Color definitions (RGB565 format)
// -------------------------------------------------
#define BLACK 0x0000
#define WHITE 0xFFFF

// -------------------------------------------------
// Display coordinate offsets
// (needed because the panel origin is shifted)
// -------------------------------------------------
#define X_OFFSET 20
#define Y_OFFSET -25 

// -------------------------------------------------
// Font scaling factor
// -------------------------------------------------
#define SCALE 2

// -------------------------------------------------
// Font layout parameters
// -------------------------------------------------
#define FONT_WIDTH   5
#define FONT_HEIGHT  7
#define FONT_SPACING 1 // Space between characters

// -------------------------------------------------
// 5x7 font table (ASCII 32–127)
// Stored in flash memory (PROGMEM)
// -------------------------------------------------
#include <avr/pgmspace.h>

const uint8_t font5x7[][5] PROGMEM = {
  {0x00,0x00,0x00,0x00,0x00}, // 32 ' '
  {0x00,0x00,0x5F,0x00,0x00}, // 33 '!'
  {0x00,0x07,0x00,0x07,0x00}, // 34 '"'
  {0x14,0x7F,0x14,0x7F,0x14}, // 35 '#'
  {0x24,0x2A,0x7F,0x2A,0x12}, // 36 '$'
  {0x23,0x13,0x08,0x64,0x62}, // 37 '%'
  {0x36,0x49,0x55,0x22,0x50}, // 38 '&'
  {0x00,0x05,0x03,0x00,0x00}, // 39 '''
  {0x00,0x1C,0x22,0x41,0x00}, // 40 '('
  {0x00,0x41,0x22,0x1C,0x00}, // 41 ')'
  ...
  {0x00,0x00,0x00,0x00,0x00}  // 127 DEL
};

// -------------------------------------------------
// Low-level SPI helpers
// -------------------------------------------------

// Send a command byte to the display
void sendCommand(uint8_t cmd) {
  digitalWrite(PIN_DC, LOW);   // Command mode
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(cmd);
  digitalWrite(PIN_CS, HIGH);
}

// Send a data byte to the display
void sendData(uint8_t data) {
  digitalWrite(PIN_DC, HIGH);  // Data mode
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(data);
  digitalWrite(PIN_CS, HIGH);
}

// -------------------------------------------------
// Define drawing window on the display
// -------------------------------------------------
void setWindow(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {
  // Apply panel-specific offsets
  x0 += X_OFFSET;
  x1 += X_OFFSET;
  y0 += Y_OFFSET;
  y1 += Y_OFFSET;

  // Set column range
  sendCommand(CASET);
  sendData(x0 >> 8); sendData(x0 & 0xFF);
  sendData(x1 >> 8); sendData(x1 & 0xFF);

  // Set row range
  sendCommand(RASET);
  sendData(y0 >> 8); sendData(y0 & 0xFF);
  sendData(y1 >> 8); sendData(y1 & 0xFF);

  // Prepare for RAM write
  sendCommand(RAMWR);
}

// -------------------------------------------------
// Drawing primitives
// -------------------------------------------------

// Draw a single pixel
void drawPixel(uint16_t x, uint16_t y, uint16_t color) {
  if (x >= TFT_WIDTH || y >= TFT_HEIGHT) return;

  setWindow(x, y, x, y);
  digitalWrite(PIN_DC, HIGH);
  digitalWrite(PIN_CS, LOW);
  SPI.transfer(color >> 8);
  SPI.transfer(color & 0xFF);
  digitalWrite(PIN_CS, HIGH);
}

// Fill the entire screen with one color
void fillScreen(uint16_t color) {
  setWindow(0, 0, TFT_WIDTH - 1, TFT_HEIGHT - 1);
  digitalWrite(PIN_DC, HIGH);
  digitalWrite(PIN_CS, LOW);

  for (uint32_t i = 0; i < (uint32_t)TFT_WIDTH * TFT_HEIGHT; i++) {
    SPI.transfer(color >> 8);
    SPI.transfer(color & 0xFF);
  }
  digitalWrite(PIN_CS, HIGH);
}

// -------------------------------------------------
// Font rendering
// -------------------------------------------------

// Draw a single scaled character
void drawCharScaled(
  uint16_t x,
  uint16_t y,
  char c,
  uint16_t color,
  uint8_t scale
) {
  if (c < 32 || c > 127) return;

  const uint8_t *bitmap = font5x7[c - 32];

  for (uint8_t col = 0; col < 5; col++) {
    uint8_t line = pgm_read_byte(&bitmap[col]);

    for (uint8_t row = 0; row < 7; row++) {
      if (line & 0x01) {
        // Draw scaled pixel block
        for (uint8_t dx = 0; dx < scale; dx++) {
          for (uint8_t dy = 0; dy < scale; dy++) {
            drawPixel(
              x + col * scale + dx,
              y + row * scale + dy,
              color
            );
          }
        }
      }
      line >>= 1;
    }
  }
}

// Draw text without line wrapping
void drawTextScaled(
  uint16_t x,
  uint16_t y,
  const char *text,
  uint16_t color,
  uint8_t scale
) {
  uint16_t cursorX = x;

  while (*text) {
    drawCharScaled(cursorX, y, *text++, color, scale);
    cursorX += (5 + 1) * scale; // Character width + spacing
  }
}

// Draw text with automatic line wrapping
void drawTextWrapped(
  uint16_t x,
  uint16_t y,
  const char *text,
  uint16_t color,
  uint8_t scale
) {
  uint16_t cursorX = x;
  uint16_t cursorY = y;

  const uint16_t charWidth  = (FONT_WIDTH + FONT_SPACING) * scale;
  const uint16_t charHeight = FONT_HEIGHT * scale;

  while (*text) {
    char c = *text++;

    // Explicit newline
    if (c == '\n') {
      cursorX = x;
      cursorY += charHeight + 5;
      continue;
    }

    // Automatic line break
    if (cursorX + charWidth > TFT_WIDTH) {
      cursorX = x;
      cursorY += charHeight + 5;
    }

    // Stop drawing if screen is full
    if (cursorY + charHeight > TFT_HEIGHT) {
      break;
    }

    drawCharScaled(cursorX, cursorY, c, color, scale);
    cursorX += charWidth;
  }
}

// -------------------------------------------------
// Function called from Python via RouterBridge
// -------------------------------------------------
void printFromPython(String text) {
  // Clear the screen
  fillScreen(BLACK);

  // Convert Arduino String to C string and draw it
  drawTextWrapped(20, 40, text.c_str(), WHITE, 2);
}

// -------------------------------------------------
// Arduino setup
// -------------------------------------------------
void setup() {
  // Configure control pins
  pinMode(PIN_CS, OUTPUT);
  pinMode(PIN_RES, OUTPUT);
  pinMode(PIN_DC, OUTPUT);

  SPI.begin();
  // 10 MHz SPI clock
  SPI.beginTransaction(SPISettings(10000000, MSBFIRST, SPI_MODE0));

  Serial.begin(115200);
  Serial.println("Display signal test started...");

  // Hardware reset sequence
  digitalWrite(PIN_RES, LOW);
  delay(50);
  digitalWrite(PIN_RES, HIGH);
  delay(150);

  // Display initialization
  sendCommand(SWRESET);
  delay(150);

  sendCommand(SLPOUT);
  delay(150);

  sendCommand(COLMOD);
  sendData(0x55); // RGB565 color mode

  sendCommand(MADCTL);
  sendData(0xA0); // Display orientation

  sendCommand(DISPON);
  delay(100);

  fillScreen(BLACK);

  // Register Python bridge function
  Bridge.begin();
  Bridge.provide("display_print", printFromPython);
}

// -------------------------------------------------
// Main loop (unused)
// -------------------------------------------------
void loop() {
}

