#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void app_main() {
    int btnPins [] = {4,5,6,7,15,16,17};
    for (int i = 0; i < 6; i++) {
        gpio_set_direction(btnPins[i], GPIO_MODE_INPUT);
    }
    while (true) {
        if (gpio_get_level(4)) {
            printf("0x01_129\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(4)) {
            //     printf("0x01_1\n");
            // }
        } 
        if (gpio_get_level(5)) {
            printf("0x01_130\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(5)) {
            //     printf("0x01_2\n");
            // }
        } 
        if (gpio_get_level(6)) {
            printf("0x01_132\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(6)) {
            //     printf("0x01_4\n");
            // }
        }
        if (gpio_get_level(7)) {
            printf("0x01_136\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(7)) {
            //     printf("0x01_8\n");
            // }
        }
        if (gpio_get_level(15)) {
            printf("0x01_144\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(15)) {
            //     printf("0x01_16\n");
            // }
        }
        if (gpio_get_level(16)) {
            printf("0x01_160\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(16)) {
            //     printf("0x01_32\n");
            // }
        }
        if (gpio_get_level(17)) {
            printf("0x01_192\n");
            // vTaskDelay(100 / portTICK_PERIOD_MS);
            // if (!gpio_get_level(17)) {
            //     printf("0x01_64\n");
            // }
        } 
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}
