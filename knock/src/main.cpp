#include <Arduino.h>

const int knockPin = 8;
const int ledPin = 7;

int knockVal = HIGH;
boolean knockAlarm = false;
unsigned long prevKnockTime;


int knockAlarmTime = 100;


void setup ()
{
  Serial.begin(9600);  
  pinMode (ledPin, OUTPUT) ;
  pinMode (knockPin, INPUT) ;
}
void loop ()
{
  knockVal = digitalRead (knockPin) ;
  
  if (knockVal == LOW)
  {
  
    prevKnockTime = millis();
    
    if (!knockAlarm)
    {
      Serial.println("KNOCK, KNOCK");
      digitalWrite(ledPin,HIGH);
      knockAlarm = true;
      delay(1000);
    }
  }
  else
  {
    if( (millis()-prevKnockTime) > knockAlarmTime &&  knockAlarm)
    {
      digitalWrite(ledPin,LOW);
      Serial.println("No Knocks");
      knockAlarm = false;
    }
  }
}