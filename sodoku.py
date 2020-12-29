from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import multiprocessing

import numpy as np
import random

#initialise blank sodoku array
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

def fill_in(sodoku, string_rep):
    counter = 0
    for row in range(9):
        for col in range(9):
            if (string_rep[counter]!='.'):
                sodoku[row][col] = int(string_rep[counter])
            counter += 1
    return sodoku


def print_sodoku(sodoku):
    for row in range(9):
        for col in range(9):
            print(sodoku[row][col], end = " ")
        print()

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

def nextBlank(sodoku):
    for i in range(9):
        for j in range(9):
            if sodoku[i][j] == 0:
                return (i, j)
    return None

def addEntry(sodoku, row, col, value):
    if isValid(sodoku, row, col, value):
        sodoku[row][col] = value
        return True
    else:
        return False


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

def runRecursiveHistory(sodoku, ans):
    dummy = np.copy(sodoku) 
    recursiveHistory(dummy, ans) 
    return dummy

def recursiveHistory(sodoku, list): 

    pos = nextBlank(sodoku)
    if pos == None:
        return True
    
    for i in range(1,10):
        list.append("t" + str(i)  + str(pos[0])  + str(pos[1]) + "\n")
        if isValid(sodoku, pos[0], pos[1], i):  
            sodoku[pos[0]][pos[1]] = i  
            list.append("m" + str(i) + str(pos[0]) +  str(pos[1]) + "\n")                
            if recursiveHistory(sodoku, list):
                return True
        sodoku[pos[0]][pos[1]] = 0
        list.append("f0" + str(pos[0]) + str(pos[1]) + "\n")  
    return False  
            
def main():
    sodoku = init_arr()
    print_sodoku(sodoku)
    print("\n --- soln ---")
    
    recursive(sodoku)
    print_sodoku(sodoku)
    
    #print(str(nextBlank([8,8])))
    
    exit()
    

if __name__=="__main__":
    main()
    # p = multiprocessing.Process(target=main, name="Sodoku Solver", args=())
    # p.start()
    # # Terminate foo
    # if p.is_alive():
    #     print("\n Process terminated  after 1 second. No solutions exist ... probably\n")
    #     p.terminate()
    #     p.join()
