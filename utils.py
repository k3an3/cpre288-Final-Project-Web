import serial

def serial_init():
  return serial.Serial()#serial.Serial('/dev/rfcomm0', 57600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO)

def serial_multi_byte(string, serial):
  for letter in string:
    serial.write(letter)
