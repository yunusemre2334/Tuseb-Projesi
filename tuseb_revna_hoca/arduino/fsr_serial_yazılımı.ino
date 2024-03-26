#include <SoftwareSerial.h>
int fsr1Pin = 0;
int fsr2Pin = 1;
int fsrReading1;
int fsrReading2;
int fsr1 = 8;
int fsr2 = 9;

SoftwareSerial mySerial(2, 3);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600); 
}

void loop() {
  fsrReading1 = analogRead(fsr1Pin);
  fsrReading2 = analogRead(fsr2Pin);

  Serial.print(fsrReading1);
  Serial.print(fsr1);
  Serial.println();
  
  Serial.print(fsrReading2);
  Serial.print(fsr2);
  Serial.println();
  
  
  delay(100); 
}
