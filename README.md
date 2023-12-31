# Informed-Search-Pancake-Sorting

A* search algorithm and a UCS algorithm to solve the Pancake Sorting Problem. That is, order a disordered stack of different sized pancakes by flipping all pancakes above a certain depth.

## Title

CS 131 HW 02 - The Pancake Problem

## Author

Brandon Dionisio

## Problem Description

A messy cook has a disordered stack of 10 differently sized pancakes [size from 1 to 10] and a spatula that can be inserted at any point in the stack and used to flip all pancakes above it. The goal is for the cook to have them in the “correct” order for the customer, that is, the large on the bottom up to the smallest on top ([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]).

## Acknowledgements

stackoverflow

CS 131 Canvas Slides

CS 131 Piazza

docs.python.org

## Running The Program

To run the A* search algorithm, use "python astar.py"

To run the UCS search algorithm, use "python ucs.py"

## User Inputs

When running the program, users will be prompted to enter their pancake stack or type 'r'.  
Pancake stacks must be consecutive integers with the largest of the integers being the last number.

"42135" is a valid input  
"7564348" is a valid input  
"5" is a valid input  
"32154" is an invalid input  
"3 2 1 4" is an invalid input  
"4215" is an invalid input  

Typing 'r' will initialize the pancake stack as a randomly sorted 10-length pancake stack.

## Assumptions

Keeps requesting input until user provides valid input  
Plate is on the right of the stack array

## Forward Cost Function (Heuristic Function)

Number of stack positions for which the pancake at that position is not of adjacent size to the pancake below

## Backward Cost Function

Total number of pancakes flipped to get to current position
