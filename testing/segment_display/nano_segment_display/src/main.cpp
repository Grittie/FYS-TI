#include "SevSeg.h"
SevSeg sevseg;

int countdown = 0;
int max_countdown = 5000;

int number = 0;
char buffer[5];

void setup() {
    Serial.begin(9600);

    byte numDigits = 4;  
    byte digitPins[] = {2, 3, 4, 5};
    byte segmentPins[] = {6, 7, 8, 9, 10, 11, 12, 13};
    bool resistorsOnSegments = 0; 
    sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins, resistorsOnSegments);
    sevseg.setBrightness(90);
}

void loop() {
    sprintf(buffer, "%04d", number);
    char numb;
    for (size_t i = 0; i < 4; i++)
    {
      numb = numb + buffer[i];
    }
    countdown++;

    if (countdown >= max_countdown) {
      number++;
      countdown = 0;
    }

    sevseg.setChars(buffer);
    sevseg.refreshDisplay(); // Must run repeatedly
}

