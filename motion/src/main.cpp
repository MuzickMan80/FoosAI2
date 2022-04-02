
#include <Arduino.h>
#include <HardwareTimer.h>
#include <TMCStepper.h>

#include <board.h>
#include <ports.h>
#include <stepper.h>

RodController rod0 = RodController(0);
RodController rod1 = RodController(1);


// Select your stepper driver type
TMC2209Stepper driver(SW_RX, SW_TX, R_SENSE, DRIVER_ADDRESS);

HardwareTimer timer(1);

#define MICROSTEPS 4
uint32 speedRpm_ = 10;
bool running = false;

void rampUp(uint32_t speed);

void timerExpire() {
  digitalWrite(STEP_PIN, !digitalRead(STEP_PIN));
}

void setup() {
  init_board();

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