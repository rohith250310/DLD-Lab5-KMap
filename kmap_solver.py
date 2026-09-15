from itertools import combinations          # Used to select different groups

variables = "abcd"                           # Variable names
gray = [0, 1, 3, 2]                          # Gray-code order


def read_map():
    # Read all lines from input.txt
    lines = [line.split() for line in open("input.txt") if line.strip()]

    # First line contains number of variables
    n = int(lines[0][0])

    # Remaining lines contain the K-map
    return n, lines[1:]


def get_minterm(n, row, col):
    # 2 variables: rows and columns are normal binary order
    if n == 2:
        return row * 2 + col

    # 3 variables: columns use Gray-code order
    if n == 3:
        return row * 4 + gray[col]

    # 4 variables: both rows and columns use Gray-code order
    return gray[row] * 4 + gray[col]


def find_groups(n, kmap):
    rows = len(kmap)
    cols = len(kmap[0])
    all_groups = []

    # Try every possible group size
    for height in [1, 2, 4]:
        for width in [1, 2, 4]:

            if height > rows or width > cols:
                continue

            # Try starting from every K-map cell
            for start_row in range(rows):
                for start_col in range(cols):

                    cells = []

                    # Create the rectangular group
                    for i in range(height):
                        for j in range(width):
                            row = (start_row + i) % rows
                            col = (start_col + j) % cols
                            cells.append((row, col))

                    # Group is valid if it contains only 1 or X
                    valid = True
                    for row, col in cells:
                        if kmap[row][col].lower() not in ["1", "x"]:
                            valid = False

                    if valid:
                        ones = []

                        # Store minterms containing actual 1s
                        for row, col in cells:
                            if kmap[row][col] == "1":
                                ones.append(get_minterm(n, row, col))

                        if ones:
                            group = (tuple(sorted(cells)), tuple(sorted(ones)))

                            if group not in all_groups:
                                all_groups.append(group)

    return all_groups


def make_term(n, cells):
    # Convert every cell into binary
    binary = []

    for row, col in cells:
        number = get_minterm(n, row, col)
        binary.append(format(number, "0" + str(n) + "b"))

    term = ""

    # Check each variable
    for i in range(n):
        values = []

        for number in binary:
            if number[i] not in values:
                values.append(number[i])

        # Variable is constant in this group
        if len(values) == 1:
            if values[0] == "1":
                term += variables[i]
            else:
                term += variables[i] + "'"

    return term if term else "1"


def solve(n, kmap):
    # Find all required minterms
    required = []

    for row in range(len(kmap)):
        for col in range(len(kmap[0])):
            if kmap[row][col] == "1":
                required.append(get_minterm(n, row, col))

    # Generate all possible groups
    groups = find_groups(n, kmap)

    terms = []

    # Convert groups into Boolean terms
    for cells, ones in groups:
        expression = make_term(n, cells)
        terms.append((expression, ones))

    best = None
    answers = []

    # Try solutions with 1 group, 2 groups, 3 groups, ...
    for number_of_groups in range(1, len(terms) + 1):

        for selected in combinations(terms, number_of_groups):

            covered = []

            # Find all minterms covered by selected groups
            for term, ones in selected:
                for value in ones:
                    if value not in covered:
                        covered.append(value)

            # Check whether every 1 is covered
            if all(value in covered for value in required):

                literal_count = 0

                for term, ones in selected:
                    literal_count += len(term.replace("'", ""))

                score = (number_of_groups, literal_count)
                expression = " + ".join(sorted(term for term, ones in selected))

                if best is None or score < best:
                    best = score
                    answers = [expression]

                elif score == best and expression not in answers:
                    answers.append(expression)

        # Once the minimum number of groups is found, stop
        if best is not None:
            break

    return sorted(answers)


# ---------- Main program ----------

n, kmap = read_map()                         # Read input

print("K-Map:")
for row in kmap:
    print(" ".join(row))

# Display the minterms
minterms = []

for row in range(len(kmap)):
    for col in range(len(kmap[0])):
        if kmap[row][col] == "1":
            minterms.append(get_minterm(n, row, col))

print("\nMinterms:", sorted(minterms))

# Find and display minimum expressions
print("\nMinimum Boolean Expressions:")

answers = solve(n, kmap)

for number, answer in enumerate(answers, 1):
    print(number, "F =", answer)