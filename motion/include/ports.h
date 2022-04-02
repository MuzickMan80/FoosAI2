
#pragma once

#include "board.h"

#define EN_PIN           PB14 // Enable
#define DIR_PIN          PB12 // Direction
#define STEP_PIN         PB13 // Step
#define SW_RX            PB15 // TMC2208/TMC2224 SoftwareSerial receive pin
#define SW_TX            PB15 // TMC2208/TMC2224 SoftwareSerial transmit pin
#define DRIVER_ADDRESS 0b00   // TMC2209 Driver address according to MS1 and MS2
#define LED1              PA8 // port with an attached LED
#define LED2              PC9 // port with an attached LED

// Using direct register manipulation can reach faster stepping times
#define STEP_PORT     PORTB // Match with STEP_PIN
#define STEP_BIT_POS     13 // Match with STEP_PIN


//
// Steppers
//
#define X_ENABLE_PIN                        PB14
#define X_STEP_PIN                          PB13
#define X_DIR_PIN                           PB12

#define Y_ENABLE_PIN                        PB11
#define Y_STEP_PIN                          PB10
#define Y_DIR_PIN                           PB2

#define Z_ENABLE_PIN                        PB1
#define Z_STEP_PIN                          PB0
#define Z_DIR_PIN                           PC5

#define E0_ENABLE_PIN                       PD2
#define E0_STEP_PIN                         PB3
#define E0_DIR_PIN                          PB4

//
// Software serial
//
#define X_SERIAL_TX_PIN                  PB15
#define X_SERIAL_RX_PIN                  PB15

#define Y_SERIAL_TX_PIN                  PC6
#define Y_SERIAL_RX_PIN                  PC6

#define Z_SERIAL_TX_PIN                  PC10
#define Z_SERIAL_RX_PIN                  PC10

#define E0_SERIAL_TX_PIN                 PC11
#define E0_SERIAL_RX_PIN                 PC11

// Reduce baud rate to improve software serial reliability
#define TMC_BAUD_RATE 19200

#define MAX_SPEED      2000 // In timer value
#define MIN_SPEED        10

#define STALL_VALUE      15 // [-64..63]

#define R_SENSE 0.11f // Match to your driver
                      // SilentStepStick series use 0.11
                      // UltiMachine Einsy and Archim2 boards use 0.2
                      // Panucatt BSD2660 uses 0.1
                      // Watterott TMC5160 uses 0.075