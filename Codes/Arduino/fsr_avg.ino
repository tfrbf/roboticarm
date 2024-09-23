#include <movingAvg.h>    // Include the moving average library

const uint8_t PHOTOCELL_PIN1 = A0;  // Define pin A0 for the first photocell
const uint8_t PHOTOCELL_PIN2 = A1;  // Define pin A1 for the second photocell

movingAvg photoCell1(10);  // Create a moving average object for the first photocell
movingAvg photoCell2(10);  // Create a moving average object for the second photocell

void setup()
{
    pinMode(PHOTOCELL_PIN1, INPUT_PULLUP);  // Set the default state for the first photocell pin
    pinMode(PHOTOCELL_PIN2, INPUT_PULLUP);  // Set the default state for the second photocell pin
    Serial.begin(115200);
    photoCell1.begin();  // Initialize the moving average object for the first photocell
    photoCell2.begin();  // Initialize the moving average object for the second photocell
}

void loop()
{
    int pc1 = analogRead(PHOTOCELL_PIN1);  // Read the analog value from the first photocell
    int avg1 = photoCell1.reading(pc1);    // Compute the moving average for the first photocell

    int pc2 = analogRead(PHOTOCELL_PIN2);  // Read the analog value from the second photocell
    int avg2 = photoCell2.reading(pc2);    // Compute the moving average for the second photocell

    Serial.print(pc1);  // Send the raw value from the first photocell
    Serial.print(',');
    Serial.print(avg1);  // Send the moving average from the first photocell
    Serial.print(',');
    Serial.print(pc2);  // Send the raw value from the second photocell
    Serial.print(',');
    Serial.println(avg2);  // Send the moving average from the second photocell

    delay(1000);  // Wait for 1 second
}
