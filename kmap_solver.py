#!/usr/bin/env python3
"""
DLD Lab 5 - K-Map Boolean Expression Minimizer

Reads a 2-, 3-, or 4-variable K-map from a text file and prints
ALL minimum SOP Boolean expressions.

Input:
    The first line may optionally contain the number of variables.
    Otherwise, the number of variables is inferred from the matrix size.

    2 variables -> 2 x 2
    3 variables -> 2 x 4
    4 variables -> 4 x 4

    Cell values may be 0, 1, or X/x (don't-care).

Example input:
    4
    0 1 0 1
    1 0 0 0
    1 0 0 1
    0 0 0 1
"""

from itertools import combinations
import sys
from pathlib import Path

VARIABLES = "abcd"
ALLOWED = {"0", "1", "x"}


def gray_code(bits):
    """Return Gray-code labels in K-map order."""
    if bits == 1:
        return [0, 1]
    if bits == 2:
        return [0, 1, 3, 2]
    raise ValueError("Only 1- or 2-bit Gray codes are needed here.")


def read_kmap(filename):
    """Read and validate a K-map file."""
    raw_lines = Path(filename).read_text(encoding="utf-8").splitlines()
    lines = [line.strip() for line in raw_lines if line.strip() and not line.lstrip().startswith("#")]

    if not lines:
        raise ValueError("Input file is empty.")

    first = lines[0].replace(",", " ").split()
    declared_vars = None

    # Optional first line containing only the number of variables.
    if len(first) == 1 and first[0].isdigit():
        declared_vars = int(first[0])
        lines = lines[1:]

    if not lines:
        raise ValueError("K-map matrix is missing.")

    matrix = [line.replace(",", " ").split() for line in lines]
    rows = len(matrix)
    cols = len(matrix[0])

    if any(len(row) != cols for row in matrix):
        raise ValueError("Every K-map row must have the same number of cells.")

    if (rows, cols) == (2, 2):
        inferred_vars = 2
    elif (rows, cols) == (2, 4):
        inferred_vars = 3
    elif (rows, cols) == (4, 4):
        inferred_vars = 4
    else:
        raise ValueError("Supported K-map sizes are 2x2, 2x4, and 4x4.")

    if declared_vars is not None and declared_vars != inferred_vars:
        raise ValueError(
            f"Declared variable count is {declared_vars}, but the matrix is {rows}x{cols}."
        )

    for row in matrix:
        for value in row:
            if value.lower() not in ALLOWED:
                raise ValueError("Each K-map cell must be 0, 1, or X.")

    return inferred_vars, [[v.lower() for v in row] for row in matrix]


def coordinate_bits(num_vars, row, col):
    """Return the binary assignment represented by a K-map coordinate."""
    if num_vars == 2:
        row_bits = gray_code(1)[row]
        col_bits = gray_code(1)[col]
    elif num_vars == 3:
        row_bits = gray_code(1)[row]
        col_bits = gray_code(2)[col]
    else:
        row_bits = gray_code(2)[row]
        col_bits = gray_code(2)[col]

    return f"{row_bits:0{1 if num_vars == 2 else 2 if num_vars == 4 else 1}b}" + \
           f"{col_bits:0{1 if num_vars == 2 else 2}b}"


def kmap_minterm_map(num_vars):
    """Map each K-map coordinate to its minterm number."""
    rows = 2 if num_vars in (2, 3) else 4
    cols = 2 if num_vars == 2 else 4
    result = {}
    for r in range(rows):
        for c in range(cols):
            bits = coordinate_bits(num_vars, r, c)
            result[(r, c)] = int(bits, 2)
    return result


def power_sizes(limit):
    """Return powers of two up to limit."""
    sizes = []
    value = 1
    while value <= limit:
        sizes.append(value)
        value *= 2
    return sizes


def generate_groups(num_vars, matrix):
    """
    Generate every distinct rectangular K-map group containing only 1/X.
    Wrap-around is handled by modulo indexing.

    A group is represented by its set of (row, col) coordinates.
    """
    rows = len(matrix)
    cols = len(matrix[0])
    groups = {}

    row_sizes = power_sizes(rows)
    col_sizes = power_sizes(cols)

    for height in row_sizes:
        for width in col_sizes:
            for start_r in range(rows):
                for start_c in range(cols):
                    cells = frozenset(
                        ((start_r + dr) % rows, (start_c + dc) % cols)
                        for dr in range(height)
                        for dc in range(width)
                    )

                    if all(matrix[r][c] in {"1", "x"} for r, c in cells):
                        groups[cells] = (height, width)

    return groups


def group_minterms(group, coord_to_minterm, matrix):
    """Return actual 1-minterms covered by a group. X cells are not required."""
    return frozenset(
        coord_to_minterm[cell]
        for cell in group
        if matrix[cell[0]][cell[1]] == "1"
    )


def group_term(group, num_vars, coord_to_minterm):
    """
    Convert a K-map group to a Boolean product term.
    A variable is retained only if its value is constant throughout the group.
    """
    assignments = []
    for cell in group:
        bits = f"{coord_to_minterm[cell]:0{num_vars}b}"
        assignments.append(bits)

    term = []
    for i, variable in enumerate(VARIABLES[:num_vars]):
        values = {bits[i] for bits in assignments}
        if len(values) == 1:
            term.append(variable if "1" in values else variable + "'")

    return "".join(term) if term else "1"


def group_sort_key(item):
    """Stable ordering for readable output."""
    group, term, covered, height, width = item
    return (-len(group), len(term), term, sorted(group))


def build_implicants(num_vars, matrix):
    """Create unique implicants from all valid groups."""
    coord_to_minterm = kmap_minterm_map(num_vars)
    raw_groups = generate_groups(num_vars, matrix)
    implicants = {}

    for group, (height, width) in raw_groups.items():
        covered = group_minterms(group, coord_to_minterm, matrix)
        if not covered:
            continue

        term = group_term(group, num_vars, coord_to_minterm)

        # Same group cells -> same implicant. Keep one representation.
        key = (covered, term)
        implicants[key] = (group, term, covered, height, width)

    return sorted(implicants.values(), key=group_sort_key)


def find_minimum_solutions(implicants, required_minterms):
    """
    Find all minimum SOP covers.

    Primary objective: minimum number of product terms.
    Secondary objective: minimum total number of literals.

    This is exhaustive for the small 2/3/4-variable K-maps used in the lab.
    """
    if not required_minterms:
        return [tuple()]

    candidates = [
        (i, item) for i, item in enumerate(implicants)
        if item[2] & required_minterms
    ]

    by_minterm = {m: [] for m in required_minterms}
    for i, item in candidates:
        for m in item[2] & required_minterms:
            by_minterm[m].append(i)

    # If a required 1 has no candidate, the input is inconsistent.
    if any(not indexes for indexes in by_minterm.values()):
        raise ValueError("Could not find a group covering every 1-cell.")

    # Prefer minterms with fewer choices to reduce search.
    for m in by_minterm:
        by_minterm[m].sort(key=lambda i: (-len(implicants[i][2]), len(implicants[i][1])))

    solutions = set()
    best_key = None

    def search(covered, chosen):
        nonlocal best_key

        if covered >= required_minterms:
            chosen_tuple = tuple(sorted(chosen))
            terms = [implicants[i][1] for i in chosen_tuple]
            key = (len(chosen_tuple), sum(len(t.replace("'", "")) for t in terms))
            # Count literals correctly: each complemented variable is one literal.
            key = (len(chosen_tuple), sum(
                sum(1 for ch in term if ch.isalpha()) for term in terms
            ))

            if best_key is None or key < best_key:
                best_key = key
                solutions.clear()

            if key == best_key:
                solutions.add(chosen_tuple)
            return

        # Lower bound: even in the best case, one new term covers at least this many...
        if best_key is not None and len(chosen) >= best_key[0]:
            return

        # Choose an uncovered minterm with the fewest currently useful candidates.
        uncovered = required_minterms - covered
        target = min(
            uncovered,
            key=lambda m: sum(
                1 for i in by_minterm[m] if i not in chosen and (implicants[i][2] & uncovered)
            )
        )

        for i in by_minterm[target]:
            if i in chosen:
                continue

            newly_covered = implicants[i][2] & required_minterms & uncovered
            if not newly_covered:
                continue

            new_chosen = chosen + [i]

            # Avoid exploring a partial solution that already uses too many terms.
            if best_key is not None and len(new_chosen) > best_key[0]:
                continue

            search(covered | implicants[i][2], new_chosen)

    search(frozenset(), [])

    return sorted(solutions, key=lambda sol: tuple(implicants[i][1] for i in sol))


def format_expression(solution, implicants):
    terms = sorted((implicants[i][1] for i in solution), key=lambda t: (len(t), t))
    return " + ".join(terms)


def print_kmap(matrix):
    print("K-Map:")
    for row in matrix:
        print(" ".join(value.upper() for value in row))


def solve(filename):
    num_vars, matrix = read_kmap(filename)
    coord_to_minterm = kmap_minterm_map(num_vars)

    required = frozenset(
        coord_to_minterm[(r, c)]
        for r in range(len(matrix))
        for c in range(len(matrix[0]))
        if matrix[r][c] == "1"
    )

    print(f"Number of variables: {num_vars}")
    print_kmap(matrix)
    print("\nMinterms with 1:", sorted(required))

    if not required:
        print("\nMinimum Boolean expression:")
        print("F = 0")
        return

    if all(cell in {"1", "x"} for row in matrix for cell in row) and not any(
        cell == "0" for row in matrix for cell in row
    ):
        print("\nMinimum Boolean expression:")
        print("F = 1")
        return

    implicants = build_implicants(num_vars, matrix)
    solutions = find_minimum_solutions(implicants, required)

    print(f"\nCandidate implicants generated: {len(implicants)}")
    print(f"Number of minimum solutions: {len(solutions)}")
    print("\nMinimum Boolean Expressions:")

    for number, solution in enumerate(solutions, start=1):
        print(f"{number}. F = {format_expression(solution, implicants)}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python kmap_solver.py input.txt")
        sys.exit(1)

    try:
        solve(sys.argv[1])
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
