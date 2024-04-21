#include <Wire.h>
#include "SHT31_SWW.h"
#include "SHT31.h"

#define FSR1 A0
#define FSR2 A1
#define FSR3 A2
#define FSR4 A3

//int fsrPin = A0; 
//int fsrReading;

//her slave in adresi 1 den 32 ye ayrı ayrı belirlenmeli
#define I2C_SLAVE_ADDR 20
#define SHT_address   0x44
#define USESOFTWIRE

#define SHT1_SDA 2
#define SHT1_SCL 3
////////////////////////
#define SHT2_SDA 4
#define SHT2_SCL 5
////////////////////////
#define SHT3_SDA 6
#define SHT3_SCL 7
////////////////////////
#define SHT4_SDA 8
#define SHT4_SCL 9


////////////////////////
SoftwareWire sw1(SHT1_SDA, SHT1_SCL);
SoftwareWire sw2(SHT2_SDA, SHT2_SCL);
SoftwareWire sw3(SHT3_SDA, SHT3_SCL);
SoftwareWire sw4(SHT4_SDA, SHT4_SCL);
////////////////////////


int sensorValue = 0;
uint16_t raw_shtVal=0;
byte buffer[40];

SHT31_SWW sht1;
SHT31_SWW sht2;
SHT31_SWW sht3;
SHT31_SWW sht4;

int MASK[]   = {0x00FF, 0xFF00};
int SHIFT[]  = {0,    8};


void setup() {
  Serial.begin(9600);
  Wire.begin(I2C_SLAVE_ADDR);
  Wire.setClock(100000);
  Wire.onRequest(requestEvent);



  sw1.begin();
  sw2.begin();
  sw3.begin();
  sw4.begin();

  sht1.begin(SHT_address, &sw1);
  sht2.begin(SHT_address, &sw2);
  sht3.begin(SHT_address, &sw3);
  sht4.begin(SHT_address, &sw4);

}



void loop() {

  ///////////////////////////////////////////////////////////////////////////////
  sensorValue = analogRead(FSR1);
  buffer[0] = getByteAt(sensorValue,1);//High byte
  buffer[1] = getByteAt(sensorValue,0);//Low byte
  ////////////////////
  sensorValue = analogRead(FSR2);
  buffer[2] = getByteAt(sensorValue,1);//High byte
  buffer[3] = getByteAt(sensorValue,0);//Low byte
  ////////////////////
  sensorValue = analogRead(FSR3);
  buffer[4] = getByteAt(sensorValue,1);//High byte
  buffer[5] = getByteAt(sensorValue,0);//Low byte
  ////////////////////
  sensorValue = analogRead(FSR4);
  buffer[6] = getByteAt(sensorValue,1);//High byte
  buffer[7] = getByteAt(sensorValue,0);//Low byte
  ///////////////////////////////////////////////////////////////////////////////
  sht1.read(false);         //  default = true/fast       slow = false
  sht2.read(false);
  sht3.read(false);
  sht4.read(false);
  ////////////////////
  if (sht1.isConnected()){
    raw_shtVal = sht1.getRawHumidity();    buffer[8]  = getByteAt(raw_shtVal,1);  buffer[9] = getByteAt(raw_shtVal,0);
    raw_shtVal = sht1.getRawTemperature(); buffer[10] = getByteAt(raw_shtVal,1); buffer[11] = getByteAt(raw_shtVal,0);
    }
  else{
      raw_shtVal = 1000 + ADDR;    buffer[8]  = getByteAt(raw_shtVal,1);  buffer[9] = getByteAt(raw_shtVal,0);
      raw_shtVal = 1000 + ADDR;    buffer[10] = getByteAt(raw_shtVal,1); buffer[11] = getByteAt(raw_shtVal,0);
    }
  ////////////////////
  if (sht2.isConnected()){
    raw_shtVal = sht2.getRawHumidity();    buffer[12]  = getByteAt(raw_shtVal,1);  buffer[13] = getByteAt(raw_shtVal,0);
    raw_shtVal = sht2.getRawTemperature(); buffer[14] = getByteAt(raw_shtVal,1); buffer[15] = getByteAt(raw_shtVal,0);
    }
  else{
      raw_shtVal = 1000 + ADDR;    buffer[12]  = getByteAt(raw_shtVal,1);  buffer[13] = getByteAt(raw_shtVal,0);
      raw_shtVal = 1000 + ADDR;    buffer[14] = getByteAt(raw_shtVal,1); buffer[15] = getByteAt(raw_shtVal,0);
    }
  ////////////////////
  if (sht3.isConnected()){
    raw_shtVal = sht3.getRawHumidity();    buffer[16]  = getByteAt(raw_shtVal,1);  buffer[17] = getByteAt(raw_shtVal,0);
    raw_shtVal = sht3.getRawTemperature(); buffer[18] = getByteAt(raw_shtVal,1); buffer[19] = getByteAt(raw_shtVal,0);
    }
  else{
      raw_shtVal = 1000 + ADDR;    buffer[16]  = getByteAt(raw_shtVal,1);  buffer[17] = getByteAt(raw_shtVal,0);
      raw_shtVal = 1000 + ADDR;    buffer[18] = getByteAt(raw_shtVal,1); buffer[19] = getByteAt(raw_shtVal,0);
    }
  ////////////////////
  if (sht4.isConnected()){
    raw_shtVal = sht4.getRawHumidity();    buffer[20]  = getByteAt(raw_shtVal,1);  buffer[21] = getByteAt(raw_shtVal,0);
    raw_shtVal = sht4.getRawTemperature(); buffer[22] = getByteAt(raw_shtVal,1); buffer[23] = getByteAt(raw_shtVal,0);
    }
  else{
      raw_shtVal = 1000 + ADDR;    buffer[20]  = getByteAt(raw_shtVal,1);  buffer[21] = getByteAt(raw_shtVal,0);
      raw_shtVal = 1000 + ADDR;    buffer[22] = getByteAt(raw_shtVal,1); buffer[23] = getByteAt(raw_shtVal,0);
    }
  ///////////////////////////////////////////////////////////////////////////////
  delay(1);

 


  delay(1);
}


byte getByteAt(int value, int position)
{
  int result = value & MASK[position];  
  result = result >> SHIFT[position];    
  byte resultAsByte = (byte) result;     
  return resultAsByte;  
}

void requesttt(){
  int two_byte = 1022;
  Wire.write(getByteAt(two_byte,1)); //High byte
  Wire.write(getByteAt(two_byte,0)); //Low byte
}

void requestEvent() {
  for(int i=0;i<=23;i++){
    Wire.write(buffer[i]);
  }
}

//uint16_t getRawHumidity()    { return _rawHumidity; };
//uint16_t getRawTemperature() { return _rawTemperature; };

