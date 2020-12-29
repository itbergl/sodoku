from os import environ
import time
import multiprocessing
import numpy as np
import random

# initialise blank sodoku array
def init_arr():
    sodoku = []
    Sample_file = None

    for r in range(9):
        row = []
        for c in range(9):
            row.append(0)
        sodoku.append(row)

    Sample_file = open("dep/Samples.txt","r")
    list = Sample_file.readlines()
    
    Sample_file.close()
    return fill_in(sodoku, random.choice(list))

# turn string representation into a board
def fill_in(sodoku, string_rep):
    counter = 0
    for row in range(9):
        for col in range(9):
            if (string_rep[counter]!='.'):
                sodoku[row][col] = int(string_rep[counter])
            counter += 1
    return sodoku

# check if entry is valid
def isValid(sodoku, row, col, value):

    if sodoku[row][col] != 0:
        return False

    if value < 1 or value > 9:
        return False

    for i in range(9):
        if sodoku[row][i]==value:
            return False
    
    for i in range(9):
        if sodoku[i][col]==value:
            return False
    
    row_offset = row - row%3
    col_offset = col - col%3

    for i in range(3):
        for j in range(3):
            if sodoku[row_offset+i][col_offset+j]==value:
                return False


    return True

# finds the next blank along, left to right then up to down
def nextBlank(sodoku):
    for i in range(9):
        for j in range(9):
            if sodoku[i][j] == 0:
                return (i, j)
    return None

# adds entry to a sodoku - returns boolean of success
def addEntry(sodoku, row, col, value):
    if isValid(sodoku, row, col, value):
        sodoku[row][col] = value
        return True
    else:
        return False

#make dummy copy and save into answer list
def runRecursiveHistory(sodoku, ans):
    dummy = np.copy(sodoku) 
    recursiveHistory(dummy, ans) 
    return dummy

#recursively solve - record history
def recursiveHistory(sodoku, list): 

    pos = nextBlank(sodoku)
    if pos == None:
        return True
    
    for i in range(1,10):
        list.append(str(i)  + str(pos[0])  + str(pos[1]) + "\n")
        if isValid(sodoku, pos[0], pos[1], i):  
            sodoku[pos[0]][pos[1]] = i  
            list.append(str(i) + str(pos[0]) +  str(pos[1]) + "\n")                
            if recursiveHistory(sodoku, list):
                return True
        sodoku[pos[0]][pos[1]] = 0
        list.append("0" + str(pos[0]) + str(pos[1]) + "\n")  
    return False  

# recursively solve - no recording
def recursive(sodoku):
    pos = nextBlank(sodoku)
    if pos == None:
        return True

    for i in range(1,10):
        if isValid(sodoku, pos[0], pos[1], i):  
            sodoku[pos[0]][pos[1]] = i                  
            if recursive(sodoku):
                return True
        sodoku[pos[0]][pos[1]] = 0
    return False

# print sodoku to terminal
def print_sodoku(sodoku):
    for row in range(9):
        for col in range(9):
            print(sodoku[row][col], end = " ")
        print()