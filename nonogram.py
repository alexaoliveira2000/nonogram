import numpy as np
import copy
from functools import reduce
import operator

rows = [[1], [1], [1], [1], [2]]
columns = [[1], [1], [1], [1], [1]]

#rows = [[1, 3], [1, 2], [4], [1], [1]]
#columns = [[4], [1, 1], [1, 1], [3], [2]]

#rows = [[3], [1], [1, 2], [2], [2, 2]]
#columns = [[2], [3], [1], [3, 1], [1, 1, 1]]

# rows = [[2, 2, 1], [2, 1, 3, 1], [2, 2], [1, 4], [2, 1, 1, 1], [5, 2], [1, 1, 3], [2, 3], [1, 1, 1, 1], [1, 3, 4]]
# columns = [[1, 3, 2], [1, 2], [1, 3, 1], [2, 2, 1, 1], [1, 2, 2], [5], [2, 1, 1, 1], [1, 1, 5], [2, 3, 1], [3, 1, 3]]

# rows = [[13],[1,1,1,3],[1,3,9],[2,5,1],[1,4,4,1],[4,3,3],[1,2,1,1],[2,1,1,1],[2,7,1],[1,3,5],[2,3,3],[1,2,5],[1,6],[9,1,2],[3,8,1]]
# columns = [[1,1,1,1,1],[2,2,3,2],[1,1,2,1,2],[1,1,2,1,1,2],[6,2,1,1],[1,2,2,3],[3,2,2,2],[1,3,1,4,2],[7,3,2],[6,2,2,1],[6,7],[1,2,2,4,1],[1,1,1,3,1],[1,2,2,3],[1,2,2,3]]

def sequence_value(seq, size):
    if len(seq) == 0:
        return 0
    if seq[0] == 1:
        return 2 ** (size - 1) + sequence_value(seq[1:], size - 2)
    else:
        seq[0] -= 1
        return 2 ** (size - 1) + sequence_value(seq, size - 1)
    
def sequence(bits, seq=None, new_stream=True):
    if seq is None:
        seq = []
    if len(bits) == 0:
        return seq
    elif bits[0] == '0':
        return sequence(bits[1:], seq, True)
    elif new_stream:
        seq.append(1)
    else:
        seq[-1] += 1
    return sequence(bits[1:], seq, False)
    
def possible_solutions(n_solution, n_actual):
    solutions = []
    n_min = n_actual if n_actual != 0 else int(bin(n_solution)[2:].rstrip('0'), 2)
    solution_seq = sequence(list(bin(n_solution)[2:]))
    for number in range(n_min, n_solution + 1):
        number_seq = sequence(list(bin(number)[2:]))
        if np.array_equal(number_seq, solution_seq) and number | n_actual == number and number not in solutions:
            solutions.append(number)
    return solutions

def cross_update(n_updated, n_to_update, index_updated, index_to_update):
    arr_updated = list(bin(n_updated)[2:].zfill(len(rows)))
    arr_to_update = list(bin(n_to_update)[2:].zfill(len(rows)))
    arr_to_update[index_to_update] = arr_updated[index_updated]
    return int(''.join(arr_to_update), 2)

rows_decimal = [sequence_value(value, len(columns)) for value in copy.deepcopy(rows)]
columns_decimal = [sequence_value(value, len(rows)) for value in copy.deepcopy(columns)]
rows_solution = [bin(value) for value in copy.deepcopy(rows_decimal)]
columns_solution = [bin(value) for value in copy.deepcopy(columns_decimal)]

def is_solved(solution):
    for i in range(len(solution[0])):
        if bin(solution[0][i]).count('1') != rows_solution[i].count('1'):
            return False
        if bin(solution[1][i]).count('1') != columns_solution[i].count('1'):
            return False
    return True

def print_solution(solution):
    biggest_row = len(max(rows, key=len))
    biggest_col = len(max(columns, key=len))
    for i in range(biggest_col, 0, -1):
        row = '   ' * biggest_row + '\t  '
        for j in range(len(columns)):
            row += (str(columns[j][len(columns[j]) - i]) if len(columns[j]) >= i else " ") + "   "
        print(row)
    for i in range(len(solution[0])):
        row_sequence = [str(element) for element in rows[i]]
        row_sequence = [' '] * (biggest_row - len(row_sequence)) + row_sequence
        row = '   '.join(str(element) for element in row_sequence)
        row += "\t| "
        binary_row = list(bin(solution[0][i])[2:].zfill(len(rows)))
        for j in range(len(binary_row)):
            row += ("X" if binary_row[j] == '1' else " ") + " | "
        print(row)

def solve(solution = np.zeros((2, len(rows))).astype(int), last_solution = None):

    for i in range(len(columns)):
        possibilities = possible_solutions(columns_decimal[i], solution[1][i])
        if len(possibilities) == 0:
            return False
        solution[1][i] = reduce(operator.and_,possibilities)
        for j in range(len(rows)):
            solution[0][j] = cross_update(solution[1][i], solution[0][j], j, i)

    for i in range(len(rows)):
        possibilities = possible_solutions(rows_decimal[i], solution[0][i])
        if len(possibilities) == 0:
            return False
        solution[0][i] = reduce(operator.and_,possibilities)
        for j in range(len(columns)):
            solution[1][j] = cross_update(solution[0][i], solution[1][j], j, i)

    if is_solved(solution):
        return solution

    if np.all(solution == last_solution):
        for i in range(len(columns)):
            possibilities = possible_solutions(columns_decimal[i], solution[1][i])
            if len(possibilities) > 1:
                for p in range(len(possibilities)):
                    solution[1][i] = possibilities[p]
                    new_solution = solve(copy.deepcopy(solution), copy.deepcopy(solution))
                    if np.any(new_solution):
                        return new_solution
        return False
    
    return solve(solution, copy.deepcopy(solution))

solution = solve()
if np.any(solution):
    print_solution(solution)
else:
    print("Unsolvable")