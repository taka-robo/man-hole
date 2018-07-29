#include <Wire.h>
#include <MsTimer2.h>
#include <LIDARLite.h>
#include <LiquidCrystal.h>
#include "Adafruit_VL53L0X.h"
#define pi 3.14159265
#define DIR_PIN 2
#define STEP_PIN 3
#define deg2rad pi/180.0

LIDARLite myLidarLite;
Adafruit_VL53L0X ToF = Adafruit_VL53L0X();
LiquidCrystal lcd()
volatile int stepCount = 0;
volatile int roundCount = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("setup");
  /*ToF set up*/
  if (!ToF.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }else{
      Serial.println("ToF ready");
  }

  /*Lidar set up*/
  myLidarLite.begin(0, true);
  myLidarLite.configure(0);
  Serial.println("lidar ready");
  //step motor set up
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  digitalWrite(DIR_PIN, HIGH);
  /*timer attch set up*/
  MsTimer2::set(20, tick);/*[ms]*/
  MsTimer2::start();
}
void loop() {
}
int receive()
{
  VL53L0X_RangingMeasurementData_t measure;
  ToF.rangingTest(&measure, false); // pass in 'true' to get debug data printout
  int rad_from_lidar = myLidarLite.distance(1);/*[mm]*/
  int rad_from_ToF   = measure.RangeMilliMeter;/*[mm]*/
  /*暫定的にlidarが1000mm以下の場合ToFの値をリターン*/
  if(rad_from_lidar>1000){
    return rad_from_lidar;
  }else{
    return rad_from_ToF;
  }
}
int stepUp(){
  digitalWrite(STEP_PIN, HIGH);
  delay(1);
  digitalWrite(STEP_PIN, LOW);
  stepCount++;
  if (stepCount >= 200)
  {
    stepCount = 0;
    roundCount++;
  }
  return stepCount;
}

void tick()//タイマで割り込む
{
  interrupts();
  int radius = receive();
  noInterrupts();
  digitalWrite(STEP_PIN, HIGH);
  delay(1);
  digitalWrite(STEP_PIN, LOW);
  stepCount++;
  if (stepCount >= 200)
  {
    stepCount = 0;
    roundCount++;
  }
  Serial.print(stepCount);
  Serial.print(",");
  Serial.println(radius);
}
void noneAction() {
 //何の働きもない関数です。 
}


