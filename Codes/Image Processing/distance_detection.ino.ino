#include <Servo.h>

Servo servo;

const int redPin = 3;
int angel = 0;


void setup() {
  Serial.begin(9600);
  servo.attach(10);
}


void loop() {
  while (Serial.available() > 0) {
    int red = Serial.parseInt();
    if (Serial.read() == '\n') {
      red = constrain(red, 0, 255);
      angel = map(red, 0, 255, 10, 170);
      servo.write(angel);
      Serial.print(angel);
    }
  }

  delay(10);
}