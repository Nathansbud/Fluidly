import cv2
import serial
from collections import deque
import statistics
import multiprocessing as mp
import sys
import json
import websockets
import asyncio


# constants
NUM_SENSORS = 3
NOISE_THRESHOLD = 100
QUEUE_SIZE = 25
WAIT_TIME = 100 
FRAME_RATE = lambda x: max(1, int(WAIT_TIME / x))
# PORT = "COM3"

# # globals
# arduino = serial.Serial(port=PORT)

readings_queue = [deque([]) for _ in range(NUM_SENSORS)]
files = ["./media/Dance 2.mov"]

def read_in():
    line = sys.stdin.readline()
    #Since our input would only be having one line, parse our JSON data from that
    print(json.loads, line)
    return json.loads(line)

# plays video clips according to multiplier calculated by sensor reader
def play_clips(files, mult):
    video_index = 0
    cap = cv2.VideoCapture(files[video_index])

    WN = "Breathing Underwater"
    cv2.namedWindow(WN, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WN, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while True:
        ret, frame = cap.read()
        if not ret:
            video_index += 1    
            cap.release()
            cap = cv2.VideoCapture(files[video_index % len(files)])
            continue
        
        cv2.imshow(WN, frame)
        if cv2.waitKey(FRAME_RATE(mult.value)) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

# reads sensor values from arduino and calulates multiplier to pass to streamer
async def read_serial(ws, q, mult):
    while True:
        msg = await ws.recv()
        data = msg.split(",")
        # data = arduino.readline().decode().rstrip().split(",")
        if len(data) < NUM_SENSORS:
            continue
        data = [int(r) for r in data]
        change_to_running_avg = [0 for _ in range(NUM_SENSORS)]
        for i in range(NUM_SENSORS):
            srq = q[i]
            if len(srq) > 1:
                change_to_running_avg[i] = statistics.median(srq) - data[i]
            if len(srq) > QUEUE_SIZE:
                srq.popleft()
            srq.append(data[i])
        
        total_avg_change = statistics.mean(change_to_running_avg)
        if abs(total_avg_change) in range(-100, 100):
            continue
        if total_avg_change < 0:
            mult.value = max(1, mult.value - 5)
        else:
            # larger multipler = faster video = inc diff, total avg change > 0
            mult.value = min(100, mult.value + 1)
        
async def main(rq, mult):
    url = "ws://localhost:8081"
    async with websockets.connect(url) as ws:
        await read_serial(ws, rq, mult)
        await asyncio.Future()

if __name__ == "__main__":
    mult = mp.Value('d', 1)
    video_streamer = mp.Process(target = play_clips, args=[files, mult])
    video_streamer.start()
    asyncio.run(main(readings_queue, mult))

    # mult = mp.Value('d', 1)
    # sensor_reader = mp.Process(target = asyncio.run, args=[wrapper()])

    # sensor_reader.start() 
    # # video_streamer.start()

    # sensor_reader.join()
    # # video_streamer.join()
