// LidarScanner.pde Processing sketch
// http://www.qcontinuum.org/lidar

// Load sketch into Processing, available from:
// https://processing.org/

// This sketch accepts XYZ coordinates from Arduino LIDAR scanner
// and displays them graphically as a 3D point cloud that you can
// pan, zoom, and rotate using keyboard.

import processing.serial.*;

Serial serial;
int serialPortNumber = 0;
float angle = 6.5f;
float angleIncrement = 0;
float xOffset = 3.0;
float xOffsetIncrement = 0;
float yOffset = 152.0f;
float yOffsetIncrement = 0;
float scale = 2.6f;
float scaleIncrement = 0;
//ArrayList<PVector> vectors;
int lastPointIndex = 0;
int lastPointCount = 0;

int MAX_ROW = 1000000;
int MAX_COLUM = 3;
String[] mapForDraw;
float[][] dotData = new float[MAX_ROW][MAX_COLUM];
float distanceFromTheOrigin = 0;
float averageDiameter = 0;
float BIAS_MIN = 0.8;
float BIAS_MAX = 1.2;

void setup() {
  size(800, 600, P3D);
  colorMode(RGB, 255, 255, 255);
  noSmooth();

  mapForDraw = loadStrings("myLabo_5_03_25_21_14.csv");
  //vectors = new ArrayList<PVector>();
  
  // If the File could be opned
  if(mapForDraw != null) {
    for(int i = 0; i < mapForDraw.length; i++) {
      // Check If It Is Not Brank
      if(mapForDraw[i].length() != 0) {
        // Separate by ",".
        String[] values = split(mapForDraw[i], ',');
        // Read As Many Columns
        for(int j = 0; j < 3; j++) {
          if(values[j] != null && values[j].length() != 0) {
            dotData[i][j] = float(values[j]);
          }
        }
      }
    }
  }
  /*String[] serialPorts = Serial.list();
  String serialPort = serialPorts[serialPortNumber];
  println("Using serial port \"" + serialPort + "\"");
  println("To use a different serial port, change serialPortNumber:");
  printArray(serialPorts);
  serial = new Serial(this, serialPort, 115200);*/
}

void calculateTheDiameter() {
  int index,countValid = 0;
  float distance = 0,ave = 0,ave2 = 0;
  for (index = 0; index < mapForDraw.length; index++) {
    ave += mag(dotData[index][0],dotData[index][1],dotData[index][2]);
  }
  ave /= index;//Compute Average of Diameter
  for (index = 0; index < mapForDraw.length; index++) {
    distance = mag(dotData[index][0],dotData[index][1],dotData[index][2]);
    //Carefully Select The Values, And Compute A New Average.
    if(distance > (ave * BIAS_MIN) && distance < (ave * BIAS_MAX)){
      ave2 += distance;
      countValid ++;
    }
  }
  ave2 /= countValid;
  fill(255,255,255);
  textSize(20);
  text("Average Of Old Diameter Is : " + ave ,10,30);
  text("Average Of New Diameter Is : " + ave2,10,60);
}

void draw() {
  /*String input = mapForDraw.readStringUntil(10); //Read Until "10" means "\n" comes.
  if (input != null) {
    String[] components = split(input, ','); // Separate by ",".
    if (components.length == 3) {
      vectors.add(new PVector(float(components[0]), float(components[1]), float(components[2])));
    }
  }*/
  background(0); //Back Ground Color Is Black.
  calculateTheDiameter();
  translate(width/2, height/2, -50);
  rotateY(angle);
  for (int index = 0; index < mapForDraw.length; index++) {
    //PVector v = vectors.get(index);
    /*if (index == size - 1) {
      // draw red line to show recently added LIDAR scan point
      if (index == lastPointIndex) {
        lastPointCount++;
      } else {
        lastPointIndex = index;
        lastPointCount = 0;
      }
      if (lastPointCount < 10) {
        stroke(255, 0, 0);
        line(xOffset, yOffset, 0, v.x * scale + xOffset, -v.z * scale + yOffset, -v.y * scale);
      }
    }*/
    stroke(255, 255, 255);
    distanceFromTheOrigin = mag(dotData[index][0],dotData[index][1],dotData[index][2]);
    if(distanceFromTheOrigin < 10) {
      stroke(color(255,0,0));//R
    }else if(distanceFromTheOrigin > 10 && distanceFromTheOrigin < 15){
      stroke(color(255,255,0));//R + G
    }else if(distanceFromTheOrigin > 15 && distanceFromTheOrigin < 20){
      stroke(color(0,255,0));//G
    }else if(distanceFromTheOrigin > 20 && distanceFromTheOrigin < 25){
      stroke(color(0,0,255));//B
    }else if(distanceFromTheOrigin > 25){
      stroke(color(255,0,255));//R + B
    }
    point(dotData[index][0] * scale + xOffset, -dotData[index][2] * scale + yOffset, -dotData[index][1] * scale);// [Attention!!]X, Z, Y
  }
  angle += angleIncrement;
  xOffset += xOffsetIncrement;
  yOffset += yOffsetIncrement;
  scale += scaleIncrement;
}

void keyPressed() {
  if (key == 'q') {
    // zoom in
    scaleIncrement = 0.02f;
  } else if (key == 'z') {
    // zoom out
    scaleIncrement = -0.02f;
  } else if (key == 'a') {
    // move left
    xOffsetIncrement = -1f;
  } else if (key == 'd') {
    // move right
    xOffsetIncrement = 1f;
  } else if (key == 'w') {
    // move up
    yOffsetIncrement = -1f;
  } else if (key == 's') {
    // move down
    yOffsetIncrement = 1f;
  } else if (key =='x') {
    // erase all points
    //dotMap.clear();
  } else if (key == CODED) {
    if (keyCode == LEFT) {
      // rotate left
      angleIncrement = -0.015f;
    } else if (keyCode == RIGHT) {
      // rotate right
      angleIncrement = 0.015f;
    }
  }
}

void keyReleased() {
  if (key == 'q') {
    scaleIncrement = 0f;
  } else if (key == 'z') {
    scaleIncrement = 0f;
  } else if (key == 'a') {
    xOffsetIncrement = 0f;
  } else if (key == 'd') {
    xOffsetIncrement = 0f;
  } else if (key == 'w') {
    yOffsetIncrement = 0f;
  } else if (key == 's') {
    yOffsetIncrement = 0f;
  } else if (key == CODED) {
    if (keyCode == LEFT) {
      angleIncrement = 0f;
    } else if (keyCode == RIGHT) {
      angleIncrement = 0f;
    }
  }
}
