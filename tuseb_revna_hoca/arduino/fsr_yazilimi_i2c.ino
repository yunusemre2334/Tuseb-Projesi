#include <Wire.h>

int fsrPin = A0; 
int fsrReading;
//her slave in adresi 1 den 32 ye ayrı ayrı belirlenmeli
#define I2C_SLAVE_ADDR 20

int MASK[]   = {0x00FF, 0xFF00};
int SHIFT[]  = {0,    8};
byte buffer[2];

void setup() {
  Serial.begin(9600);
  Wire.begin(I2C_SLAVE_ADDR);
  Wire.setClock(100000);
  Wire.onRequest(requestEvent);
}



void loop() {
  // Analog sensörden okuma yap
  fsrReading = analogRead(fsrPin);
  buffer[0] = getByteAt(fsrReading,1); //High byte
  buffer[1] = getByteAt(fsrReading,0); //Low byte
  buffer[2] = getByteAt(I2C_SLAVE_ADDR,2); //işte slave in adresi burada
  
 
  Serial.println(fsrReading);

  delay(500);
}


byte getByteAt(int value, int position)
{
  int result = value & MASK[position];  
  result = result >> SHIFT[position];    
  byte resultAsByte = (byte) result;     
  return resultAsByte;  
}


void requestEvent() {
  for(int i=0;i<=2;i++){
    Wire.write(buffer[i]);
  }
}


