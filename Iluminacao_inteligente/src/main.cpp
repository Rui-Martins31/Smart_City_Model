#include <Arduino.h>
#include <NeoPixelConnect.h>

#define NUM_LEDS_PER_ZONE 23
#define NUM_ZONES 6
#define TOTAL_LEDS 138

#define SOUND_SPEED 0.0343 
#define MIN_DETECT_DIST 3  // cm
#define MAX_DETECT_DIST 6  // cm
#define CLEAR_MIN_DIST 10  // cm
#define CLEAR_MAX_DIST 15  // cm


int trigPins[NUM_ZONES] = {10, 11, 12, 13, 14, 25};


#define LED_PIN 0

// 1 strip de 138 LEDs
NeoPixelConnect strip(LED_PIN, TOTAL_LEDS, pio0, 0);

// flags de estado
bool zoneOn[NUM_ZONES] = {false,false,false,false,false,false};

////////////////////////////////////////////////////////////////////////////////

bool isObjectDetected(int minD, int maxD, int pin)
{
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delayMicroseconds(2);
  digitalWrite(pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin, LOW);

  pinMode(pin, INPUT);
  unsigned long pulse = pulseIn(pin, HIGH, 10000);
  if (pulse == 0)
    return false;
  uint16_t dist = pulse * SOUND_SPEED / 2;
  //Serial.print("Sensor ");
  //Serial.print(pin);
  //Serial.print(": ");
  //Serial.print(dist);
  //Serial.println(" cm");
  return (dist > minD && dist <= maxD);
}




int isObjectDetected22(int min, int thresholdDistance) {
  digitalWrite(3, LOW);
  delayMicroseconds(2);
  digitalWrite(3, HIGH);
  delayMicroseconds(10);
  digitalWrite(3, LOW);

  long duration = pulseIn(4, HIGH);

  int distance = duration * 0.034 / 2;

  if (distance > min && distance <= thresholdDistance) {
    return 1;
  } else {
    return 0; 
  }


   Serial.print(distance);
   Serial.println(" cm");
}

////////////////////////////////////////////////////////////////////////////////
// Liga ou desliga o bloco de LEDs [zone*23 .. zone*23+22]
void setZone(int zone, bool on)
{
  int start = zone * NUM_LEDS_PER_ZONE;
  int end = start + NUM_LEDS_PER_ZONE;
  for (int i = start; i < end; i++)
  {
    if (on)
    {
      
      strip.neoPixelSetValue(i, 255, 255, 255);
    }
    else
    {
      
      strip.neoPixelSetValue(i, 0, 0, 0);
    
    }
  }
  strip.neoPixelShow();
  // Serial.print("Zona ");
  // Serial.print(zone);
  // Serial.println(on ? " ligada" : " desligada");
}

////////////////////////////////////////////////////////////////////////////////
/*
void setup()
{
  Serial.begin(115200);
  Serial.print("Serial initializing");
  while(!Serial && millis()<=10000){
    Serial.print(".");
  }
  Serial.print("Serial initialized!\n");
  strip.neoPixelClear();
  strip.neoPixelShow();
}

void loop()
{
  for (int i = 0; i < 5; i++)
  {
    while (!isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[i])){}
    Serial.print("Obj near detected at sensor ");
    Serial.print(i);
    Serial.print("!\n");
    while (!isObjectDetected(CLEAR_MIN_DIST, CLEAR_MAX_DIST, trigPins[i])){}
    Serial.print("Obj far detected at sensor ");
    Serial.print(i);
    Serial.print("!\n");
  }
  
}*/

void setup()
{
  Serial.begin(115200);
  strip.neoPixelClear();
  strip.neoPixelShow();
  pinMode(4,INPUT);
  pinMode(3,OUTPUT);
}

void loop()
{


  if (!zoneOn[0] && isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[0]))
  {
    zoneOn[0] = true;
    setZone(0, true);
  }
  
  if (zoneOn[0] && isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[1]))
  {
    zoneOn[0] = false;
    setZone(0, false);
  }

  // zona 0

  if (!zoneOn[1] &&  isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[1]))
  {
    zoneOn[1] = true;
    setZone(1, true);
  }

  if (zoneOn[1] && isObjectDetected(CLEAR_MIN_DIST, CLEAR_MAX_DIST, trigPins[0]))
  {
    zoneOn[1] = false;
    setZone(1, false);
  }

  if (!zoneOn[2] && isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[2]))
  {
    zoneOn[2] = true;
    setZone(2, true);
  }

  if (zoneOn[2] && isObjectDetected22(CLEAR_MIN_DIST, CLEAR_MAX_DIST) )
  {
    zoneOn[2] = false;
    setZone(2, false);
  }

  if (!zoneOn[5] && isObjectDetected22(MIN_DETECT_DIST, MAX_DETECT_DIST))
  {
    zoneOn[5] = true;
    setZone(5, true);
  }
  
  if (zoneOn[5] && isObjectDetected(CLEAR_MIN_DIST, CLEAR_MAX_DIST, trigPins[2]))
  {
    zoneOn[5] = false;
    setZone(5, false);
  }

  if (!zoneOn[3] && isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[3]))
  {
    zoneOn[3] = true;
    setZone(3, true);
  }
  
  if (zoneOn[3] && isObjectDetected(CLEAR_MIN_DIST, CLEAR_MAX_DIST, trigPins[4]))
  {
    zoneOn[3] = false;
    setZone(3, false);
  }

  if (!zoneOn[4] && isObjectDetected(MIN_DETECT_DIST, MAX_DETECT_DIST, trigPins[4]))
  {
    zoneOn[4] = true;
    setZone(4, true);
  }
  
  if (zoneOn[4] && isObjectDetected(CLEAR_MIN_DIST, CLEAR_MAX_DIST, trigPins[3]))
  {
    zoneOn[4] = false;
    setZone(4, false);
  }

  delay(5);
}
