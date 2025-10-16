from machine import Pin
import math, time
from machine import PWM #load the MicroPython pulse-width-modulation module for driving hardware

time.sleep(1) # Wait for USB to become ready

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