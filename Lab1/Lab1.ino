// Sensor Modes
#define STANDBY 0
#define ACTIVE 1

// Pins
#define CAMERA_PIN 2
#define FLASH_PIN 4      //This is the output pin on the Arduino we are using
#define SOLENOID_1_PIN 12  //This is the output pin on the Arduino we are using
#define SOLENOID_2_PIN 13

// [Program]
int D_BETWEEN_RUN     = 4000;  // Delay between run loops
int N_RUNS            = 4;

// [Solenoid]
int D_BEFORE_DROP     = 200;  // Camera opens
int D_VALVE_OPEN      = 300;  // Valve open time
int D_BETWEEN_DROP    = 80;   // Duration between drops
int N_DROPS           = 2;
int F_DECREMENT       = 50; // Factor to decrement successive drops (F_DECREMENT * Nth Drop); must be < D_VALVE_OPEN

// [Flash]
int D_BEFORE_FLASH    = 90;  // Delay before initial flash
int D_BETWEEN_FLASH   = 150;   // Delay between flashes (if N_FLASHES > 1)
int N_FLASHES         = 3;

// [Other]
int D_FORCE           = 10;   // Delay required by components (e.g. flash)

void setup() {
  pinMode(SOLENOID_1_PIN, OUTPUT);  //Sets the pin as an output
  pinMode(SOLENOID_2_PIN, OUTPUT);
  pinMode(FLASH_PIN, OUTPUT);   //Sets the pin as an output
  pinMode(CAMERA_PIN, OUTPUT);  //Sets the pin as an output

  // Start
  Serial.print("Start capture: ");
}

void loop() {
  for(int runs = 0; runs < N_RUNS; runs++) {
    if(runs > 0) delay(D_BETWEEN_RUN); 
    
    digitalWrite(CAMERA_PIN, HIGH);  //Switch Camera ON   
    // Our camera requires some initial startup time, so this shouldn't be 0
    delay(D_BEFORE_DROP);

    for(int drops = 0; drops < N_DROPS; drops++) {
      // Ignore our delay the first time (D_BEFORE_DROP does that)
      if(drops > 0) delay(D_BETWEEN_DROP);

      digitalWrite(SOLENOID_1_PIN, HIGH);  //Switch Solenoid ON
      digitalWrite(SOLENOID_2_PIN, HIGH);
      
      delay(D_VALVE_OPEN);
      
      digitalWrite(SOLENOID_1_PIN, LOW);  //Switch Solenoid OFF
      digitalWrite(SOLENOID_2_PIN, LOW);  //Switch Solenoid OFF
    }
    
    delay(D_BEFORE_FLASH);
  
    for(int flashes = 0; flashes < N_FLASHES; flashes++) {
      // Ignore our delay the first time (D_BEFORE_FLASH does that)
      if(flashes > 0) delay(D_BETWEEN_FLASH + D_BETWEEN_FLASH * runs);
      
      digitalWrite(FLASH_PIN, HIGH);  //Switch Flash ON
      delay(D_FORCE);                  
      digitalWrite(FLASH_PIN, LOW);   //Switch Flash OFF
    }
    digitalWrite(CAMERA_PIN, LOW);  //Switch Camera OFF
  }

  while(true) {}
}