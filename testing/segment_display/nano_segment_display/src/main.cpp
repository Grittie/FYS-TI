#include <Arduino.h>

/*
  Showing number 0-9 on a Common Anode 7-segment LED display
      A(9)
      ---
F(8) |   | B(2)
     |   |
      --- G(7)
E(6) |   | C(3)
     |   |
      ---     .(4)
      D(5)

D1: 10
D2: 11
D3: 12
D4: 13
 */

const byte digitalPins[] = {2, 3, /*4,*/ 5, 6, 7, 8, 9};
int digitalPinLenght = 0;

const byte segmentPins[] = {10, 11, 12, 13};
int segmentPinLenght = 0;

const int buttonPin = 4;
int buttonState = 0;

int loopIndex = 0;
bool isPressed = false;

int digitalNumbers[10][8] = {
    {1, 1, /*1,*/ 1, 1, 0, 1, 1}, // 0
    {0, 0, /*0,*/ 0, 1, 0, 1, 0}, // 1
    {1, 0, /*0,*/ 1, 1, 1, 0, 1}, // 2
    {1, 1, /*0,*/ 1, 0, 1, 0, 1}, // 3
    {1, 1, /*0,*/ 0, 0, 1, 1, 0}, // 4
    {0, 1, /*0,*/ 1, 0, 1, 1, 1}, // 5
    {0, 1, /*0,*/ 1, 1, 1, 1, 1}, // 6
    {1, 1, /*0,*/ 0, 0, 0, 0, 1}, // 7
    {1, 1, /*0,*/ 1, 1, 1, 1, 1}, // 8
    {1, 1, /*0,*/ 1, 0, 1, 1, 1}, // 9
};
int dititalNumberLength = 0;
char buffer[5];

// the setup routine runs once when you press reset:
void setup()
{
  Serial.begin(9600);
  Serial.print("Setup \n");
  digitalPinLenght = sizeof(digitalPins) / sizeof(digitalPins[0]);
  segmentPinLenght = sizeof(segmentPins) / sizeof(segmentPins[0]);
  dititalNumberLength = sizeof(digitalNumbers) / sizeof(digitalNumbers[0]);

  // initialize the digital pins
  for (size_t i = 0; i < digitalPinLenght; i++)
  {
    pinMode(digitalPins[i], OUTPUT);
    digitalWrite(digitalPins[i], digitalNumbers[0][i]);
  }

  // initialize the digital pins
  for (size_t i = 0; i < segmentPinLenght; i++)
  {
    pinMode(segmentPins[i], OUTPUT);
  }

  pinMode(buttonPin, INPUT);
}

void setDitgitalNumber(int number)
{
  sprintf(buffer, "%04d", number);
  Serial.println(buffer);

  for (size_t i = 0; i < segmentPinLenght; i++)
  {
    digitalWrite(segmentPins[i], HIGH);
    for (size_t j = 0; j < segmentPinLenght; j++)
    {
      if (j != i)
      {
        digitalWrite(segmentPins[j], LOW);
      }
    }

    for (size_t j = 0; j < dititalNumberLength; j++)
    {
      int n = buffer[i] - '0';
      digitalWrite(digitalPins[j], digitalNumbers[loopIndex][j]);
    }
  }
}

void loop()
{
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == HIGH)
  {
    // turn on:
    if (!isPressed)
    {
      Serial.println("pressed?");
      setDitgitalNumber(loopIndex);
      loopIndex++;
      isPressed = true;
    }
  }
  else
  {
    // turn off:
    isPressed = false;
  }
}
