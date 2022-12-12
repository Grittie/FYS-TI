#include <Arduino.h>
#include "SevSeg.h"
SevSeg sevseg;

TaskHandle_t Task1;
TaskHandle_t Task2;

int number = 0;
char buffer[5];

byte digitPins[] = {4, 5, 6, 7};
byte segmentPins[] = {9, 46, 16, 18, 8, 3, 15, 17};

int relayPins[] = {10, 11};
int relayCooldown[] = {0, 0};
int relayUpTime = 100;

int relayIndex = 1;
int relayLength = 0;

int buttonPin = 13;
int buttonState = 0;
bool isPressed = false;
int pressDelay = 10;
int currentPressDelay = 0;

void enable_relay()
{
  if (relayCooldown[relayIndex] <= 0)
  {
    Serial.printf("TURN ON: %d \n", relayPins[relayIndex]);
    digitalWrite(relayPins[relayIndex], HIGH);
    relayCooldown[relayIndex] = relayUpTime;
  }
  relayIndex = relayIndex < relayLength - 1 ? relayIndex + 1 : 0;
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

  while (true)
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

  while (true)
  {
    for (size_t i = 0; i < relayLength; i++)
    {
      // Serial.printf("Relay check %d: %d\n", i, relayCooldown[i]);
      if (relayCooldown[i] > 0)
      {
        // Serial.printf("Relay cooldown %d: %d\n", i, relayCooldown[i]);
        relayCooldown[i]--;

        if (relayCooldown[i] <= 0)
        {
          // Serial.printf("Relay cooldown over %d: %d\n", i, relayCooldown[i]);
          digitalWrite(relayPins[relayIndex], LOW);
          relayCooldown[i] = 0;
        }
      }
    }
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
}

void loop()
{
}