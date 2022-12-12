#include "SevSeg.h"
SevSeg sevseg;

int number = 0;
char buffer[5];

byte digitPins[] = {4, 5, 6, 7};
byte segmentPins[] = {9, 46, 16, 18, 8, 3, 15, 17};

int relayPins[] = {10, 11};
int relayCooldown[] = {0, 0};
int relayUpTime = 1000;

int relayIndex = 1;
int relayLength = 0;

int buttonPin = 13;
int buttonState = 0;
bool isPressed = false;
int pressDelay = 2000;
int currentPressDelay = 0;

void enable_relay() {
    Serial.println("Pressed");
    if (relayCooldown[relayIndex] <= 0) {
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

void setup()
{
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);
  for (size_t i = 0; i < relayLength; i++)
  {
    Serial.printf("initializing: %d", i);
    pinMode(relayPins[i], OUTPUT);
  }

  byte numDigits = sizeof(digitPins) / sizeof(digitPins[0]);;
  relayLength = sizeof(relayPins) / sizeof(relayPins[0]);
  bool resistorsOnSegments = 0;
  //sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments);
  //sevseg.setBrightness(90);
  currentPressDelay = pressDelay;

  //reset();
}

int incomingByte = 0;
void loop()
{
  buttonState = digitalRead(buttonPin);
  if (buttonState == LOW)
  {
    if (!isPressed && currentPressDelay <= 0)
    {
      isPressed = true;
      currentPressDelay = pressDelay;
      //add_number(1);
      enable_relay();
    }
  }
  else
  {
    isPressed = false;
    if (currentPressDelay > 0){
      currentPressDelay--;
    }
  }

  for (size_t i = 0; i < relayLength; i++)
  {
    if (relayCooldown[i] > 0) {
      relayCooldown[i]--;

      if (relayCooldown[i] <= 0) {
        Serial.printf("Relay cooldown over %d: %d\n", i, relayCooldown[i]);
        //digitalWrite(relayPins[relayIndex], LOW);
        relayCooldown[i] = 0;
      }
    }
  }

  //sevseg.refreshDisplay();
}
