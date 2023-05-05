/* Adapted from Ping))) Sensor example; https://www.arduino.cc/en/Tutorial/BuiltInExamples/Ping */

// Echo, Trig
const int DISTANCE_PINS[] = { 6, 7, 8, 9, 10, 11, 12, 13 };
const int NUM_SENSORS = 2;

void setup() {
  // initialize serial communication:
  Serial.begin(9600);
  for (int i = 0; i < NUM_SENSORS; i++) {
    pinMode(DISTANCE_PINS[2 * i], INPUT);
    pinMode(DISTANCE_PINS[2 * i + 1], OUTPUT);
  }
}

void loop() {
  for (int i = 0; i < NUM_SENSORS; i++) {
    long duration, cm;
    digitalWrite(DISTANCE_PINS[2 * i + 1], LOW);
    delayMicroseconds(2);
    digitalWrite(DISTANCE_PINS[2 * i + 1], HIGH);
    delayMicroseconds(10);
    digitalWrite(DISTANCE_PINS[2 * i + 1], LOW);
    duration = pulseIn(DISTANCE_PINS[2 * i], HIGH);
    cm = microsecondsToCentimeters(duration);

    Serial.print(i);
    Serial.print(" ");
    Serial.println(cm);
  }
  
  delay(100);
}

long microsecondsToInches(long microseconds) {
  // According to Parallax's datasheet for the PING))), there are 73.746
  // microseconds per inch (i.e. sound travels at 1130 feet per second).
  // This gives the distance travelled by the ping, outbound and return,
  // so we divide by 2 to get the distance of the obstacle.
  // See: https://www.parallax.com/package/ping-ultrasonic-distance-sensor-downloads/
  return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the object we
  // take half of the distance travelled.
  return microseconds / 29 / 2;
}
