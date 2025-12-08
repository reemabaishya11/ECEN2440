from machine import Pin, I2C
import time

i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)   # use 100 kHz
print("Scan:", i2c.scan())

addr = 0x39
reg_id = 0x92   # APDS9960 ID register
time.sleep(0.05)
try:
    b = i2c.readfrom_mem(addr, reg_id, 1)
    print("ID register read OK, value:", b[0])
except OSError as e:
    print("Read error:", e)