// Libraries
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MPU6050.h>

// Define pins
#define sensor0 A0
#define sensor1 A1
#define sensor2 A2
#define sensor3 A3


// Global Variables
double sensor0_value = 0, sensor1_value = 0, sensor2_value = 0, sensor3_value = 0, current_temp = 0;
float glove_average = 0, gripper_value = 0, gripper_average = 0, glove_value = 0;
int16_t roll_angle, pitch_angle;
bool glove_wear = false;



// Initializes Servo motors and Gyroscope
Servo servo;
Servo servo1;
Servo servo2;
Adafruit_MPU6050 mpu;


void setup() {

  Serial.begin(9600);
  Wire.begin();
  servo1.attach(3);
  servo2.attach(4);
  servo.attach(7);
  servo.write(170);
  Serial.println("Initializing the MPU");
  Serial.println(mpu.begin() ? "Successfully Connected" : "Connection failed!");
  delay(1000);
  Serial.println("Taking Values from the MPU");
  delay(1000);
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  current_temp = temp.temperature;
}

void loop() {

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  roll_angle = map(a.acceleration.x, -17000, 17000, 0, 180);

  servo1.write(roll_angle);

  // Reading FSR values
  sensor0_value = floor(analogRead(sensor0) / 100);  // Divide sensor value to 100 for getting stable data
  sensor1_value = floor(analogRead(sensor1) / 100);  // Divide sensor value to 100 for getting stable data
  sensor2_value = floor(analogRead(sensor2) / 100);  // Divide sensor value to 100 for getting stable data
  sensor3_value = floor(analogRead(sensor3) / 100);  // Divide sensor value to 100 for getting stable data

  glove_average = (sensor0_value + sensor1_value) / 2;  // Calculate average value of two FSR
  glove_value = map(glove_average, 0, 4, 170, 10);      // Map FSR value to servo motor rotation range(0-180)

  gripper_average = (sensor2_value + sensor3_value) / 2;  // Calculate average value of two FSR
  servo.write(glove_value);


  // Receive data from blue module
  if (Serial.available() > 0) {

    String str = Serial.readString();
    if (str.startsWith("S1")) {
      str = str.substring(3, str.length());
      int S1 = str.toInt();
      S1 = map(S1, 20, 186, 0, 180);
      servo2.write(S1);
    }

    int num = str.toInt();
    Serial.print("The converted number is: ");
  }


  // Glove_wearing detection
  if (temp.temperature - current_temp >= 0.09) glove_wear = true;
  else glove_wear = false;


  // Printting data
  //Serial.print("Sensor1: ");
  //Serial.print(floor(sensor0_value));
  // Serial.print("\t");
  //Serial.print("Sensor2: ");
  // Serial.print(floor(sensor1_value));
  // Serial.print("\t");
  Serial.print("Glove Average: ");
  Serial.print(glove_average);
  Serial.print("\t");
  Serial.print("Gripper Average: ");
  Serial.print(gripper_average);
  Serial.print("\t");
  Serial.print("servo");
  Serial.print(servo.read());
  Serial.print("\t");
  Serial.print("Twist degree:");
  Serial.print(roll_angle);
  Serial.print("\t");
  Serial.print("Temperature:");
  Serial.print(temp.temperature);
  Serial.print("\t");
  Serial.print("Glove Status:");
  Serial.print(glove_wear);
  Serial.print("\n");

  delay(10);
}
