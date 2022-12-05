#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define HIGH 1
#define LOW 0

int relay_pins[] = {4, 9};
int relayLength = 0;
int loopIndex = 0;
int up_length = 800;

void app_main()
{
    relayLength = sizeof(relay_pins) / sizeof(relay_pins[0]);
    for (size_t i = 0; i < relayLength; i++)
    {
        gpio_set_direction(relay_pins[i], GPIO_MODE_OUTPUT);
    }

    while (true)
    {
        toggle_relay();
    }
}

void toggle_relay() {
    // Turn the relay on
    gpio_set_level(relay_pins[loopIndex], HIGH);

    // Add a delay before turning it off
    vTaskDelay(up_length / portTICK_PERIOD_MS);

    // turn the relay off
    gpio_set_level(relay_pins[loopIndex], LOW);
    loopIndex = loopIndex < relayLength - 1 ? loopIndex + 1 : 0;
}