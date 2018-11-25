/// PINS
#define RPI_PIN   0
#define DOOR_PIN  2

void setup() {
  pinMode(DOOR_PIN, OUTPUT);
}

void loop() {
  if (digitalRead(RPI_PIN) > 100) {
    openDoor();
  } else {
    closeDoor();
  }

  delay(1000);
}

void openDoor() {
  digitalWrite(DOOR_PIN, HIGH);
}

void closeDoor() {
  digitalWrite(DOOR_PIN, LOW);
}
