#include <Arduino.h>
#include <Servo.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID "FFE0"
#define CHARACTERISTIC_UUID "FFE1"

const int motoren[] = {18, 19, 20, 21};        
Servo servo;
int servoWinkel = 75;

unsigned long letzteZeit = 0;
int intervall = 100;

BLECharacteristic *pCharacteristic;

void vorne() {
  for(int i = 0; i < 2; i++) {
    digitalWrite(motoren[i], HIGH);
  }
  for(int j = 2; j < 4; j++) {
    digitalWrite(motoren[j], LOW);
  }
}

void hinten() {
  for(int i = 2; i < 4; i++) {
    digitalWrite(motoren[i], HIGH);
  }
  for(int j = 0; j < 2; j++) {
    digitalWrite(motoren[j], LOW);
  }
}

void stopp() {
  for(int i = 0; i < 4; i++) {
    digitalWrite(motoren[i], LOW);
  }
}

void neutral() { //Neutrale Servo-Position --> 75°
    servo.write(75);
    servoWinkel = 75;
}

void links() {
  unsigned long jetztigeZeit = millis();
  if(jetztigeZeit - letzteZeit >= intervall) {
    servo.write(110);
    servoWinkel = 110;
    letzteZeit = jetztigeZeit;
  }
}

void rechts() {
  unsigned long jetztigeZeit = millis();
  if(jetztigeZeit - letzteZeit >= intervall) {
    servo.write(40);
    servoWinkel = 40;
    letzteZeit = jetztigeZeit;
  }
}

class MyCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();

    if (value.length() > 0) {
      String data = String(value.c_str());
      int komma = data.indexOf(',');
      char c = value[0];
      if(c == 'U') {
        vorne();
      } else if(c == 'D') {
        hinten();
      } else if(c == 'L') {
        links();
      } else if(c == 'R') {
        rechts();
      } else if(c == 'S') {
        stopp();
        neutral();
      }
    }
  }
};

void setup() {
  for(int i = 0; i < 4; i++) {
    pinMode(motoren[i], OUTPUT);
  }
  servo.attach(35);
  servo.write(75);

  Serial.begin(115200);

  BLEDevice::init("Korex KI-Roboter");
  BLEServer *pServer = BLEDevice::createServer();

  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = 
  pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_WRITE
  );
  pCharacteristic->setCallbacks(new MyCallbacks());
  pService->start();
  pServer->getAdvertising()->start();
}

void loop(){
  if(Serial.available()) {
    char c = Serial.read();
    if(c == 'V') {
      vorne();
      Serial.println("Vorne");
    } 
    else if(c == 'H') {
      hinten();
      Serial.println("Hinten");
    }
    else if(c == 'S') {
      stopp();
      Serial.println("Stopp");
    }
  }
}
