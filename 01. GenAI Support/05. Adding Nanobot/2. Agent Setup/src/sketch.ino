#include <MsgPack.h>
#include <Arduino_RouterBridge.h>

String storedPrompt = "Give a short description of AI agent technolgy";

// Called by Python
String get_prompt() {
    String temp = storedPrompt;
    storedPrompt = "";   // Clear after sending once
    return temp;
}

// Called by Python
bool set_response(String response) {
    Serial.println("===== Nanobot response =====");
    Serial.println(response);
    Serial.println("============================");
    return true;
}

void setup() {
    Serial.begin(115200);
    Bridge.begin();

    Bridge.provide("nanobot/get_prompt", get_prompt);
    Bridge.provide("nanobot/set_response", set_response);
}

void loop() {
    // nothing required
}
