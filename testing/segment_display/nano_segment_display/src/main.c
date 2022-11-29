// #include "freertos/FreeRTOS.h"
// #include "freertos/task.h"
// #include "driver/gpio.h"
  
// void app_main() {
//     int pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
//     for (size_t i = 0; i < sizeof(pins); i++)
//     {
//         gpio_set_direction(pins[i], GPIO_MODE_OUTPUT);
//     }

//     for (size_t i = 0; i < pinLength; i++)
//     {
//         gpio_set_level(pins[i], 1);
//     }
// }