import socket

import vdr
import screenagent

VDR = vdr.Vdr()
VDR.add_connection("localhost", 12345, "ECDIS")
VDR.add_connection("localhost", 12346, "nmea")

ecdis = vdr.ReceivingFrame(VDR, "ECDIS")
nmea = vdr.ReceivingNmea(VDR, "nmea")

ecdis.start()
nmea.start()

"""agent = screenagent.ScreenAgent("localhost", 12345)
agent.send_screenshot()"""

UDP_IP = "localhost"
UDP_PORT = 12346

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

file = open("nmea.txt", "r")
for i in file:
    sock.sendto(i.encode(), (UDP_IP, UDP_PORT))