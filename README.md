# Sodoku player and Solver

This project demonstrates a simple recursive backtracking algorithm that visually demonstrates a brute force approach to finding the solution to a sodoku through an exhaustive, undirected search of the search space.

You can additionally play the game yourself.

Press a number to enter it after selecting a cell with your mouse.
Backspace will erase the entry.
Crt + [number key] will pencil in the entry.
Crt + backspace will erase all the pencil entries.

To view the backtracking algorithm, press space and wait. To skip the visualisation press space again.

Note, the loading time for the algorithm is slow as it prerenders the moves before displaying them sequencially to the canvas.

Optimisations to this project include implementing a yield generator to solve the sodoku as it is being displayed.
