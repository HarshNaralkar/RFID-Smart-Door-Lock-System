#include <Servo.h>
#include <LiquidCrystal_I2C.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define LED_PIN 4  
#define MAX_ATTEMPTS 3

String UID = "63 66 8A 23";
byte lock = 0;
byte wrong_attempts = 0;

Servo servo;
LiquidCrystal_I2C lcd(0x27, 16, 2);
MFRC522 rfid(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  servo.write(20);  
  lcd.init();
  lcd.backlight();
  servo.attach(3);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  SPI.begin();
  rfid.PCD_Init();
}

void loop() {
  lcd.setCursor(4, 0);
  lcd.print("Welcome!");
  lcd.setCursor(1, 1);
  lcd.print("Put your card");

  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scanning...");

  String ID = "";
  
  for (byte i = 0; i < rfid.uid.size; i++) {
    if (i > 0) ID += " ";
    ID += String(rfid.uid.uidByte[i], HEX);
  }
  
  ID.toUpperCase();
  Serial.println(ID);

  if (ID == UID && lock == 0) {
    servo.write(50);  
    digitalWrite(LED_PIN, HIGH);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Door is open");
    Serial.println("PLAY_UNLOCK_VIDEO");
    delay(1000);  
    lcd.clear();
    lock = 1;
    wrong_attempts = 0;
  } else if (ID == UID && lock == 1) {
    servo.write(20);  
    digitalWrite(LED_PIN, LOW);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Door is locked");
    Serial.println("PLAY_LOCK_VIDEO");
    delay(1000);  
    lcd.clear();
    lock = 0;
  } else {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Wrong card!");
    Serial.println("WRONG_CARD");
    wrong_attempts++;
    delay(1000);
    lcd.clear();

    if (wrong_attempts >= MAX_ATTEMPTS) {
      Serial.println("PLAY_FINAL_WARNING_VIDEO");
      wrong_attempts = 0;
    } else {
      Serial.println("PLAY_WRONG_ATTEMPT_VIDEO");
    }
  }
}
