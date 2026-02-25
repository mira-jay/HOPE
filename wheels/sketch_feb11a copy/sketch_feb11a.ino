/**
 * Author Teemu Mäntykallio
 * Initializes the library and runs the stepper
 * motor in alternating directions.
 */

#include <TMCStepper.h>

#define EN_PIN           2 // Enable - black
#define DIR_PIN          3 // Direction - orange
#define STEP_PIN         4 // Step - black
#define SW_SCK           5 // Clock - red
#define SW_TX            6 // Receive - yellow
#define SW_RX            7 //Transmit - blue
#define DRIVER_ADDRESS 0b00 // TMC2209 Driver address according to MS1 and MS2

#define R_SENSE 0.11f // Match to your driver



TMC2209Stepper driver(SW_RX, SW_TX, R_SENSE, DRIVER_ADDRESS);


void setup() {
  pinMode(EN_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(EN_PIN, LOW);      // Enable driver in hardware

                                  // Enable one according to your setup
//SPI.begin();                    // SPI drivers
//SERIAL_PORT.begin(115200);      // HW UART drivers
  driver.beginSerial(115200);     // SW UART drivers

  driver.begin();                 //  SPI: Init CS pins and possible SW SPI pins
                                  // UART: Init SW UART (if selected) with default 115200 baudrate
  driver.toff(5);                 // Enables driver in software
  driver.rms_current(600);        // Set motor RMS current
  driver.microsteps(16);          // Set microsteps to 1/16th

//driver.en_pwm_mode(true);       // Toggle stealthChop on TMC2130/2160/5130/5160
//driver.en_spreadCycle(false);   // Toggle spreadCycle on TMC2208/2209/2224
  driver.pwm_autoscale(true);     // Needed for stealthChop
}

bool shaft = false;

void loop() {
  // Run 5000 steps and switch direction in software
  for (uint16_t i = 5000; i>0; i--) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1600);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1600);
  }
  shaft = !shaft;
  driver.shaft(shaft);
}