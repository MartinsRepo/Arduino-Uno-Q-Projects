#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/kernel.h>
#include <stm32u5xx.h>

#define FIRST_PIN 8
#define LAST_PIN  13
#define LED_COUNT (LAST_PIN - FIRST_PIN + 1)

#define USER_NODE DT_PATH(zephyr_user)

/* Compile-time pin extraction */
static const struct gpio_dt_spec leds[LED_COUNT] = {
    GPIO_DT_SPEC_GET_BY_IDX(USER_NODE, digital_pin_gpios, 8),
    GPIO_DT_SPEC_GET_BY_IDX(USER_NODE, digital_pin_gpios, 9),
    GPIO_DT_SPEC_GET_BY_IDX(USER_NODE, digital_pin_gpios, 10),
    GPIO_DT_SPEC_GET_BY_IDX(USER_NODE, digital_pin_gpios, 11),
    GPIO_DT_SPEC_GET_BY_IDX(USER_NODE, digital_pin_gpios, 12),
    GPIO_DT_SPEC_GET_BY_IDX(USER_NODE, digital_pin_gpios, 13),
};

/* LED-Status für Python-Bridge */
static bool led_states[LED_COUNT] = {0};

void setup()
{
    printk("Starting Zephyr LED Port Test\n");

    for (int i = 0; i < LED_COUNT; i++) {
        const auto &led = leds[i];
        int ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT);
        if (ret != 0) {
            printk("Failed to configure pin %d\n", FIRST_PIN + i);
        } else {
            printk("Configured D%d on %s pin %d\n", FIRST_PIN + i,
                   led.port->name, led.pin);
        }
    }
}

void loop()
{
    for (int i = 0; i < LED_COUNT; i++) {
        const auto &led = leds[i];
        led_states[i] = !led_states[i];               // Status toggeln
        gpio_pin_set_dt(&led, led_states[i]);         // LED schalten
        printk("D%d -> %s = %d\n", FIRST_PIN + i,
               led.port->name, led_states[i]);
        
        // Optional: Python Bridge aufrufen
        // Bridge.call("set_led_state", FIRST_PIN + i, led_states[i]);
    }
    k_msleep(500);
}
