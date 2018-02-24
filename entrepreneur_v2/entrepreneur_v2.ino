/*************************************
* My Lidar Lite を扱うためのプログラム
*************************************/

//#include <SoftwareServo.h>
//#include <TimerOne.h>
#include <MsTimer2.h>
#include <Wire.h>
#include <LIDARLite.h>
#include <Servo.h>
#define pi 3.14159265
#define DIR_PIN 2
#define STEP_PIN 3
#define deg2rad pi/180.0

LIDARLite myLidarLite;
Servo servo;

volatile int stepCount = 0;
volatile int roundCount = 0;

int height = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("setup");

  myLidarLite.begin(0, true);
  myLidarLite.configure(0);

  servo.attach(11);
  servo.write(height);

  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);

  digitalWrite(DIR_PIN, HIGH);

  //Timer1.initialize(2000);//2000
  //Timer1.attachInterrupt(tick);//ステッピングはタイマーで割り込み事によってスムーズに動かす
  MsTimer2::set(2, tick);
  MsTimer2::start();
}

void loop() {
  receive(true);
}

void receive(bool bias)
{

  // float azimuth = (((float)stepCount / 200.0f) * 360.0f);
  float azimuth = 1.8 * stepCount * deg2rad;
  float elevation = (90 - height) * deg2rad;
  float radius = myLidarLite.distance(bias);//極座標系(距離) trueじゃないと距離が取れない
  //極座標を直行座標に変換
  float y = radius * sin(elevation ) * cos(azimuth );
  float x = radius * sin(elevation ) * sin(azimuth );
  float z = radius * cos(elevation );
  Serial.println(String(-x, 5) + " " + String(-y, 5) + " " + String(z, 5)/* + " " + String(height)*/);
  servo.write(height);
}


void tick()//タイマで割り込む
{
  digitalWrite(STEP_PIN, HIGH);
  delay(1);
  digitalWrite(STEP_PIN, LOW);

  stepCount++;
  if (stepCount >= 200)
  {
    stepCount = 0;
    roundCount++;
  }

  if (roundCount >= 2) //二週したら0に戻す
  {
    height = height + 1;//サーボの角度をプラス
    if (height >= 91)  { //サーボが90度までいったら0に戻す
      height = 0;
    }
    roundCount = 0;
  }
}

void noneAction() {
 //何の働きもない関数です。 
}
