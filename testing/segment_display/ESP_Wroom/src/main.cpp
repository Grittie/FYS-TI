#include <Arduino.h>
#include "SevSeg.h"
SevSeg sevseg;

TaskHandle_t Task1;
TaskHandle_t Task2;

int number = 0;
char buffer[5];

byte digitPins[] = {4, 0, 2, 15};
byte segmentPins[] = {20, 12, 33, 26, 27, 14, 32, 25};

int relayPins[] = {19, 5};
int relayCooldown[] = {0, 0};
int relayUpTime = 1;

int relayIndex = 1;
int relayLength = 0;

int buttonPin = 13;
int buttonState = 0;
bool isPressed = false;
int pressDelay = 10;
int currentPressDelay = 0;

void enable_relay()
{
  relayIndex = relayIndex < relayLength - 1 ? relayIndex + 1 : 0;
  if (relayCooldown[relayIndex] <= 0)
  {
    //Serial.printf("TURN ON: %d \n", relayPins[relayIndex]);
    digitalWrite(relayPins[relayIndex], HIGH);
    relayCooldown[relayIndex] = relayUpTime;
  }
}

void update_counter()
{
  enable_relay();
  sprintf(buffer, "%04d", number);
  sevseg.setChars(buffer);
}

void set_number(int num)
{
  number = num;
  update_counter();
}

void add_number(int amount)
{
  number += amount;
  update_counter();
}

void subtract_number(int amount)
{
  add_number(-amount);
}

void reset()
{
  number = 0;
  sprintf(buffer, "%04d", number);
  sevseg.setChars(buffer);
}

void Task1code(void *pvParameters)
{
  Serial.print("Task1 running on core ");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    buttonState = digitalRead(buttonPin);
    if (buttonState == LOW)
    {
      if (!isPressed && currentPressDelay <= 0)
      {
        isPressed = true;
        currentPressDelay = pressDelay;
        add_number(1);
      }
    }
    else
    {
      isPressed = false;
      if (currentPressDelay > 0)
      {
        currentPressDelay--;
      }
    }
    sevseg.refreshDisplay();
    delay(1);
  }
}

void Task2code(void *pvParameters)
{
  Serial.print("Task2 running on core ");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    for (size_t i = 0; i < relayLength; i++)
    {
      if (relayCooldown[i] == 0)
      {
        digitalWrite(relayPins[i], LOW);
        relayCooldown[i] = 0;
        // Serial.printf("Turn off: %d\n", relayPins[relayIndex]);
      }
      else if (relayCooldown[i] > 0)
      {
        relayCooldown[i]--;
        // Serial.printf("Count: %d | %d\n", relayPins[relayIndex], relayCooldown[i]);
      }
    }

    delay(200);
  }
}

void setup()
{
  Serial.begin(115200);

  // Create threads
  xTaskCreatePinnedToCore(Task1code, "Task1", 10000, NULL, 1, &Task1, 0);
  delay(500);
  xTaskCreatePinnedToCore(Task2code, "Task2", 10000, NULL, 1, &Task2, 1);
  delay(500);

  // Setup the values
  byte numDigits = sizeof(digitPins) / sizeof(digitPins[0]);
  relayLength = sizeof(relayPins) / sizeof(relayPins[0]);
  bool resistorsOnSegments = 0;
  currentPressDelay = pressDelay;

  // Setup the pins
  pinMode(buttonPin, INPUT_PULLUP);
  for (size_t i = 0; i < relayLength; i++)
  {
    pinMode(relayPins[i], OUTPUT);
  }

  // Setup the segment display
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);

  reset();
  for (size_t i = 0; i < 10; i++)
  {
      delay(500);
      add_number(1);
  }
}

void loop()
{
}