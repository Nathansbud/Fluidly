import cv2
import serial

files = ["media/Dance 1.mov", "media/Dance 2.mov", "media/Dance 3.mov"]
def play_clips():
    video_index = 0
    cap = cv2.VideoCapture(files[video_index])
    while True:
        ret, frame = cap.read()
        if not ret:
            video_index += 1    
            cap.release()
            cap = cv2.VideoCapture(files[video_index % len(files)])
            continue
        
        cv2.imshow('video', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def read_serial():
    arduino = serial.Serial("/dev/tty.usbmodem141201", 9600)
    while True:
        b = arduino.readline()
        print(b.decode())

if __name__ == "__main__":
    # read_serial()
    play_clips()
    pass
