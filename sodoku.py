from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import multiprocessing

import numpy as np
import pygame
import random



#initialise blank sodoku array
sodoku = []

def init_arr():
    for r in range(9):
        row = []
        for c in range(9):
            row.append(0)
        sodoku.append(row)

def fill_in(string_rep):
    counter = 0
    for row in range(9):
        for col in range(9):
            if (string_rep[counter]!='.'):
                sodoku[row][col] = int(string_rep[counter])
            counter += 1


def print_sodoku():
    for row in range(9):
        for col in range(9):
            print(sodoku[row][col], end = " ")
        print()

def isValid(row, col, value):
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

def nextBlank():
    for i in range(9):
        for j in range(9):
            if sodoku[i][j] == 0:
                return (i, j)
    return None

def recursive():
    pos = nextBlank()
    if pos == None:
        return True

    for i in range(1,10):
        if isValid(pos[0], pos[1], i):  
            sodoku[pos[0]][pos[1]] = i                  
            if recursive():
                return True
        sodoku[pos[0]][pos[1]] = 0
    return False   
            
def main():
    Sample_file = open("Samples.txt","r")
    list = Sample_file.readlines()

    sodoku = random.choice(list)

    init_arr()
    fill_in(sodoku)
    print_sodoku()
    print("\n --- soln ---")
    
    recursive()
    print_sodoku()
    
    #print(str(nextBlank([8,8])))
    Sample_file.close()
    exit()
    

if __name__=="__main__":
    p = multiprocessing.Process(target=main, name="Sodoku Solver", args=())
    p.start()
    
    time.sleep(1)
    # Terminate foo
    if p.is_alive():
        print("\n Process terminated after 1 second. No solutions exist ... probably\n")
        p.terminate()
        p.join()
