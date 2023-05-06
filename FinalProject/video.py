import cv2
import serial
from collections import deque
import statistics
import cv2
import multiprocessing as mp


NUM_SENSORS = 3
readings_queue = [deque([]) for _ in range(NUM_SENSORS)]
files = ["media/radial1.mp4", "media/circular1"]
setpoint = 450
frametime = 100


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
        print(int(frametime / mult.value))
        if cv2.waitKey(max(1, int(frametime / mult.value))) & 0xFF == ord('q'):
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
                change_to_running_avg[i] = statistics.median(srq) - data[i]
            if len(srq) > 25:
                srq.popleft()
            srq.append(data[i])

        total_avg_change = statistics.mean(change_to_running_avg)
        if -100 < abs(total_avg_change) < 100:
            continue

        # larger multipler = faster video = increasing diff = total avg change > 0
        if total_avg_change < 0:
            mult.value = max(1, mult.value - 1)
        else:
            mult.value = min(180, mult.value + 1)
        

if __name__ == "__main__":
    mult = mp.Value('d', 1)
    p1 = mp.Process(target = read_serial, args=[readings_queue, mult])
    p2 = mp.Process(target = play_clips, args=[files, mult])
    p1.start() 
    p2.start()

    p1.join()
    p2.join()
    pass
