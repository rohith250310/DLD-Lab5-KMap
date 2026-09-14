# DLD Lab 5 - Mini Project Report

## Title
K-Map Based Boolean Expression Minimizer

## Objective
To design a program that reads a 2-, 3-, or 4-variable Karnaugh map from a file and generates all Boolean SOP expressions having minimum cost.

## Problem Statement
The input is a K-map containing 0 and 1 values, with optional X don't-care values. The program must identify valid K-map groups, simplify them into product terms, and find all minimum covers of the 1-cells.

## Concepts Used
- Boolean algebra
- Karnaugh maps
- Gray-code ordering
- Minterms
- SOP representation
- K-map grouping
- Wrap-around adjacency
- Overlapping groups
- Prime implicants
- Essential prime implicants
- Don't-care conditions
- Minimum cover search

## Method
1. Read the K-map from a text file.
2. Validate its dimensions and values.
3. Map K-map positions to minterms using Gray-code ordering.
4. Generate every valid rectangular group of power-of-two size.
5. Handle wrap-around using modulo indexing.
6. Convert each useful group into a Boolean product term.
7. Find combinations that cover every required 1.
8. Minimize first by number of product terms and then by total literals.
9. Print every tied minimum solution.

## Important Design Choice
The assignment asks for all possible minimized expressions. Therefore, the implementation does not stop after finding the first valid minimum cover. It stores every cover with the same minimum cost.

## Input
Example:

    4
    0 1 0 1
    1 0 0 0
    1 0 0 1
    0 0 0 1

## Output
The program prints the detected variable count, K-map, minterms, number of candidate implicants, number of minimum solutions, and each minimum SOP expression.

## Testing
The project includes test cases for:
- single minterm
- all ones
- pairs
- wrap-around
- overlapping/multiple minimum solutions
- don't-care cells

## Limitation
The exhaustive cover search is intended for 2-, 3-, and 4-variable K-maps used in this lab. It is not intended for large Boolean functions.

## Viva Summary
The key point to explain is that the program first generates valid K-map groups and then searches for covers of all required 1s. Since multiple grouping choices may have equal minimum cost, all tied minimum covers are retained and displayed.
