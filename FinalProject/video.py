import cv2
import serial
from collections import deque
import statistics
import cv2
import multiprocessing as mp


NUM_SENSORS = 3
readings_queue = [deque([]) for _ in range(NUM_SENSORS)]
files = ["media/radial1.mp4"]
setpoint = 450
frametime = 25


def play_clips(files, mult):
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

        if cv2.waitKey(frametime // mult) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()


def read_serial(q, mult):
    while True:
        arduino = serial.Serial(port="/dev/cu.usbmodem11201")
        data = arduino.readline().decode().rstrip().split(",")
        if len(data) < NUM_SENSORS:
            continue
        data = [int(r) for r in data]
        change_to_running_avg = [0 for _ in range(NUM_SENSORS)]
        for i in range(NUM_SENSORS):
            srq = q[i]
            if len(srq) > 1:
                change_to_running_avg[i] = statistics.mean(srq) - data[i]
            if len(srq) > 25:
                srq.popleft()
            srq.append(data[i])

        total_avg_change = statistics.mean(change_to_running_avg)
        if -50 < abs(total_avg_change) < 50:
            continue
        
        if total_avg_change < 0:
            mult.value -= .01
            # mult.value *= 100 // avg_change
            # print(mult.value + int(total_avg_change))
        else:
            mult.value + .01
            # print(mult.value * int(total_avg_change))
        print(mult.value)
        

if __name__ == "__main__":
    # read_serial(readings_queue, 1)
    # play_clips(files, 2)
    mult = mp.Value('d', 1.0)
    p1 = mp.Process(target = read_serial, args=[readings_queue, mult])
    # p2 = mp.Process(target = play_clips, args=[files, mult])
    p1.start() 
    # p2.start()

    p1.join()
    # p2.join()
    pass
