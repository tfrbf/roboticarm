#include <Wire.h>
#include <Servo.h>

Servo servo;


void setup() {
  // Start the serial communication
  Serial.begin(9600);  
servo.attach(3);
   if (Serial.available() > 0)

  Serial.print("\tBluetooth Connected Seccessfully.\a");// Checks whether data is comming from the serial port
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming string
    String str = Serial.readString();
    if (str.startsWith("S1")) {
      str = str.substring(3, str.length());
      int S1 = str.toInt();
      //s1 = map(s1, 20, 186, 0, 180)
      Serial.print(S1);
      servo.write(S1);

    }

    // Remove any whitespace or newline characters
   // str.trim();

    // Convert the string to an integer
    int num = str.toInt();

    // Print the integer to the serial monitor
    Serial.print("The converted number is: ");
    Serial.println(num);
  }
  delay(100);
}
