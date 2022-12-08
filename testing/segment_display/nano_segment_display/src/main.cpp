#include "SevSeg.h"
SevSeg sevseg;

int countdown = 0;
int max_countdown = 5000;

int number = 0;
char buffer[5];

void setup()
{
  Serial.begin(9600);

  byte numDigits = 4;
  byte digitPins[] = {2, 3, 4, 5};
  byte segmentPins[] = {13, 12, 7, 9, 10, 11, 6, 8};
  bool resistorsOnSegments = 0;
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);
}

void update_counter()
{
  sprintf(buffer, "%04d", number);
  sevseg.setChars(buffer);
}

void add_number(int amount)
{
  number += amount;
  update_counter();
}

void remove_number(int amount) {
  add_number(-amount);
}

void reset() {
  number = 0;
  sprintf(buffer, "%04d", number);
  sevseg.setChars(buffer);
}

void loop()
{
  // countdown++;
  // if (countdown >= max_countdown)
  // {
  //   if (number <= 500) {
  //     add_number(1);
  //   } else {
  //     reset();
  //   }
  //   countdown = 0;
  // }

  sevseg.refreshDisplay(); // Must run repeatedly
}
