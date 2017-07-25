import socket
import datetime
import math
import array
import time

def get_digit(number, n):
    return number // 10**n % 10

UDP_IP = "127.0.0.1"
UDP_PORT = 1075

PANEL_WIDTH = 5
PANEL_HEIGHT = 5
PANEL_PROTOCOL = 0

MESSAGE_HEADER = str(PANEL_PROTOCOL) + "\n" + str(PANEL_WIDTH) + "\n" + str(PANEL_HEIGHT)
MESSAGE_BODY = ""

BLANK_FRAME = ('\n' + '0'*PANEL_WIDTH)*PANEL_HEIGHT 

now = datetime.datetime.now()

formatString = "{0:0" + str(PANEL_HEIGHT) + "b}"

panelData = [list(formatString.format(get_digit(now.hour,1)))]
panelData.append(list(formatString.format(get_digit(now.hour,0))))
panelData.append(['0']*PANEL_HEIGHT)
panelData.append(list(formatString.format(get_digit(now.minute,1))))
panelData.append(list(formatString.format(get_digit(now.minute,0))))

panelData = zip(*panelData)

for i in panelData:
	MESSAGE_BODY += '\n' + ''.join(map(str, i))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE_HEADER + MESSAGE_BODY, (UDP_IP, UDP_PORT))

time.sleep(1)
sock.sendto(MESSAGE_HEADER + BLANK_FRAME, (UDP_IP, UDP_PORT))