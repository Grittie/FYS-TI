#include "SevSeg.h"
SevSeg sevseg;

int number = 0;
char buffer[5];

byte digitPins[] = {4, 5, 6, 7};
byte segmentPins[] = {9, 46, 16, 18, 8, 3, 15, 17};

const int buttonPin = 4;
int buttonState = 0;
bool isPressed = false;

void update_counter()
{
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

void remove_number(int amount)
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
  pinMode(buttonPin, INPUT);
  byte numDigits = 4;

  bool resistorsOnSegments = 0;
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);

  reset();
}

int incomingByte = 0;
void loop()
{
  //sevseg.refreshDisplay();
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);

  if (buttonState == HIGH)
  {
    // turn on:
    if (!isPressed)
    {
      //add_number(1);
      isPressed = true;
    }
  }
  else
  {
    // turn off:
    isPressed = false;
  }
  // printf("loop");
  // if (Serial.available() > 0) {
  //   incomingByte = Serial.read();

  //   printf("Serial: %d", incomingByte);
  // }
}
