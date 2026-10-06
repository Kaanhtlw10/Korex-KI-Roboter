//Test

#include <Arduino.h>
#include <SPI.h>

#define MOSI 23
#define MISO 19
#define SCLK 18
#define CS 5

#define TX_CC1101 0x3F //Adresse des Sendespeichers aus dem Datenblatt
#define STX_CC1101 0x35 //Sendebefehl aus dem Datenblatt
#define CC1101_ResetAdresse 0x30 //Chip zurücksetzen

const int TasterPin = 15;
const int x_Richtung = 34;
const int y_Richtung = 35;

unsigned long vorherigeZeit = 0;
int delay_ = 200;

void cc1101_resetPin() {
  digitalWrite(CS, HIGH);
  delay(1);

  digitalWrite(CS, LOW);
  digitalWrite(CS, HIGH);
  delay(1);
  digitalWrite(CS, LOW);

  while(digitalRead(MISO)){}
  SPI.transfer(CC1101_ResetAdresse);
  digitalWrite(CS, HIGH);
} 

void setup() {
  Serial.begin(115200);

  SPI.begin(SCLK, MISO, MOSI, CS);
  SPI.beginTransaction(SPISettings(6000000, MSBFIRST, SPI_MODE0));
  
  pinMode(CS, OUTPUT);
  pinMode(MISO, INPUT);
  digitalWrite(CS, HIGH);
  cc1101_resetPin();

  pinMode(TasterPin, INPUT_PULLUP);
}

void loop() {
  unsigned long jetztigeZeit = millis();

  if(jetztigeZeit - vorherigeZeit >= delay_) {
    vorherigeZeit = jetztigeZeit;
    //Joxstick-Teil
    //--------------------------------
    byte mapped_XWert = map(analogRead(x_Richtung), 0, 4095, 0, 255);
    byte mapped_YWert = map(analogRead(y_Richtung), 0, 4095, 0, 255);

    Serial.printf("X-Wert: %d\n", mapped_XWert);
    Serial.printf("Y-Wert: %d\n", mapped_YWert);
    //Taster-Teil
    //-----------------------------------
    byte tasterStatus = digitalRead(TasterPin);
    Serial.println(tasterStatus == LOW ? "Gedrückt" : "Nicht gedrückt");

    digitalWrite(CS, LOW);
    SPI.transfer(TX_CC1101 | 0x40); //Burst Befehl für WRITE
    SPI.transfer(3);
    SPI.transfer(mapped_XWert);
    SPI.transfer(mapped_YWert);
    SPI.transfer(tasterStatus);
    digitalWrite(CS, HIGH);

    digitalWrite(CS, LOW);
    SPI.transfer(STX_CC1101);
    digitalWrite(CS, HIGH);
  }
}