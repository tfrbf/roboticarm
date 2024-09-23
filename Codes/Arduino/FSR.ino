
#include <Servo.h>

#define sensor0 A0
#define sensor1 A1
#define sensor2 A2
#define sensor3 A3

double sensor0_value, sensor1_value, sensor2_value, sensor3_value;


float glove_average = 0;
float gripper_value = 0;

Servo servo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  servo.attach(3);
  servo.write(170);
}

void loop() {


  sensor0_value = floor(analogRead(sensor0) / 100);
  sensor1_value = floor(analogRead(sensor1) / 100);
  sensor2_value = analogRead(sensor2);
  sensor3_value = analogRead(sensor3);

  glove_average = (sensor0_value + sensor1_value) / 2;

  gripper_value = map(glove_average, 0, 4, 170, 10);
  

  servo.write(gripper_value);

  Serial.print("Sensor1: ");
  Serial.print(floor(sensor0_value));
  Serial.print("\t");
  Serial.print("Sensor2: ");
  Serial.print(floor(sensor1_value));
  Serial.print("\t");
  Serial.print("Glove Average: ");
  Serial.print(glove_average);
  Serial.print("\t");
  Serial.print("Gripper degree: ");
  Serial.print(gripper_value);
  Serial.print("\t");
  Serial.print("servo");
  Serial.print(servo.read());
  Serial.print("\n");

}
