#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define HIGH 1
#define LOW 0

int relayPins[] = {10, 11};
int relayLength = 0;
int relayIndex = 0;
int up_length = 800;

void enable_relay() {
    // Turn the relay on
    gpio_set_level(relayPins[relayIndex], HIGH);

    // Add a delay before turning it off
    vTaskDelay(up_length / portTICK_PERIOD_MS);

    // turn the relay off
    gpio_set_level(relayPins[relayIndex], LOW);
    relayIndex = relayIndex < relayLength - 1 ? relayIndex + 1 : 0;
}

void app_main()
{
    relayLength = sizeof(relayPins) / sizeof(relayPins[0]);
    for (size_t i = 0; i < relayLength; i++)
    {
        gpio_set_direction(relayPins[i], GPIO_MODE_OUTPUT);
    }

    while (true)
    {
        enable_relay();
    }
}