#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(9600);
  servo1.attach(9);  // Attach servo to pin 9
  servo2.attach(10); // Attach servo to pin 10
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int pos1 = data.substring(0, data.indexOf(',')).toInt();
    int pos2 = data.substring(data.indexOf(',') + 1).toInt();
    
    // Map position values (0-180) to servo angles (0-180)
    int angle1 = map(pos1, 0, 180, 0, 180);
    int angle2 = map(pos2, 0, 180, 0, 180);
    
    servo1.write(angle1);
    servo2.write(angle2);
  }
}
