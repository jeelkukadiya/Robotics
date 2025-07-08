#include <TFminiS.h>

int distanceLeft;
int distanceRight;
int dLeft;
int dRight;

#define tfLeftSerial Serial2
TFminiS tfLeft(tfLeftSerial);

#define tfRightSerial Serial3
TFminiS tfRight(tfRightSerial);

unsigned long previousMillis = 0;
const long interval = 200;

void setup() 
{
  Serial.begin(9600);
  tfLeftSerial.begin(115200);
  tfRightSerial.begin(115200);
}

void loop() 
{
  unsigned long currentMillis = millis();
  
  distanceLeft=distLeft();
  distanceRight=distRight();

  if (currentMillis - previousMillis >= interval) 
  {
    previousMillis = currentMillis;
    Serial.print("Left : ");
    Serial.println(distanceLeft);
    Serial.print("Right : ");
    Serial.println(distanceRight);
  }
}

int distLeft()
{
  tfLeftSerial.flush();
  tfLeft.readSensor();
  dLeft = tfLeft.getDistance();
  return dLeft;
}

int distRight()
{
  tfRightSerial.flush();
  tfRight.readSensor();
  dRight = tfRight.getDistance();
  return dRight;
}