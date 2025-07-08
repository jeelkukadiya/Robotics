# communication.py
import serial
import time
import argparse
# import balldetect_new_USB as bd

global_port = '/dev/ttyACM0'
detect_color = 'red'

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", default=global_port,
    help="serial port")
args = vars(ap.parse_args())

# last_done_time = None
#verify = "no"

def setup_serial(port=global_port, baudrate=9600, timeout=1):
    """ Initialize serial connection """
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.is_open:
            print(f"Serial port {port} opened successfully.")
        return ser
    except Exception as e:
        print(f"Failed to connect to {port}: {str(e)}")
        return None
    
def send_coordinates(coordinates,ser,message="no"):
    """ Send coordinates over serial """
    if ser is not None:
        try:
            message = f"{coordinates},{message}\n"
            ser.write(message.encode())
            print(f"Sent coordinates: {coordinates}")
        except Exception as e:
            print(f"Failed to send data: {str(e)}")
    else:
        print("Serial connection not established.")

def read_coordinates():
    # Read coordinates from the shared resource
    with open("coordinates.txt", "r") as f:
        return f.read().strip()

def read_verify():
    #ball detecrt

    # verify = "no"
    # verify = bd.detect_ball()


    # return verify
    with open("ball_detected.txt", "r") as file:
        verify = file.read().strip()
    print("verify sent:",verify)
    verify = "no"
    return verify

def main():
    # ser = serial.Serial('/dev/ttyACM0', 9600,x timeout=1)
    try:
        while True:
            coordinates = read_coordinates()
            if ser is not None:# ser.in_waiting > 0:
                # ser.write(coordinates.encode())
                # send_coordinates(coordinates, ser)
                line = ser.readline().decode('utf-8').strip()
                # line = ""
                current_time = time.time()

                if line == "done":
                    # last_done_time = current_time
                    print("BOOM BOOM")               
                    verify = read_verify()
                    print("verify",verify)
                    send_coordinates(coordinates, ser,verify)
                # elif last_done_time and (current_time - last_done_time < 3):
                #     send_coordinates(coordinates, ser,verify)
                else:
                    send_coordinates(coordinates, ser)

                # with open("done_message.txt", "w") as file:
                #     file.write("")  

            time.sleep(0.1)  # Adjust based on your requirements
    finally:
        if ser is not None:
            ser.close()

ser= setup_serial(args["port"], 9600)

if __name__ == "__main__":
    main()