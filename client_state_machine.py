# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
import pygame
import random
import ast
import random
import math
import numpy as np
from chat_utils import *


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT + 'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def pinpoint(self, msg):
        new_list = list(msg)
        dimension = math.ceil(math.sqrt(len(msg))) ** 2
        sqrd_dimension = int(math.sqrt(dimension))

        #converting the message to optimal square matrix
        new_list.extend(['0' for i in range(dimension - len(msg))])

        #print(new_list)

        new_list = [new_list[j:j+sqrd_dimension] for j in range(0, dimension, sqrd_dimension)]

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


    def decode_pinpoint(self, matrix):
        msg = matrix[:-2]
        checksum = matrix[-2:]
        sqrd_dimension = len(matrix[0])
        print(msg)

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

        points, differences = self.get_point(difference_matrix)

        try:
            for i in range(len(points)):
                msg[points[i][0]][points[i][1]] = chr(ord(msg[points[i][0]][points[i][1]]) + differences[i])
        except:
            pass


        msg = [''.join(msg[i])for i in range(len(msg))]
        msg = ''.join(msg)
        try:
            index_of_0 = msg.index('0')
            msg = msg[:index_of_0]
        except:
            pass


        return msg

    def get_point(self, matrix):
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


    def proc(self, my_msg, peer_code, peer_msg, world):
        self.out_msg = ''
        #==============================================================================
        # Once logged in, do a few things: get peer listing, connect, search
        # And, of course, if you are so bored, just go
        # This is event handling instate "S_LOGGEDIN"
        #==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    logged_in = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                        world.reset()
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_rslt = myrecv(self.s)[1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, M_POEM + poem_idx)
                    poem = myrecv(self.s)[1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    """
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    """
                    # print(peer_msg)
                    world.reset()
                    posdict = ast.literal_eval(peer_msg)
                    world.interpretPos(self.me, posdict)
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            pygame.event.pump()
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_a]:
                if world.players[self.me].changeDirection('left'):
                    mysend(self.s, M_DIRECTION + self.me + ":left")
            if pressed[pygame.K_d]:
                if world.players[self.me].changeDirection('right'):
                    mysend(self.s, M_DIRECTION + self.me + ":right")
            if pressed[pygame.K_w]:
                if world.players[self.me].changeDirection('up'):
                    mysend(self.s, M_DIRECTION + self.me + ":up")
            if pressed[pygame.K_s]:
                if world.players[self.me].changeDirection('down'):
                    mysend(self.s, M_DIRECTION + self.me + ":down")

            if pressed[pygame.K_RETURN]:
                mysend(self.s, M_START)

            world.tick()

            if world.getWinner() != None:
                self.disconnect()
                self.state = S_LOGGEDIN
                self.peer = ''

            if len(my_msg) > 0:  # my stuff going out
                mysend(self.s, M_EXCHANGE + self.me + ":" + str(self.pinpoint(my_msg)))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:  # peer's stuff, coming in
                if peer_code == M_CONNECT:
                    posdict = ast.literal_eval(peer_msg)
                    world.interpretPos(self.me, posdict)
                    # print(posdict)
                elif peer_code == M_START:
                    world.start()
                elif peer_code == M_DIRECTION:
                    spltmsg = peer_msg.split(":")
                    world.players[spltmsg[0]].changeDirection(spltmsg[1])
                else:
                    spltmsg = peer_msg.split(":")
                    spltmsg[1] = self.decode_pinpoint(ast.literal_eval(spltmsg[1]))
                    self.out_msg = self.out_msg + spltmsg[0] + ":" + spltmsg[1]


            # I got bumped out
            if peer_code == M_DISCONNECT:
                while world.getWinner() == None:
                    world.tick()
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
