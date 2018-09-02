#include <MsTimer2.h>
#define DIR_PIN 2
#define STEP_PIN 3
void setup() {
  // put your setup code here, to run once:
  MsTimer2::set(20, tick);/*[ms]*/
  MsTimer2::start();
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  digitalWrite(DIR_PIN, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:

}
void tick()//タイマで割り込む
{
  digitalWrite(STEP_PIN, HIGH);
  delay(10);
  digitalWrite(STEP_PIN, LOW);
}
