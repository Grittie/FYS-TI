#include <Arduino.h>

/*
  Showing number 0-9 on a Common Anode 7-segment LED display
    A
   ---
F |   | B
  | G |
   ---
E |   | C
  |   |
   ---
    D
 */

int pins[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};
int pinLength = 0;

// the setup routine runs once when you press reset:
void setup()
{
  pinLength = sizeof(pins) / sizeof(pins[0]);

  // initialize the digital pins as outputs.
  for (size_t i = 0; i < pinLength; i++)
  {
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], HIGH);
  }
}
