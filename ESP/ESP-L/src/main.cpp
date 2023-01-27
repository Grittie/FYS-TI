/*
  Program which handles the score and relays of the Whacky Adventures system.
  @author Cor & Don's Whacky adventures
*/
#include <Arduino.h>
#include "SevSeg.h"
SevSeg sevseg;

TaskHandle_t GameTask, RelayTask;
char buffer[5];
int score = 0;

byte digitPins[] = {15, 2, 0, 4};
byte segmentPins[] = {13, 14, 33, 26, 27, 12, 32, 25};

int relayPins[] = {19, 18};
int relayCooldown[] = {0, 0};
int relayUpTime = 1;

int relayIndex = 1;
int relayLength = 0;

// Pins for recieving data from ESP-K
int plusPin = 23;
int resetPin = 22;
int plusState = 0;
int resetState = 0;

void next_relay() {
  relayIndex = relayIndex < relayLength - 1 ? relayIndex + 1 : 0;
} 

/// @brief method which enables the next relay in the index
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

/// @brief method to update the score and the seven Segment Display
void update_score(bool enableRelay = true)
{
  if (enableRelay) {
    enable_relay();
  }

  sprintf(buffer, "%04d", score);
  sevseg.setChars(buffer);
}

/// @brief method to set the value of the 7Segment Display
/// @param num amount to set the score to
void set_score(int num)
{
  score = num;
  update_score();
}

/// @brief method to add the assigned value to the current score amount
/// @param amount amount to add
void add_score(int amount)
{
  score += amount;
  update_score();
}

/// @brief method to subtract the assigned value from the score
/// @param amount amount to subtract
void subtract_score(int amount)
{
  add_score(-amount);
}

/// @brief method to reset the score and 7 Segment Display
void reset()
{
  score = 0;
  update_score(false);
}

/// @brief task which refreshes the 7 Segment Display and keeps track of the incoming data from ESP-K
/// @param pvParameters NULL
void game_task(void *pvParameters)
{
  Serial.print("Task1 running on core ");
  Serial.println(xPortGetCoreID());

  for (;;)
  {
    // Add a point to the score if we receive a correct hit from the ESP-K
    plusState = digitalRead(plusPin);
    if (plusState  == HIGH)
    {
      add_score(1);
    }

    // Reset the system if we receive the signal from the ESP-K
    resetState = digitalRead(resetPin);
    if (resetPin == HIGH)
    {
      Serial.print("reset activated");
      reset();
    }

    // Refresh the seven Segment Display
    sevseg.refreshDisplay();
    delay(1);
  }
}

/// @brief task which updates the states of the relays
/// @param pvParameters NULL
void relay_task(void *pvParameters)
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

/// @brief Setup of the system
void setup()
{
  Serial.begin(115200);
  delay(200);
  Serial.println("Initializing...");

  // Create threads
  xTaskCreatePinnedToCore(game_task, "gameTask", 10000, NULL, 1, &GameTask, 0);
  delay(200);
  xTaskCreatePinnedToCore(relay_task, "relayTask", 10000, NULL, 1, &RelayTask, 1);
  delay(200);

  // Setup the values
  byte numDigits = sizeof(digitPins) / sizeof(digitPins[0]);
  relayLength = sizeof(relayPins) / sizeof(relayPins[0]);
  bool resistorsOnSegments = false;

  // Setup the input pins
  pinMode(plusPin, GPIO_MODE_INPUT);
  pinMode(resetPin, GPIO_MODE_INPUT);
  for (size_t i = 0; i < relayLength; i++)
  {
    Serial.printf("Pin: %d\n", relayPins[i]);
    pinMode(relayPins[i], GPIO_MODE_OUTPUT);
  }

  // Setup the segment display
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments, false, false, true);
  reset();
}

void loop() { }
