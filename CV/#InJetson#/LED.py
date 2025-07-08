import serial
import time
import Jetson.GPIO as GPIO

# Define the GPIO pin for the LED
LED_PIN = 18

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)



def setup_serial(port='/dev/ttyACM0', baudrate=9600, timeout=1):
    """ Initialize serial connection """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.is_open:
            print(f"Serial port {port} opened successfully.")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
        return ser
    except Exception as e:
        print(f"Failed to connect to {port}: {str(e)}")
        return None

def close_serial(ser):
    """ Close serial connection """
    if ser is not None and ser.is_open:
        ser.close()
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED
        print("Serial port closed and LED turned off.")

# Example usage
ser = setup_serial()

# Simulate some work
time.sleep(10)

# Close the serial connection and turn off the LED
close_serial(ser)

# Cleanup GPIO
GPIO.cleanup()