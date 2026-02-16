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

void links() {
  servo.write(65);
}

void rechts() {
  digitalWrite(motoren[0], HIGH);
  digitalWrite(motoren[1], LOW);
  digitalWrite(motoren[2], LOW);
  digitalWrite(motoren[3], HIGH);
}


class MyCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string value = pCharacteristic->getValue();

    if (value.length() > 0) {
      String data = String(value.c_str());
      int commaIndex = data.indexOf(',');

      if (commaIndex > 0) {
        int x = data.substring(0, commaIndex).toInt();
        int y = data.substring(commaIndex + 1).toInt();

        if (y > 20) {
          vorne();
        }
        else if (y < -20) {
          hinten();
        }
        else if (x > 20) {
          rechts();
        }
        else if (x < -20) {
          links();
        }
        else {
          stopp();
        }
      } else {
        char c = value[0];
        if(c == 'V') {
          vorne();
        } else if(c == 'H') {
          hinten();
        } else if(c == 'S') {
          stopp();
        }
      }
    }
  }
};

void setup() {
  for(int i = 0; i < 4; i++) {
    pinMode(motoren[i], OUTPUT);
    servo.attach(35);
  }

  Serial.begin(115200);

  BLEDevice::init("kiRoboter");
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
    } 
    else if(c == 'H') {
      hinten();
    }
    else if(c == 'S') {
      stopp();
    }
  }
}
