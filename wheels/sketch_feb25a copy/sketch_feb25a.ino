// Front Left
#define FL_EN    4
#define FL_DIR   3
#define FL_STEP  2

// Front Right
#define FR_EN    7
#define FR_DIR   5
#define FR_STEP  6

// Rear Left
#define RL_EN    10
#define RL_DIR   8
#define RL_STEP  9

// Rear Right
#define RR_EN    13
#define RR_DIR   11
#define RR_STEP  12

#define STEP_DELAY_US 1600

char receivedChar;
bool move = false;

void setup() {

  Serial.begin(9600);

  const int enPins[]   = {FL_EN,   FR_EN,   RL_EN,   RR_EN};
  const int dirPins[]  = {FL_DIR,  FR_DIR,  RL_DIR,  RR_DIR};
  const int stepPins[] = {FL_STEP, FR_STEP, RL_STEP, RR_STEP};

  for (int i = 0; i < 4; i++) {
    pinMode(enPins[i],   OUTPUT);
    pinMode(dirPins[i],  OUTPUT);
    pinMode(stepPins[i], OUTPUT);
    digitalWrite(enPins[i], LOW);   // LOW = driver enabled
    Serial.println("EN pulled low");
  }

  // For forward motion, left and right sides run opposite directions
  // because the motors are mounted as mirrors of each other.
  // Swap HIGH/LOW here if your robot moves backward instead.
  digitalWrite(FL_DIR, LOW);
  digitalWrite(FR_DIR, HIGH);   // mirrored
  digitalWrite(RL_DIR, LOW);
  digitalWrite(RR_DIR, HIGH);   // mirrored
  Serial.println("Forward");
}



void stop(){
  const int enPins[]   = {FL_EN,   FR_EN,   RL_EN,   RR_EN};
  const int dirPins[]  = {FL_DIR,  FR_DIR,  RL_DIR,  RR_DIR};
  const int stepPins[] = {FL_STEP, FR_STEP, RL_STEP, RR_STEP};

  for (int i = 0; i < 4; i++) {
    digitalWrite(enPins[i], HIGH);   // LOW = driver enabled
    Serial.println("EN pulled high");
  }
  digitalWrite(FL_DIR, LOW);
  digitalWrite(FR_DIR, LOW);   
  digitalWrite(RL_DIR, LOW);
  digitalWrite(RR_DIR, LOW); 

  digitalWrite(FL_STEP, LOW);
  digitalWrite(FR_STEP, LOW);
  digitalWrite(RL_STEP, LOW);
  digitalWrite(RR_STEP, LOW); 
}

void loop() {
  if (Serial.available() > 0) {
    receivedChar = Serial.read(); // read the incoming character
    if (receivedChar == '1') {
      move = true;
    } else if (receivedChar == '0') {
      move = false;
      stop(); // stop moving
    }
  }

  if (move){
    // Pulse all four step pins together
    digitalWrite(FL_STEP, HIGH);
    digitalWrite(FR_STEP, HIGH);
    digitalWrite(RL_STEP, HIGH);
    digitalWrite(RR_STEP, HIGH);
    //Serial.println("Step high");

    delayMicroseconds(STEP_DELAY_US);

    digitalWrite(FL_STEP, LOW);
    digitalWrite(FR_STEP, LOW);
    digitalWrite(RL_STEP, LOW);
    digitalWrite(RR_STEP, LOW);

    delayMicroseconds(STEP_DELAY_US);
    //Serial.println("Step low");
  }

}



