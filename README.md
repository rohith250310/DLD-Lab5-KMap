# DLD Lab 5 - K-Map Boolean Expression Minimizer

## 1. Objective

The objective of this assignment is to write a program that reads a Karnaugh map from a file and finds **all possible minimum Sum-of-Products (SOP) Boolean expressions**.

The program supports:

- 2-variable K-maps: 2 x 2
- 3-variable K-maps: 2 x 4
- 4-variable K-maps: 4 x 4
- `0`, `1`, and optional `X`/`x` don't-care cells
- K-map wrap-around adjacency
- overlapping groups
- multiple equally minimum solutions

No external Python packages are required.

---

## 2. K-map convention

The program uses standard Gray-code ordering.

### 2 variables

Rows: `0, 1`  
Columns: `0, 1`

### 3 variables

Rows: `0, 1`  
Columns: `00, 01, 11, 10`

### 4 variables

Rows: `00, 01, 11, 10`  
Columns: `00, 01, 11, 10`

Variables are named `a, b, c, d`.

For a 4-variable map, the row contains the first two variables and the column contains the last two variables.

---

## 3. Input format

The first line may optionally contain the number of variables.

Example:

```text
4
0 1 0 1
1 0 0 0
1 0 0 1
0 0 0 1
```

The program can also infer the number of variables from the matrix size, so the first line may be omitted:

```text
0 1 0 1
1 0 0 0
1 0 0 1
0 0 0 1
```

Use spaces between cells. Commas are also accepted.

`X` means don't-care. It may be used in a group, but it does not have to be covered.

---

## 4. Running the program

Open a terminal in this folder and run:

```bash
python kmap_solver.py input.txt
```

On Windows, if `python` does not work, try:

```bash
py kmap_solver.py input.txt
```

---

## 5. Algorithm

1. Read the K-map from the input file.
2. Validate the matrix dimensions and cell values.
3. Convert K-map coordinates into minterm numbers using Gray-code ordering.
4. Generate all possible rectangular groups whose dimensions are powers of two.
5. Use modulo indexing to handle wrap-around adjacency.
6. Accept groups containing only `1` and `X`.
7. Convert each useful group into a Boolean product term:
   - a variable that remains `1` is included normally.
   - a variable that remains `0` is included with a prime (`'`).
   - a variable that changes is removed.
8. Find combinations of groups that cover every required `1`.
9. Compare valid covers using:
   - first: minimum number of product terms
   - second: minimum total number of literals
10. Print every solution tied for the minimum cost.
11. Duplicate solutions are removed automatically.

---

## 6. Why Gray code?

K-map cells are arranged in Gray-code order so adjacent cells differ in exactly one Boolean variable.

For two bits:

```text
00  01  11  10
```

Notice that the first and last entries are also adjacent in a K-map. This gives the wrap-around property.

---

## 7. Grouping rules implemented

A valid group:

- contains `1` and optionally `X` cells
- has `1, 2, 4, 8, ...` cells
- is rectangular
- may wrap around an edge
- may overlap another group

Diagonal-only cells are not considered adjacent.

---

## 8. Minimum solution definition

The program minimizes in two stages:

### Primary criterion

Minimum number of product terms.

Example:

```text
A + B + C
```

has 3 terms.

### Secondary criterion

If two solutions have the same number of terms, the program chooses the one with fewer total literals.

This gives a consistent and explainable definition of a minimum SOP solution.

If multiple solutions have exactly the same minimum cost, **all of them are printed**.

---

## 9. Example

Input:

```text
4
0 1 0 1
1 0 0 0
1 0 0 1
0 0 0 1
```

The program calculates the K-map using the standard Gray-code convention and prints all minimum expressions according to that convention.

> Note: The assignment handout's sample output should be checked with the instructor's exact K-map ordering. Under standard 4-variable Gray-code ordering, the displayed input has 1-minterms 1, 2, 4, 10, 12 and 14. The expression written in the handout does not evaluate to the same set of minterms, so it appears to contain a typographical or ordering error. Do not silently change the K-map rules just to force an inconsistent sample.

---

## 10. Project structure

```text
DLD_Lab5_KMap/
│
├── kmap_solver.py
├── input.txt
├── requirements.txt
├── README.md
│
├── test_cases/
│   ├── test_2var_single.txt
│   ├── test_2var_allones.txt
│   ├── test_3var_pair.txt
│   ├── test_3var_wrap.txt
│   ├── test_4var_single.txt
│   ├── test_4var_allones.txt
│   ├── test_4var_wrap.txt
│   ├── test_4var_multiple.txt
│   └── test_4var_dontcare.txt
│
└── docs/
    ├── algorithm.md
    └── viva_questions.md
```

---

## 11. Important functions

### `read_kmap()`

Reads the file and validates the K-map.

### `gray_code()`

Creates the Gray-code order used by the K-map.

### `kmap_minterm_map()`

Maps each row/column position to a minterm number.

### `generate_groups()`

Generates all valid power-of-two rectangular groups and handles wrap-around.

### `group_term()`

Converts a group into its Boolean product term.

### `find_minimum_solutions()`

Finds all minimum covers of the required 1-cells.

### `format_expression()`

Formats the final SOP expression for display.

---

## 12. Complexity

For the 2-, 3-, and 4-variable K-maps used in this assignment, the number of cells is at most 16. Therefore, exhaustive generation and cover search is practical.

The algorithm is designed specifically for small K-maps rather than very large Boolean minimization problems.

---

## 13. Viva preparation

Be able to explain:

1. What is a K-map?
2. Why is Gray code used?
3. What is a minterm?
4. What is an SOP expression?
5. Why must groups have powers of two cells?
6. Why are larger groups preferred?
7. What is wrap-around adjacency?
8. Why are diagonal cells not adjacent?
9. Can groups overlap?
10. What is a prime implicant?
11. What is an essential prime implicant?
12. How does a variable disappear from a group?
13. How does the program convert a group into a Boolean term?
14. How does the program find all possible minimum solutions?
15. What happens for all 0s?
16. What happens for all 1s?
17. What is a don't-care?
18. Why are X cells allowed in a group but not required to be covered?
19. Why is exhaustive search acceptable here?
20. What is the time complexity?

---

## 14. Submission checklist

Before submitting:

- [ ] `kmap_solver.py` runs without errors.
- [ ] Input is read from a file.
- [ ] 2-, 3-, and 4-variable maps work.
- [ ] Wrap-around works.
- [ ] Overlapping groups work.
- [ ] Multiple minimum solutions are printed.
- [ ] All-zero case works.
- [ ] All-one case works.
- [ ] README explains the algorithm.
- [ ] Test cases are included.
- [ ] GitHub repository is public/accessibile to the instructor.
- [ ] You can explain every important function during viva.
