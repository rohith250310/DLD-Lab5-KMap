# DLD Lab 5 Viva Questions and Answers

## 1. What is a K-map?
A Karnaugh map is a graphical method for simplifying Boolean expressions.

## 2. Why do we use a K-map?
It groups adjacent minterms so changing variables can be eliminated and the Boolean expression becomes simpler.

## 3. What is Gray code?
Gray code is an ordering in which consecutive values differ in exactly one bit.

## 4. Why is Gray code used in a K-map?
Because adjacent K-map cells must represent minterms differing in only one variable.

## 5. What group sizes are allowed?
1, 2, 4, 8, 16, etc. In other words, powers of two.

## 6. Why are larger groups preferred?
A group of 2 eliminates one variable, a group of 4 eliminates two, a group of 8 eliminates three, and so on.

## 7. Can groups overlap?
Yes. Overlap is allowed and may be necessary to obtain a minimum expression.

## 8. Can groups wrap around?
Yes. The first and last rows/columns can be adjacent.

## 9. Can diagonal cells be grouped?
No. Diagonal cells are not directly adjacent in a K-map.

## 10. What is a minterm?
A minterm is a product term containing every variable exactly once, either complemented or uncomplemented.

## 11. What is SOP?
SOP means Sum of Products: OR of product terms.

Example:

```text
a'b + cd
```

## 12. How does a variable disappear?
If a variable has both 0 and 1 values inside a valid group, it changes and is therefore eliminated.

## 13. How does the program generate groups?
It tries all power-of-two rectangular sizes and all possible starting positions, using modulo indexing for wrap-around.

## 14. Why does modulo help?
For example, `(column + 1) % number_of_columns` moves from the last column back to the first column.

## 15. What is a prime implicant?
A valid implicant that cannot be enlarged to a larger valid implicant.

## 16. What is an essential prime implicant?
A prime implicant that covers at least one required minterm not covered by any other prime implicant.

## 17. Why does the program find all solutions?
Different grouping combinations can have the same minimum cost. The assignment specifically asks for all possible minimized expressions.

## 18. How does the program decide which solution is minimum?
First it minimizes the number of product terms. If tied, it minimizes total literals.

## 19. What happens if there are no 1s?
The function is:

```text
F = 0
```

## 20. What happens if every cell is 1?
The function is:

```text
F = 1
```

## 21. What is X?
X is a don't-care value. It can be included in a useful group but does not need to be covered.

## 22. Why don't we require X cells to be covered?
Because X represents an input condition whose output can be treated as either 0 or 1 for simplification.

## 23. Why is exhaustive search acceptable?
A 4-variable K-map has only 16 cells, so the number of possible groups and covers is small enough for this lab problem.

## 24. Why not use a large optimization library?
The purpose of the lab is to demonstrate the K-map algorithm. Implementing the grouping and cover search ourselves makes the working explainable.

## 25. What data structure stores the K-map?
A Python list of lists represents the matrix.

## 26. How are groups represented?
Each group is stored as a set of `(row, column)` coordinates.

## 27. How are minterms found?
Each K-map coordinate is converted to a binary assignment using the Gray-code row and column labels.

## 28. Why are duplicate groups removed?
Different starting positions can generate the same wrapped group. A set/frozenset representation makes duplicate cell sets identical.

## 29. What is the output format?
Each solution is printed as an SOP expression using `+` for OR and `'` for NOT.

## 30. What is the main limitation?
The exhaustive cover search is intended for small K-maps (2 to 4 variables). It is not intended as a scalable replacement for algorithms such as Quine-McCluskey or Espresso for very large Boolean functions.

---

# Viva explanation of the complete program

A good 30-second answer:

"My program reads a K-map from a text file and first determines whether it is a 2-, 3-, or 4-variable map. I use Gray-code ordering to map each K-map cell to a minterm. Then I generate every valid rectangular group whose dimensions are powers of two. Modulo indexing handles wrap-around adjacency. Groups containing only 1 and don't-care cells are converted into Boolean product terms by keeping only variables that remain constant in the group. Finally, I search for combinations of these groups that cover every required 1. I compare the valid covers by number of terms and then number of literals, and I print every cover with the minimum cost."
