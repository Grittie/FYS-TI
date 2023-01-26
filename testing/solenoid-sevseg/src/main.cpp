#include <Arduino.h>
#include "SevSeg.h"
SevSeg sevseg;

TaskHandle_t Task1;
TaskHandle_t Task2;

int score = 0;
char buffer[5];

byte digitPins[] = {15, 2, 0, 4};
byte segmentPins[] = {13, 14, 33, 26, 27, 12, 32, 25};

int relayPins[] = {19, 18};
int relayCooldown[] = {0, 0};
int relayUpTime = 1;

int relayIndex = 1;
int relayLength = 0;

int buttonPin = 5;
int buttonLedPin = 21;
int buttonState = 0;
int buttonPressedState = LOW;
bool isPressed = false;
int pressDelay = 500;
int currentPressDelay = 0;

/// @brief Increase the relay index
void next_relay() {
  relayIndex = relayIndex < relayLength - 1 ? relayIndex + 1 : 0;
} 

/// @brief Method which enables the next relay in the index
void enable_relay()
{
  if (relayCooldown[relayIndex] <= 0)
  {
    next_relay();
    Serial.printf("TURN ON: %d \n", relayPins[relayIndex]);
    digitalWrite(relayPins[relayIndex], HIGH);
    relayCooldown[relayIndex] = relayUpTime;
  } 
}

/// @brief Method to update the score and the seven Segment Display
void update_score()
{
  enable_relay();
  sprintf(buffer, "%04d", score);
  sevseg.setChars(buffer);
}

/// @brief Method to set the value of the 7Segment Display
/// @param num Amount to set the score to
void set_score(int num)
{
  score = num;
  update_score();
}

/// @brief Method to add to the current score amount
/// @param amount  
void add_score(int amount)
{
  score += amount;
  update_score();
}

void subtract_score(int amount)
{
  add_score(-amount);
}

void reset()
{
  score = 0;
  sprintf(buffer, "%04d", score);
  sevseg.setChars(buffer);
}

void Task1code(void *pvParameters)
{
  Serial.print("Task1 running on core ");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    buttonState = digitalRead(buttonPin);
    if (buttonState == buttonPressedState)
    {
      if (!isPressed && currentPressDelay <= 0)
      {
        isPressed = true;
        currentPressDelay = pressDelay;
        add_score(1);
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

    if (currentPressDelay > 0) {
      digitalWrite(buttonLedPin, LOW);
    } else {
      digitalWrite(buttonLedPin, HIGH);
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
      if (relayCooldown[i] > 0)
      {
        digitalWrite(relayPins[i], LOW);
        relayCooldown[i] = 0;
        Serial.printf("Turn off: %d\n", relayPins[i]);
      }
      else if (relayCooldown[i] > 0)
      {
        relayCooldown[i]--;
      }
    }
    delay(500);
  }
}

void setup()
{
  Serial.begin(115200);
  delay(200);

  Serial.println("Start");
  // Create threads
  xTaskCreatePinnedToCore(Task1code, "Task1", 10000, NULL, 1, &Task1, 0);
  delay(200);
  xTaskCreatePinnedToCore(Task2code, "Task2", 10000, NULL, 1, &Task2, 1);
  delay(200);

  // Setup the values
  byte numDigits = sizeof(digitPins) / sizeof(digitPins[0]);
  relayLength = sizeof(relayPins) / sizeof(relayPins[0]);
  bool resistorsOnSegments = false;
  currentPressDelay = pressDelay;

  // Setup the pins
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonLedPin, GPIO_MODE_OUTPUT);

  for (size_t i = 0; i < relayLength; i++)
  {
    Serial.printf("Pin: %d\n", relayPins[i]);
    pinMode(relayPins[i], GPIO_MODE_OUTPUT);
  }

  // Setup the segment display
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments, false, false, true);
  reset();
}

void loop()
{
  
}