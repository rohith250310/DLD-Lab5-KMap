
from itertools import product          # Imports product() to generate all possible group selections.

V = "abcd"                             # Names of the four Boolean variables.
GRAY = [0, 1, 3, 2]                    # Gray-code order: 00, 01, 11, 10.


# Read the K-map from the input file.
def read_map(file):                    # Function to read the K-map file.
    lines = open(file).read().splitlines()  # Reads the complete file line by line.
    lines = [x for x in lines if x.strip()] # Removes empty lines.

    if lines[0].isdigit():             # Checks whether the first line contains number of variables.
        n = int(lines[0])              # Converts the variable count from text to integer.
        lines = lines[1:]              # Removes the variable-count line.
    else:
        n = 4                          # Assumes four variables if no number is given.

    mp = [x.replace(",", " ").split() for x in lines] # Converts input into a 2D K-map list.
    return n, mp                        # Returns number of variables and K-map.


# Convert K-map position into a minterm.
def minterm(n, r, c):                  # Function to calculate minterm from row and column.
    if n == 4:                         # Handles the four-variable K-map.
        return GRAY[r] * 4 + GRAY[c]   # Uses Gray-code row and column to calculate minterm.
    return 0                           # Placeholder for other variable counts.


# Generate all possible valid groups.
def groups(mp):                        # Function to find K-map groups.
    R, C = len(mp), len(mp[0])         # Gets number of rows and columns.
    ans = set()                        # Stores unique valid groups.

    for h in [1, 2, 4]:                # Tries possible group heights.
        for w in [1, 2, 4]:            # Tries possible group widths.

            if h > R or w > C:         # Checks if the group is larger than the K-map.
                continue               # Skips that group size.

            for r in range(R):         # Tries every possible starting row.
                for c in range(C):     # Tries every possible starting column.

                    cells = frozenset( # Creates the cells belonging to this group.
                        (
                            (r + i) % R, # % allows wrapping from bottom to top.
                            (c + j) % C  # % allows wrapping from right to left.
                        )
                        for i in range(h) # Selects required rows.
                        for j in range(w) # Selects required columns.
                    )

                    if all(             # Checks whether every cell can be grouped.
                        mp[x][y].lower() in ("1", "x") # Group can contain 1 or don't-care X.
                        for x, y in cells # Checks every cell in the group.
                    ):
                        ones = frozenset( # Stores only actual 1-minterms.
                            minterm(4, x, y) # Converts each cell into a minterm.
                            for x, y in cells # Goes through every cell.
                            if mp[x][y] == "1" # Ignores X because X is not required to be covered.
                        )

                        if ones:        # Checks whether the group contains at least one 1.
                            ans.add((cells, ones)) # Saves the valid group.

    return list(ans)                    # Returns all valid groups.


# Convert a group into a Boolean product term.
def make_term(cells):                   # Function to create a Boolean expression from a group.
    bits = [f"{minterm(4, r, c):04b}" for r, c in cells] # Converts minterms into 4-bit binary.
    term = ""                           # Starts with an empty Boolean term.

    for i in range(4):                  # Checks variables a, b, c and d.
        values = {b[i] for b in bits}   # Gets all values of the current variable.

        if len(values) == 1:            # Variable is constant throughout the group.
            term += V[i] if "1" in values else V[i] + "'" # 1 gives normal variable; 0 gives complement.

    return term or "1"                  # Returns the term, or 1 if all variables change.


# Find all minimum Boolean expressions.
def solve(mp):                          # Function that finds the final minimized expressions.

    need = {                            # Creates the set of minterms that must be covered.
        minterm(4, r, c)                # Converts every 1-cell into its minterm.
        for r in range(4)               # Goes through all rows.
        for c in range(4)               # Goes through all columns.
        if mp[r][c] == "1"              # Selects only cells containing 1.
    }

    gs = groups(mp)                     # Generates all valid K-map groups.

    terms = []                          # Stores Boolean terms and their covered minterms.

    for cells, ones in gs:              # Processes every valid group.
        terms.append((make_term(cells), ones)) # Converts the group to a term and stores its minterms.

    best = None                         # Stores the best solution found so far.
    answers = set()                     # Stores all equally minimum solutions.

    # Try every possible selection of groups.
    for size in range(1, len(terms) + 1): # Starts by trying one group, then two, three, etc.
        for chosen in product([0, 1], repeat=len(terms)): # Generates every possible selection of groups.

            if sum(chosen) != size:     # Checks whether exactly 'size' groups were selected.
                continue                # Skips selections with the wrong number of groups.

            covered = set()             # Stores minterms covered by the selected groups.
            selected = []               # Stores Boolean terms selected.

            for i in range(len(terms)): # Checks every available group.
                if chosen[i]:           # Checks whether this group was selected.
                    selected.append(terms[i][0]) # Adds its Boolean term.
                    covered |= terms[i][1]      # Adds its minterms to covered set.

            if covered >= need:         # Checks whether all required 1s are covered.

                key = (                 # Creates a score for this solution.
                    size,               # First priority is fewer product terms.
                    sum(len(x.replace("'", "")) for x in selected) # Second priority is fewer literals.
                )

                if best is None or key < best: # Checks whether this is a better solution.
                    best = key           # Saves the new best score.
                    answers = {" + ".join(sorted(selected))} # Removes old solutions and saves this one.

                elif key == best:       # Checks whether another solution has the same minimum score.
                    answers.add(" + ".join(sorted(selected))) # Saves this additional minimum solution.

        if best is not None:             # Checks whether a valid minimum solution was found.
            break                        # Stops because larger groups of terms are not needed.

    return sorted(answers)               # Returns all minimum Boolean expressions.


# Main program.
n, mp = read_map("input.txt")            # Reads the K-map from input.txt.

print("K-Map:")                           # Prints the K-map heading.

for row in mp:                           # Goes through every row.
    print(" ".join(row))                 # Prints each row neatly.

print("\nMinterms:", sorted(             # Prints the minterms where K-map contains 1.
    minterm(4, r, c)                     # Converts each 1-cell to a minterm.
    for r in range(4)                    # Goes through rows.
    for c in range(4)                    # Goes through columns.
    if mp[r][c] == "1"                   # Selects only 1-cells.
))

print("\nMinimum Boolean Expressions:")   # Prints the final output heading.

for i, answer in enumerate(solve(mp), 1): # Gets every minimum solution and numbers it.
    print(i, "F =", answer)              # Prints each minimized Boolean expression.


