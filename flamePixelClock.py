import socket
import datetime
import math
import array
import time

#util to get nth digit of number
def get_digit(number, n):
    return number // 10**n % 10

#UDP settings
UDP_IP = "127.0.0.1"
UDP_PORT = 1075

#panel defs
PANEL_WIDTH = 5
PANEL_HEIGHT = 5
PANEL_PROTOCOL = 0

#build a message header that looks like
#0
#5
#5
MESSAGE_HEADER = str(PANEL_PROTOCOL) + "\n" + str(PANEL_WIDTH) + "\n" + str(PANEL_HEIGHT)

MESSAGE_BODY = ""

#an all '0' frame to turn everything off
BLANK_FRAME = ('\n' + '0'*PANEL_WIDTH)*PANEL_HEIGHT 

now = datetime.datetime.now()

#a formatter to convert a single digit into a string of a binary representation
formatString = "{0:0" + str(PANEL_HEIGHT) + "b}"

#top down, append the binary reps of the digits in hour, then a blank row, then the digits in minute
panelData = [list(formatString.format(get_digit(now.hour,1)))]
panelData.append(list(formatString.format(get_digit(now.hour,0))))
panelData.append(['0']*PANEL_HEIGHT)
panelData.append(list(formatString.format(get_digit(now.minute,1))))
panelData.append(list(formatString.format(get_digit(now.minute,0))))

#transpose array (...array of lists, whatever)
panelData = zip(*panelData)

#textify transposed array
for i in panelData:
	MESSAGE_BODY += '\n' + ''.join(map(str, i))

#set up the socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#send the header and body including the textified time
sock.sendto(MESSAGE_HEADER + MESSAGE_BODY, (UDP_IP, UDP_PORT))
#leave it up for a sec
time.sleep(1)
#wipe it
sock.sendto(MESSAGE_HEADER + BLANK_FRAME, (UDP_IP, UDP_PORT))