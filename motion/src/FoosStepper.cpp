#include <FoosStepper.h>
#include <TMCStepper.h>


RodController FoosStepper::CreateRodController(int num) {
    if (num == 0)
    {       
        TMC2209Stepper driver1(X_SERIAL_RX_PIN, X_SERIAL_TX_PIN, R_SENSE, DRIVER_ADDRESS);
        TMC2209Stepper driver2(Y_SERIAL_RX_PIN, Y_SERIAL_TX_PIN, R_SENSE, DRIVER_ADDRESS);

    }
}