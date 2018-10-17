/*hogehoge*/
#include <Wire.h>
#include <MsTimer2.h>
#include <LIDARLite.h>
#include <LiquidCrystal.h>
#include "Adafruit_VL53L0X.h"
#define pi 3.14159265
#define DIR_PIN 2
#define STEP_PIN 3
#define DEG2RAD pi/180.0
#define NOS 50 //number of smaple
float x[NOS];
float y[NOS];
bool flag = 0;
LIDARLite myLidarLite;
Adafruit_VL53L0X ToF = Adafruit_VL53L0X();
LiquidCrystal lcd();
//構造体で行列を定義
typedef struct matrix {
  int m;//行数
  int n;//列数
  float **data;//value
} matrix;
//行列を0で初期化する(getMemoryで作成した行列はcallocで0が代入されている)
void initMatrix(matrix *num) {
  int i, j;
  for (i = 0; i < num->m; i++) {
    for (j = 0; j < num->n; j++) {
      num->data[i][j] = 0; // 0で初期化
    }
  }
}
//mXnの行列のメモリを確保する(0で初期化されている)
float **getMemory(int m, int n) {
  int i, j;
  float **data;
  if ((data = (float **)malloc(m * sizeof(float *))) == NULL) {
    return NULL;
  }
  for (i = 0; i < m; i++) {
    if ((data[i] = (float *)calloc(n, sizeof(float))) == NULL) {
      while (i > 0) {
        i--;
        free(data[i]);
      }
      free(data);
      return NULL;
    }
  }
  return data;
}
/*行列の作成(行数，列数，配列のアドレス)*/
int makeMatrix(int m, int n, matrix *mat)
{
  mat->m = m;
  mat->n = n;
  if ( (mat->data = getMemory(m, n)) == NULL ) {
    return EXIT_FAILURE;
  }
  return EXIT_SUCCESS;
}
void freeMatrix(int m, float **data) {
  while (m > 0) {
    m--;
    free(data[m]);
  }
  free(data);
}
void inverse(matrix *mat, matrix *inverse) {
  int i, j, k;
  float buf = 0;
  //単位行列を作る
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      inverse->data[i][j] = (i == j) ? 1.0 : 0.0;
    }
  }
  //掃き出し法
  for (i = 0; i < 3; i++) {
    buf = 1 / mat->data[i][i];
    for (j = 0; j < 3; j++) {
      mat->data[i][j] *= buf;
      inverse->data[i][j] *= buf;
    }
    for (j = 0; j < 3; j++) {
      if (i != j) {
        buf = mat->data[j][i];
        for (k = 0; k < 3; k++) {
          mat->data[j][k] -= mat->data[i][k] * buf;
          inverse->data[j][k] -= inverse->data[i][k] * buf;
        }
      }
    }
  }
}
/*行列の表示*/
void printMatrix(matrix *mat){
    int i,j;
    for(i = 0; i < mat->m; i++){
        for(j = 0; j < mat->n; j++){
            Serial.print(mat->data[i][j]);
            Serial.print(",");
        }
        Serial.println();
    }
    return;
}
//受け取った２つの行列の掛け算を行いmatansに格納する
void matrixmultiply(matrix *matA, matrix *matB, matrix *matans) {
  int i, j;
  for (i = 0; i < 3; i++) {
    for (j = 0; j < 3; j++) {
      matans->data[i][0] += matA->data[i][j] * matB->data[j][0];
    }
  }
}
float sum(float *arr) {
  int i;
  float sum = 0;
  for (i = 0; i < NOS; i++) {
    sum += arr[i];
  }
  return sum;
}
float sum2(float *arr) {
  int i;
  float sum = 0;
  for (i = 0; i < NOS; i++) {
    sum += arr[i] * arr[i];
  }
  return sum;
} 
float sum_xy(float *x, float *y) {
  int i;
  float sum = 0;
  for (i = 0; i < NOS; i++) {
    sum += x[i] * y[i];
  }
  return sum;
}
int LSM(float *x, float *y)
{
  Serial.println("LSM");
  int i, j, k;
  float sumx = sum(x), sumy = sum(y), sumx2 = sum2(x), sumy2 = sum2(y), sumxy = sum_xy(x,y);
  matrix rightmat, leftmat, ansmat,inversemat;
  makeMatrix(3, 3, &rightmat);
  makeMatrix(3, 3, &inversemat);
  makeMatrix(3, 1, &leftmat);
  makeMatrix(3, 1, &ansmat);
  rightmat.data[0][0] = sumx2; rightmat.data[0][1] = sumxy; rightmat.data[0][2] = sumx;
  rightmat.data[1][0] = sumxy; rightmat.data[1][1] = sumy2; rightmat.data[1][2] = sumy;
  rightmat.data[2][0] = sumx;  rightmat.data[2][1] = sumy;  rightmat.data[2][2] = NOS;
  for (i = 0; i < 3; i++) {
    leftmat.data[i][0] = 0;
  }
  for (i = 0; i < 3; i++) {
    ansmat.data[i][0] = 0;
  }
  Serial.println("aa");
  for (i = 0; i < NOS; i++) {
    leftmat.data[0][0] = ((x[i] * x[i] * x[i]) - (x[i] * y[i] * y[i]));
    leftmat.data[1][0] = ((x[i] * x[i] * y[i]) - (y[i] * y[i] * y[i]));
    leftmat.data[2][0] = ((x[i] * x[i]) - (y[i] * y[i]));
  }Serial.println("b");
  for (i = 0; i < 3; i++) {
    leftmat.data[i][0] = leftmat.data[i][0]*-1;
  }
  Serial.println("ccc");
  printMatrix(&rightmat);
  printMatrix(&leftmat);
  Serial.println("dd");
  inverse(&rightmat, &inversemat);
  Serial.println("ee");
  matrixmultiply(&inversemat, &leftmat, &ansmat);
  Serial.println("ff");
  printMatrix(&ansmat);
  return EXIT_SUCCESS;
}
void setup() {
  Serial.begin(115200);
  Serial.println("setup");
  /*ToF set up*/
  if (!ToF.begin()) {
    Serial.println("Failed to boot VL53L0X");
  } else {
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
  MsTimer2::set(100, tick);/*[ms]*/
  MsTimer2::start();
}
void loop() {
  if(flag==1){
    if((LSM(x,y))==EXIT_SUCCESS){
      Serial.println("ok");
    }
    flag==0;
  }
}
int receive()
{
  VL53L0X_RangingMeasurementData_t measure;
  ToF.rangingTest(&measure, false); // pass in 'true' to get debug data printout
  int rad_from_lidar = myLidarLite.distance(1);/*[mm]*/
  int rad_from_ToF   = measure.RangeMilliMeter;/*[mm]*/
  /*暫定的にlidarが1000mm以下の場合ToFの値をリターン*/
  if (rad_from_lidar > 1000) {
    return rad_from_lidar;
  } else {
    return rad_from_ToF;
  }
}
void tick()//タイマで割り込む
{
  static int stepCount = 0;
  interrupts();
  int radius = receive();
  noInterrupts();
  x[stepCount] = radius*cos(stepCount*DEG2RAD);
  y[stepCount] = radius*sin(stepCount*DEG2RAD);
  Serial.print(stepCount);
  Serial.print(",");
  Serial.print(x[stepCount]);
  Serial.print(",");
  Serial.println(y[stepCount]);
  digitalWrite(STEP_PIN, HIGH);
  delay(10);
  digitalWrite(STEP_PIN, LOW);
  delay(10);
  digitalWrite(STEP_PIN, HIGH);
  delay(10);
  digitalWrite(STEP_PIN, LOW);
  delay(10);
  digitalWrite(STEP_PIN, HIGH);
  delay(10);
  digitalWrite(STEP_PIN, LOW);
  delay(10);
  digitalWrite(STEP_PIN, HIGH);
  delay(10);
  digitalWrite(STEP_PIN, LOW);
  stepCount++;
  if (stepCount > NOS-1)
  {  
      flag=1;
      MsTimer2::stop();
  }
}


