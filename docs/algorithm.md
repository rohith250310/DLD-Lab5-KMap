# Algorithm Explanation

## Input
A K-map is supplied as a matrix in a text file.

## Step 1: Determine variables
The program supports:
- 2 variables -> 2x2
- 3 variables -> 2x4
- 4 variables -> 4x4

## Step 2: Gray-code mapping
The coordinate positions are converted into binary assignments using Gray-code order.

For 4 variables:

```text
       cd
       00 01 11 10
ab 00
   01
   11
   10
```

## Step 3: Generate groups
The program considers rectangle sizes whose height and width are powers of two.

For a 4x4 map:
- 1x1
- 1x2
- 1x4
- 2x1
- 2x2
- 2x4
- 4x1
- 4x2
- 4x4

Modulo indexing makes the rectangles wrap around the edges.

## Step 4: Validate groups
A group is valid when every cell is `1` or `X`.

A group containing no `1` is discarded because it does not help cover the function.

## Step 5: Convert group to term
For every variable:
- constant 1 -> variable appears
- constant 0 -> complemented variable appears
- both 0 and 1 occur -> variable disappears

Example:

```text
a=0, b=0, c changes, d=1
```

gives:

```text
a'b'd
```

## Step 6: Cover all 1s
The program searches for combinations of useful groups such that every `1` cell is covered.

`X` cells are not included in the required set.

## Step 7: Select minimum solutions
Each valid cover is assigned:

```text
(number of product terms, total number of literals)
```

The smallest pair is selected.

All covers with the same smallest pair are retained.

## Step 8: Print
The selected covers are converted to:

```text
term1 + term2 + term3
```

and printed as separate minimum expressions.
