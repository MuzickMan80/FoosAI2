/**
 * Author Teemu Mäntykallio
 *
 * Plot TMC2130 or TMC2660 motor load using the stallGuard value.
 * You can finetune the reading by changing the STALL_VALUE.
 * This will let you control at which load the value will read 0
 * and the stall flag will be triggered. This will also set pin DIAG1 high.
 * A higher STALL_VALUE will make the reading less sensitive and
 * a lower STALL_VALUE will make it more sensitive.
 *
 * You can control the rotation speed with
 * 0 Stop
 * 1 Resume
 * + Speed up
 * - Slow down
 */
#include <Arduino.h>
#include <HardwareTimer.h>
#include <TMCStepper.h>

#define MAX_SPEED      2000 // In timer value
#define MIN_SPEED        10

#define STALL_VALUE      15 // [-64..63]

#define EN_PIN           PB14 // Enable
#define DIR_PIN          PB12 // Direction
#define STEP_PIN         PB13 // Step
#define SW_RX            PB15 // TMC2208/TMC2224 SoftwareSerial receive pin
#define SW_TX            PB15 // TMC2208/TMC2224 SoftwareSerial transmit pin
#define DRIVER_ADDRESS 0b00 // TMC2209 Driver address according to MS1 and MS2
#define LED1              PA8 // port with an attached LED
#define LED2              PC9 // port with an attached LED

#define R_SENSE 0.11f // Match to your driver
                      // SilentStepStick series use 0.11
                      // UltiMachine Einsy and Archim2 boards use 0.2
                      // Panucatt BSD2660 uses 0.1
                      // Watterott TMC5160 uses 0.075

// Select your stepper driver type
TMC2209Stepper driver(SW_RX, SW_TX, R_SENSE, DRIVER_ADDRESS);

// Using direct register manipulation can reach faster stepping times
#define STEP_PORT     PORTB // Match with STEP_PIN
#define STEP_BIT_POS     13 // Match with STEP_PIN

HardwareTimer timer(1);

#define MICROSTEPS 4
uint32 speedRpm_ = 10;
bool running = false;

USBSerial SerialUSB;

void rampUp(uint32_t speed);

void timerExpire() {
  digitalWrite(STEP_PIN, !digitalRead(STEP_PIN));
}

void setup() {
  afio_cfg_debug_ports(AFIO_DEBUG_SW_ONLY);

  #define USB_CONNECT_PIN                   PC13
  pinMode(USB_CONNECT_PIN, OUTPUT);
  digitalWrite(USB_CONNECT_PIN, true);  // USB clear connection
  delay(1000);                          // Give OS time to notice
  digitalWrite(USB_CONNECT_PIN, false);

  SerialUSB.begin(115200);
  uint32_t serial_connect_timeout = millis() + 1000UL;
  while (!SerialUSB && millis()<serial_connect_timeout) { /*nada*/ }
  SerialUSB.println("\nStart...");

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  for (int i = 0; i < 1; ++i) {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    delay(500);
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    delay(500);
  }

  pinMode(EN_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(EN_PIN, LOW);

  driver.begin();
  driver.toff(3);
  driver.blank_time(24);
  driver.rms_current(600); // mA
  driver.microsteps(MICROSTEPS);
  driver.semin(0);
  driver.semax(2);
  driver.sedn(0b01);

  //timer.setPrescaleFactor(8);
  //timer.setOverflow(256);
  timer.pause();
  timer.attachInterrupt(0, timerExpire);

  //rampUp(100);
}

uint32_t speedToStepPeriod(uint32_t speedRpm) {
  int stepsPerRev = 200;
  int stepsPerMin = stepsPerRev * speedRpm;
  int microStepsPerSec = (MICROSTEPS * stepsPerMin)/60;
  int period = 1000000/microStepsPerSec;
  return period;
}

void ramp(int speed) {
  if (speed > MAX_SPEED)
    speed = MAX_SPEED;
  if (speed < MIN_SPEED)
    speed = MIN_SPEED;

  int step = speed < speedRpm_ ? -1 : 1;
  uint32_t stepPeriod = speedToStepPeriod(speedRpm_);
  timer.setPeriod(stepPeriod);
  timer.refresh();
  timer.resume();
  while (speedRpm_ != speed) {
    delay(50);
    speedRpm_+=step;
    stepPeriod = speedToStepPeriod(speedRpm_);
    timer.setPeriod(stepPeriod);
  }
}

void loop() {
  static uint32_t last_time=0;
  uint32_t ms = millis();

  while(SerialUSB.available() > 0) {
    int8_t read_byte = Serial.read();
    #ifdef USING_TMC2660
      if (read_byte == '0')      { TIMSK1 &= ~(1 << OCIE1A); driver.toff(0); }
      else if (read_byte == '1') { TIMSK1 |=  (1 << OCIE1A); driver.toff(driver.savedToff()); }
    #else
      if (read_byte == '0')      { timer.pause();  digitalWrite( EN_PIN, HIGH ); }
      else if (read_byte == '1') { timer.resume(); digitalWrite( EN_PIN,  LOW ); }
    #endif
    else if (read_byte == '+') { ramp(speedRpm_ + 20); }
    else if (read_byte == '-') { ramp(speedRpm_ - 20); }
  }

  if((ms-last_time) > 200) { //run every 0.1s
    last_time = ms;

    READ_RDSEL10_t data{0};
    data.sr = driver.DRV_STATUS();

    SerialUSB.print(speedRpm_, DEC);
    SerialUSB.print(" ");
    SerialUSB.print(speedToStepPeriod(speedRpm_), DEC);
    SerialUSB.print(" ");
    SerialUSB.print(data.sg_result, DEC);
    SerialUSB.print(" ");
    SerialUSB.println(driver.cs2rms(data.se), DEC);
  }
}