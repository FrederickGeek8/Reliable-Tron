import socket
import time
import sys
import sysconfig
import math
import ast
import numpy as np

M_UNDEF = '0'
M_LOGIN = '1'
M_CONNECT = '2'
M_EXCHANGE = '3'
M_LOGOUT = '4'
M_DISCONNECT = '5'
M_SEARCH = '6'
M_LIST = '7'
M_POEM = '8'
M_TIME = '9'
M_START = 'a'
M_POS = 'b'
M_DIRECTION = 'c'

if sys.platform == "darwin":
    CHAT_IP = ''  #for Mac
    if '--enable-framework' not in sysconfig.get_config_vars()['CONFIG_ARGS']:
        print(
            "Error: Python not installed as framework. Please use proper Python version."
        )
else:
    CHAT_IP = socket.gethostname()  #for PC

CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

menu = "\n++++ Choose one of the following commands\n \
        time: calendar time in the system\n \
        who: to find out who else are there\n \
        c _peer_: to connect to the _peer_ and chat\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        p _#_: to get number <#> sonnet\n \
        q: to leave the chat system\n\n"

S_OFFLINE = 0
S_CONNECTED = 1
S_LOGGEDIN = 2
S_CHATTING = 3

SIZE_SPEC = 5

CHAT_WAIT = 0.2


def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    else:
        print('Error: wrong state')


def mysend(s, msg):
    #append size to message and send it
    msg = str(pinpoint(msg))
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    total_sent = 0
    while total_sent < len(msg):
        sent = s.send(msg[total_sent:])
        if sent == 0:
            print('server disconnected')
            break
        total_sent += sent


def myrecv(s):
    #receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
        if not text:
            print('disconnected')
            return ('')
        size += text
    size = int(size)
    #now receive message
    msg = ''
    while len(msg) < size:
        text = s.recv(size - len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
    #print ('received '+message)
    return decode_pinpoint(ast.literal_eval(msg))


def pinpoint(msg):
    new_list = list(msg)
    dimension = math.ceil(math.sqrt(len(msg)))**2
    sqrd_dimension = int(math.sqrt(dimension))

    #converting the message to optimal square matrix
    new_list.extend(['0' for i in range(dimension - len(msg))])

    #print(new_list)

    new_list = [
        new_list[j:j + sqrd_dimension]
        for j in range(0, dimension, sqrd_dimension)
    ]

    #row checksum
    row_checksum = []
    for j in range(sqrd_dimension):
        new_row = [ord(new_list[j][k]) for k in range(sqrd_dimension)]
        row_checksum.append(sum(new_row))
    new_list.append(row_checksum)

    #column checksum
    column_checksum = []
    for j in range(sqrd_dimension):
        new_column = [ord(new_list[k][j]) for k in range(sqrd_dimension)]
        column_checksum.append(sum(new_column))
    new_list.append(column_checksum)

    return new_list


def decode_pinpoint(matrix):
    msg = matrix[:-2]
    checksum = matrix[-2:]
    sqrd_dimension = len(matrix[0])
    # print(msg)

    #Locating the error
    new_row_checksum = []
    new_column_checksum = []
    for j in range(sqrd_dimension):
        new_row = [ord(matrix[j][k]) for k in range(sqrd_dimension)]
        new_row_checksum.append(sum(new_row))
        new_column = [ord(matrix[k][j]) for k in range(sqrd_dimension)]
        new_column_checksum.append(sum(new_column))
    new_checksum = [new_row_checksum, new_column_checksum]

    checksum = np.matrix(checksum)
    new_checksum = np.matrix(new_checksum)
    difference_matrix = checksum - new_checksum

    points, differences = get_point(difference_matrix)

    try:
        for i in range(len(points)):
            msg[points[i][0]][points[i][1]] = chr(
                ord(msg[points[i][0]][points[i][1]]) + differences[i])
    except:
        pass

    msg = [''.join(msg[i]) for i in range(len(msg))]
    msg = ''.join(msg)
    try:
        index_of_0 = msg.index('0')
        msg = msg[:index_of_0]
    except:
        pass

    return msg


def get_point(matrix):
    differences = []
    point_matrix = np.transpose(np.nonzero(matrix))
    points = []
    for i in point_matrix:
        if i[0] == 0:
            points.append([i[1]])
        elif i[0] == 1:
            for j in range(len(points)):
                points[j].append(i[1])
                differences.append(matrix[1].item(i[1]))
    return points, differences


def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return ('(' + ctime + ') ' + user + ' : ' + text
            )  # message goes directly to screen
