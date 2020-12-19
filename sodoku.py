from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import numpy as np
import pygame

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

def nextBlank(pos):
    
    col_temp = pos[1]
    row_temp = pos[0]
    while (row_temp<9):    
        while (col_temp<9):
            if sodoku[row_temp][col_temp] == 0:
                return [row_temp, col_temp]
            col_temp += 1
        col_temp = 0
        row_temp+= 1
    print("oof")
    return [-1,-1]

def recursive(pos):
   
    for i in range(1,10):
        if isValid(pos[0], pos[1], i):  
            sodoku[pos[0]][pos[1]] = i 
            if (pos[0]!=8 or pos[1]!=8):         
                if recursive(nextBlank(pos))==True:
                    return True
            else:
                return True
    sodoku[pos[0]][pos[1]] = 0
    return False   
            

def main():
    test_string = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
    init_arr()
    fill_in(test_string)
    print_sodoku()
    print("\n --- soln ---")
    recursive(nextBlank([0,0]))
    print_sodoku()
    
    #print(str(nextBlank([8,8])))
    

if __name__=="__main__":
    main()


            


