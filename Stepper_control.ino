// decode sent data from tx (python script)
// if HIGH is left and LOW is right, ASCII text is decoded into some values that correspond
// to HIGH or LOW, or possibly might just be able to send 0 or 1 assuming HIGH | LOW is boolean
// apparently can just use 1 for HIGH and 0 for LOW 


// TMC2209 driver pins 
const uint8_t PIN_STEP = 6; 
const uint8_t PIN_DIR  = 7; 
const uint8_t PIN_EN   = 8; 

// Nema17 controls 
const unsigned long STEP_DELAY_US = 700;   // delays are in milliseconds 
const int STEPS_PER_MOVE = 50; // 50 steps is 1/4th of a revolution 



//squarewave step signal 
void stepN(int steps) {
  for (int i = 0; i < steps; i++) {
    digitalWrite(PIN_STEP, HIGH);
    delayMicroseconds(STEP_DELAY_US);
    digitalWrite(PIN_STEP, LOW);
    delayMicroseconds(STEP_DELAY_US);
  }
}




void onLeft() {
  Serial.println("Action: LEFT");
  digitalWrite(PIN_DIR, LOW);
  stepN(STEPS_PER_MOVE);
}

void onRight() {
  Serial.println("Action: RIGHT");
  digitalWrite(PIN_DIR, HIGH);
  stepN(STEPS_PER_MOVE);
}



//setup portion & main loop 
void setup() {
  Serial.begin(9600); //Baud rate of 9600 
  Serial.setTimeout(1); 
  delay(300);

  // Stepper pins
  pinMode(PIN_STEP, OUTPUT);
  pinMode(PIN_DIR, OUTPUT);
  pinMode(PIN_EN, OUTPUT);

   // enable driver pins 
  digitalWrite(PIN_STEP, LOW);
  digitalWrite(PIN_DIR, LOW);
  digitalWrite(PIN_EN, LOW); 


}

void loop() {

//listen for char directions from the python script 
  if (Serial.available() > 0) {
  char c = Serial.read();
  if (c == 'L') {
    onLeft();
  } else if (c == 'R') {
    onRight();
  }
}

  }


