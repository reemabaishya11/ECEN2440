import ir_rx
from machine import Pin, ADC
from machine import PWM
from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
import math, time, machine
from time import sleep_ms
from apds9960LITE import APDS9960LITE

#Init I2C Buss on RP2040
i2c =  machine.I2C(1,scl=machine.Pin(19), sda=machine.Pin(18))

apds9960=APDS9960LITE(i2c)      # Enable sensor
apds9960.prox.enableSensor()    # Enable Proximit sensing

# while True:
#         sleep_ms(25) # wait for readout to be ready
#         print(apds9960.prox.proximityLevel)   #Print the proximity value

# Select which mode (IR Receiver is 0, RF is 1)
modeSelect = 1 # If RF, comment out interrupt, otherwise uncomment

#rf reciever pins set to inputs
D = Pin(7, Pin.IN)
C = Pin(6, Pin.IN)
B = Pin(5, Pin.IN)
A = Pin(4, Pin.IN)

# Buzzer
buzzer_pin = PWM(Pin(22))

freq_up = 500
freq_down = 200
freq_right = 300
freq_left = 400
freq_attack = 1000

# # Callback function to execute when an IR code is received
# def ir_callback(data, addr, _):
#     print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
#     if (data == 0x03):
#         print("Motor A & B - Backward") # Print to REPL
#         ain1_ph.low()
#         ain2_en.duty_u16(pwmA)
#         bin1_ph.high()
#         bin2_en.duty_u16(pwmB)
#         buzzer_pin.freq(freq_up)
#         buzzer_pin.duty_u16(10000)
#         time.sleep_ms(300)
#     if (data == 0x04):
#         print("Motor A & B - Left") # Print to REPL
#         ain1_ph.low()
#         ain2_en.duty_u16(pwmA)
#         bin1_ph.low()
#         bin2_en.duty_u16(pwmB)
#         buzzer_pin.freq(freq_right)
#         buzzer_pin.duty_u16(10000)
#         time.sleep_ms(150)
#     if (data == 0x01):
#         print("Motor A & B - Forward") # Print to REPL
#         ain1_ph.high()
#         ain2_en.duty_u16(pwmA)
#         bin1_ph.low()
#         bin2_en.duty_u16(pwmB)
#         buzzer_pin.freq(freq_down)
#         buzzer_pin.duty_u16(10000)
#         time.sleep_ms(300)
#     if (data == 0x02):
#         print("Motor A & B - Right") # Print to REPL
#         ain1_ph.high()
#         ain2_en.duty_u16(pwmA)
#         bin1_ph.high()
#         bin2_en.duty_u16(pwmB)
#         buzzer_pin.freq(freq_left)
#         buzzer_pin.duty_u16(10000)
#         time.sleep_ms(150)
#     if (apds9960.prox.proximityLevel >= 5):
#         print("Motor A & B - Max Forward") # Print to REPL
#         ain1_ph.high()
#         ain2_en.duty_u16(maxpwm)
#         bin1_ph.low()
#         bin2_en.duty_u16(maxpwm)
#         buzzer_pin.freq(freq_attack)
#         buzzer_pin.duty_u16(10000)
#         time.sleep_ms(100)
#         buzzer_pin.freq(freq_left)
#     time.sleep_ms(25)
#     ain1_ph.low()
#     ain2_en.duty_u16(0)
#     bin1_ph.low()
#     bin2_en.duty_u16(0)


# # Setup the IR receiver
# ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring
# ir_receiver = NEC_8(ir_pin, callback=ir_callback)

# # Optional: Use the print_error function for debugging
# ir_receiver.error_function(print_error)

# Set up motor control pins and PWM
pwm_rate = 2000
ain1_ph = Pin(12, Pin.OUT) # Initialize GP14 as an OUTPUT
ain2_en = PWM(13, freq = pwm_rate, duty_u16 = 0)
bin1_ph = Pin(14, Pin.OUT)
bin2_en = PWM(15, freq = pwm_rate, duty_u16 = 0)

pwmA = 50000 # max is 65536
pwmB = 52000

maxpwm = 65536

# Voltage divider
adc = ADC(Pin(26))
led = Pin (21, Pin.OUT)
R1 = 75000
R2 = 47000
ratio = (R1 + R2) / R2


# Main loop to keep the script running
while True:
    if (modeSelect):
        if (C.value()):
            print("RF") # Print to REPL
            print("Motor A & B - Left") # Print to REPL
            ain1_ph.low()
            ain2_en.duty_u16(pwmA)
            bin1_ph.low()
            bin2_en.duty_u16(pwmB)
            buzzer_pin.freq(freq_right)
            buzzer_pin.duty_u16(10000)
            time.sleep_ms(150)
        if (B.value()):
            print("RF") # Print to REPL
            print("Motor A & B - Backward") # Print to REPL
            ain1_ph.low()
            ain2_en.duty_u16(pwmA)
            bin1_ph.high()
            bin2_en.duty_u16(pwmB)
            buzzer_pin.freq(freq_up)
            buzzer_pin.duty_u16(10000)
            time.sleep_ms(300)
        if(D.value()):
            print("RF") # Print to REPL
            print("Motor A & B - Right") # Print to REPL
            ain1_ph.high()
            ain2_en.duty_u16(pwmA)
            bin1_ph.high()
            bin2_en.duty_u16(pwmB)
            buzzer_pin.freq(freq_left)
            buzzer_pin.duty_u16(10000)
            time.sleep_ms(150)
        if(A.value()):
            print("RF") # Print to REPL
            print("Motor A & B - Forward") # Print to REPL
            ain1_ph.high()
            ain2_en.duty_u16(pwmA)
            bin1_ph.low()
            bin2_en.duty_u16(pwmB)
            buzzer_pin.freq(freq_down)
            buzzer_pin.duty_u16(10000)
            time.sleep_ms(300)
        if (~A.value() & ~B.value() & ~C.value() & ~D.value()):
            if (apds9960.prox.proximityLevel >= 4):
                print("Motor A & B - Max Forward") # Print to REPL
                ain1_ph.high()
                ain2_en.duty_u16(maxpwm)
                bin1_ph.low()
                bin2_en.duty_u16(maxpwm)
                buzzer_pin.freq(freq_attack)
                buzzer_pin.duty_u16(10000)
                time.sleep_ms(300)
                buzzer_pin.freq(freq_left)
                print(apds9960.prox.proximityLevel)   #Print the proximity value
            else:
                print("RF - Waiting")
                ain1_ph.low()
                ain2_en.duty_u16(0)
                bin1_ph.low()
                bin2_en.duty_u16(0)
                time.sleep_ms(25)
    else:
        time.sleep_ms(10)

    #Voltage Divider code
    sum_val = 0

    for i in range(30):
        reading = adc.read_u16()
        sum_val += reading
        time.sleep_ms(10)

    average = sum_val / 30
    voltage = average * (3.3 / 65535)

    print("Raw:" , average, ", Voltage:", voltage)

    if voltage < 3:
        led.on()
    else:
        led.off()
