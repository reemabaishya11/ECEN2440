import ir_rx
import machine
from machine import Pin
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
import math, time
from machine import PWM #load the MicroPython pulse-width-modulation module for driving hardware

time.sleep(1) # Wait for USB to become ready

# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")

# Setup the IR receiver
ir_pin = Pin(17, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

# Set up motor control pins and PWM
pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
bin1_ph = Pin(10, Pin.OUT)
bin2_en = PWM(11, freq = pwm_rate, duty_u16 = 0)

pwm = min(max(int(2**16 * abs(1)), 0), 30000)

# Main loop to keep the script running
while True:
    print("Motor A & B - Forward") # Print to REPL
    ain1_ph.high()
    ain2_en.duty_u16(pwm)
    bin1_ph.high()
    bin2_en.duty_u16(pwm)
    time.sleep(3)
    print("Motor A & B - stop") # Print to REPL
    ain1_ph.high()
    ain2_en.duty_u16(0)
    bin1_ph.high()
    bin2_en.duty_u16(0)
    time.sleep(1)
    print("Motor A & B - Backward") # Print to REPL
    ain1_ph.low()
    ain2_en.duty_u16(pwm)
    bin1_ph.low()
    bin2_en.duty_u16(pwm)
    time.sleep(3)
    print("Motor A & B - stop") # Print to REPL
    ain1_ph.high()
    ain2_en.duty_u16(0)
    bin1_ph.high()
    bin2_en.duty_u16(0)
    time.sleep(1)
    #pass # Execution is interrupt-driven, so just keep the script alive