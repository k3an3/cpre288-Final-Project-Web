import serial

def serial_init():
  return serial.Serial()#serial.Serial('/dev/rfcomm0', 57600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO)

def serial_multi_byte(string, ser):
  for letter in string:
    ser.write(letter)

def check_sensor_event():
  # Will eventually check for a sensor event from serial
  # i.e. ser.read(20) and check for predetermined thing.
  return False
