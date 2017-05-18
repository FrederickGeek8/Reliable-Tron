import math
import random
import string
import numpy as np


def encode_pinpoint(msg):
    new_list = list(msg)
    dimension = math.ceil(math.sqrt(len(msg)))**2
    sqrd_dimension = int(math.sqrt(dimension))

    # converting the message to optimal square matrix
    new_list.extend([' ' for i in range(dimension - len(msg))])

    # print(new_list)

    new_list = [
        new_list[j:j + sqrd_dimension]
        for j in range(0, dimension, sqrd_dimension)
    ]

    # row checksum
    row_checksum = []
    for j in range(sqrd_dimension):
        new_row = [ord(new_list[j][k]) for k in range(sqrd_dimension)]
        row_checksum.append(sum(new_row))
    new_list.append(row_checksum)

    # column checksum
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

    # Locating the error
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
    return msg.strip()


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


def produce_error(msg, rate=0.05):
    for i in range(len(msg) - 2):
        for j in msg[1]:
            point = random.uniform(0, 1)
            if point < rate:
                # print('change', [i, j])
                new_list = list(string.printable)
                new_list.remove(j)
                j = random.choice(new_list)
    return msg


if __name__ == '__main__':
    msg = pinpoint("{'Fred': (30, 67), 'Jeff': (30, 5)}")
    msg1 = produce_error(msg)
    print(msg)
    print(msg1)
    myPinpoint = decode_pinpoint(
        produce_error(pinpoint("{'Fred': (30, 67), 'Jeff': (30, 5)}")))
    print(myPinpoint)
    print(pinpoint(myPinpoint) == msg)
