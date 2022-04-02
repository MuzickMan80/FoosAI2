
#include <Arduino.h>
#include <HardwareTimer.h>
#include <ports.h>

void init_board()
{
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
}