# https://www.sciencedirect.com/science/article/pii/S1742287613000510
# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjViPqBjrDxAhUGjhQKHe0SCN0QFjAAegQIAxAD&url=https%3A%2F%2Fwww.iacs.org.uk%2Fdownload%2F1871&usg=AOvVaw2AFrLs9fUAaCMTTwdPvqJq
import errno
import os
import socket
import threading
import time
from pathlib import Path
import configparser
from .tools import *


frame_creation_times = []
nmea_creation_times = []
config = configparser.ConfigParser()
config.read('config.ini')
record_duration = config['record']['duration']


class Vdr:

    config = configparser.ConfigParser()
    config.read('config.ini')

    def __init__(self, path="."):
        self.path = path + "/data"
        self.frame_filename = "000000"
        self.nmea_filename = "000000"
        self.voice_filename = "000000"
        self.connections = {}
        self.start_time = time.time()

        # Create tree structure of VDR if it is not already exists
        if not os.path.exists(path + "/data"):
            os.makedirs(path + "/data")
        if not os.path.exists(path + "/data/frame"):
            os.makedirs(path + "/data/frame")
        if not os.path.exists(path + "/data/nmea"):
            os.makedirs(path + "/data/nmea")
        if not os.path.exists(path + "/data/voice"):
            os.makedirs(path + "/data/voice")

    def add_connection(self, ip, port, key):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        self.connections[key] = sock


class ReceivingFrame(threading.Thread):

    def __init__(self, vdr, key):
        threading.Thread.__init__(self)
        self.vdr = vdr
        self.key = key

    def run(self):
        end_time = self.vdr.start_time + int(config['record']['duration'])
        while True:
            data = self.vdr.connections[self.key].recvfrom(1024)
            path = self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp"
            print(self.vdr.frame_filename)
            while os.path.exists(path):
                self.vdr.frame_filename = update(self.vdr.frame_filename)
                path = self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp.gz"
            if data[0] == b'start':
                f = open(self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp.gz", 'wb')
                data = self.vdr.connections[self.key].recvfrom(8192)
                while data:
                    if data[0] == b'stop':
                        print("picture received")
                        f.close()
                        os.system("gunzip " + self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp.gz")
                        frame_creation_times.append((self.vdr.frame_filename, os.path.getmtime(self.vdr.path + "/frame/" + self.vdr.frame_filename + ".bmp")))
                        print(frame_creation_times)
                        current_time = time.time()

                        if current_time > end_time:
                            for i in frame_creation_times:
                                if i[1] < current_time - int(config['record']['duration']):
                                    os.remove(self.vdr.path + "/frame/" + i[0] + ".bmp")
                                    frame_creation_times.pop(0)
                                else:
                                    break
                        break
                    else:
                        f.write(data[0])
                        data = self.vdr.connections[self.key].recvfrom(8192)


class ReceivingNmea(threading.Thread):
    def __init__(self, vdr, key):
        threading.Thread.__init__(self)
        self.key = key
        self.vdr = vdr

    def run(self):
        end_time = self.vdr.start_time + int(config['record']['duration'])
        while True:
            data = self.vdr.connections[self.key].recvfrom(1024)
            print(self.key, ":", data)
            path = self.vdr.path + "/nmea/" + self.vdr.nmea_filename
            file = open(path, "a")
            file_size = Path(path).stat().st_size
            if file_size > int(self.vdr.config['nmea']['size']):
                file.close()
                nmea_creation_times.append((self.vdr.nmea_filename, os.path.getmtime(self.vdr.path + "/nmea/" + self.vdr.nmea_filename)))
                print(nmea_creation_times)
                current_time = time.time()

                if current_time > end_time:
                    for i in nmea_creation_times:
                        if i[1] < current_time - int(config['record']['duration']):
                            os.remove(self.vdr.path + "/nmea/" + i[0])
                            nmea_creation_times.pop(0)
                        else:
                            break

                self.vdr.nmea_filename = update(self.vdr.nmea_filename)
                file = open(path, "a")

            split_data = bytes.decode(data[0]).split(',')

            try:
                if split_data[1] == "propulsion_management_system":
                    propulsion(split_data, file)
                elif split_data[1] == "safety_management_system":
                    safety(split_data, file)
                elif split_data[1] == "power_management_system":
                    power(split_data, file)
                elif split_data[1] == "utilities_management_system":
                    utilities(split_data, file)
            except IndexError:
                print(errno)
