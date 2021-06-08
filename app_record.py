from selenium import webdriver
import cv2
import numpy as np
import pyautogui
import time
import requests
import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import pyloudnorm as pyln


# RECORD VIDEO AND AUDIO
def recordVideoAudio():

    driver = webdriver.Edge(executable_path="C:\\Users\\Asus\\PycharmProjects\\pythonProject\\msedgedriver.exe")
    driver.get("https://www.youtube.com/watch?v=PjfP2tmjtQM")

    SCREEN_SIZE = (1920, 1080)  # screen resolution
    fourcc = cv2.VideoWriter_fourcc(*"XVID")  # define the codec
    out = cv2.VideoWriter("output_app.avi", fourcc, 10.0, SCREEN_SIZE)  # create the video write object
    fps = 120
    prev = 0

    fs = 44100
    seconds = 100
    myrecording = sd.rec(int(seconds * fs), fs, 1)  # sample rate, channels

    for i in range(1000):   # record time 1:40

        time_elapsed = time.time() - prev
        img = pyautogui.screenshot()  # make a screenshot

        if time_elapsed > 1.0 / fps:
            prev = time.time()
            frame = np.array(img)  # convert these pixels to a proper numpy array to work with OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert colors from BGR to RGB
            out.write(frame)  # write the frame

        cv2.waitKey(10)

    print("recorded, saving...")
    write("music_output.wav", fs, myrecording)
    print("saved")

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()


# MEASURE THE LOUDNESS OF A WAV FILE
def measureLoudness():
    data, rate = sf.read("music_output.wav")  # load audio
    meter = pyln.Meter(rate)  # create BS.1770 meter
    loudness = meter.integrated_loudness(data)  # measure loudness of signal data

    # WRITE IN A FILE THE LOUDNESS
    file = open('db.txt', 'w')
    file.write('{}'.format(loudness))
    file.close()


url = "https://www.youtube.com/watch?v=PjfP2tmjtQM"
timeout = 5

try:
    request = requests.get(url, timeout)
    print("Connected to the Internet")
    recordVideoAudio()
    measureLoudness()
except (requests.ConnectionError, requests.Timeout) as exception:
    print("No internet connection.")
