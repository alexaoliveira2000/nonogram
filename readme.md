# Nonogram Solver Algorithm - The Power of Analysis

## Introduction
In this short document I talk about an algorithm developed by me to solve nonogram puzzles, and the power of analyzing these types of problems in order to come up with simple and elegant solutions. The algorithm is open-source, so feel free to reverse engineer it, upgraded it and/or reuse it.

In case you don't know what this puzzle consists of, it is explained right below.

## What is a Nonogram?
*"A nonogram puzzle is a type of logic puzzle that involves filling in cells in a grid to reveal a hidden picture. The puzzle consists of a rectangular grid of cells, typically black-and-white, and a set of clues provided for each row and column.*

*The clues are numbers that indicate the lengths and sequences of consecutive filled cells in that row or column. Using these clues, the goal is to deduce which cells should be filled and which should be left blank, forming a coherent picture when completed."*

*- ChatGPT*

A short example:

![nonogram_example](https://github.com/alexaoliveira2000/nonogram/assets/77057098/57f241c2-6273-42ac-b391-9a9b0e8df08c)

In this document, I explain my thought process, which eventually lead to the developed algorithm. 

## Is Nonogram a solved game?
Nonogram is an NP-complete problem, meaning that until now, there is no efficient algorithms that can solve nonograms. This implies that a programmer can develop his own algorithms and heuristics which may reduce solving time, but there is no right way to do it. It is important to note that nonograms can have multiple solutions or even none, which increases the solving complexity by implying the use of search trees for these problems.

The focus of this algorithm isn't to beat other algorithms solving times (although this can be analysed further), but to solve this game with a big level of abstraction from what a player normally sees when playing. This abstraction is explained further ahead. The developed algorithm shown in this document doesn't have an heuristic for simplicity - instead it searches, in a BFS manner, all possible solutions when it get's stuck.

## Levels of Abstraction

### Level 1 - Grid Squares as Values
Initially, we can easily see that each square of the grid is essentialy a boolean value (especially if we're into programming). In this algorithm, I arbitrarily assign 1 as "painted" square, and 0 as an "unpainted" square. Some algorithms go even deeper, giving a third value in case we are sure that that square will not be painted in the future (typically represented with a cross by players).

A solution, with this level of abstraction, is a matrix of 1's and 0's which respect the given rows and columns sequences. This type of abstraction isn't anything out of this world, especially because this is the main way programmers save this type of data.

![matrix](https://github.com/alexaoliveira2000/nonogram/assets/77057098/03235812-41c5-4828-97cf-19105d5c0cd6)

### Level 2 - Work with Base 10
If we think of each row/column as a list of binary numbers, that list corresponds to a decimal number. This means that instead of having a matrix of NxM size, we can just have a list of N+M size with decimal numbers. The state of the algorithm (the current grid) is then given by this list of decimal numbers, instead of a binary matrix.

![binary_to_decimal](https://github.com/alexaoliveira2000/nonogram/assets/77057098/d51d8a39-a848-494f-b9e9-753c553c7ca3)

Initially, the state is given by a list full of zeros.

### Level 3 - Bit Operations
If we (humans) try to solve this line:

![row_solve](https://github.com/alexaoliveira2000/nonogram/assets/77057098/7a755c95-5b61-4f87-919d-0ea70f6b7ec0)

we can only be sure of a square that is going to be "painted" - the middle one. If you don't understand why, look at this:

![row_solve_solution](https://github.com/alexaoliveira2000/nonogram/assets/77057098/892b7d58-280f-4f30-899c-515c88396858)

The only square that is always painted in every solution is the middle one, hence the certainty.

Here things start getting interesting. In a practical term, the comparison of these 3 solutions can be seen as an AND operator between bits, more specifically between those 3 row possibilities.

![row_solve_solution_binary](https://github.com/alexaoliveira2000/nonogram/assets/77057098/79d2c3ec-45a3-4764-bc81-1dda7302a63f)

So, if we have all row possibilities in a list we can easily check all the certainly "painted" squares. This is especially good in Python, where we can make these comparisons with decimal numbers:
```` py
# 1 1 1 0 0 = 28
# 0 1 1 1 0 = 14
# 0 0 1 1 1 = 7
row_values = [28, 14, 7]

# certain_value = 28 & 14 & 7 = 4 = 0 0 1 0 0
certain_value = reduce(operator.and_,row_values)
````

### Level 4 - Possible Solutions
So far so good. Until now, this information can be enough to solve a grid if we are sure of every square we "paint", but what if we can't be sure without looking further ahead? This is where the solution possibilites come in.

Before starting to solve, every row/column sequence can be transformed into a decimal number. In this algorithm, each row and column sequence is represented by the biggest binary number possible, even if the solution is a smaller number:

![sequences](https://github.com/alexaoliveira2000/nonogram/assets/77057098/322ea0bb-3a42-496f-951b-263e3135f07c)

These numbers are the solutions for each row and column.
Now, why do I do these? It's easier to see with an example. Imagine we have this row:

![possibilities](https://github.com/alexaoliveira2000/nonogram/assets/77057098/09ff7150-2bf0-44f0-b5e9-eb9b2259d1ff)

If we apply what was said earlier, The sequence (1 1) is converted to the binary (1 0 1 0 0), which is converted to the decimal 20. Initially the possibilities are between the number 20 (1 0 1 0 0) and 0 (0 0 0 0 0). We can manually check all the possibilities for the sequence (1 1):
- (1 0 1 0 0) --> 20
- (1 0 0 1 0) --> 18
- (1 0 0 0 1) --> 17
- (0 1 0 1 0) --> 10
- (0 1 0 0 1) --> 9
- (0 0 1 0 1) --> 5

As you can see, the solution is indeed between 0 and 20.

The efficiency comes in when we already have some info about the row/column. By instance, assume we have this information:

![row_solve_info](https://github.com/alexaoliveira2000/nonogram/assets/77057098/eb7a36fd-4130-4caf-a635-7ae1ea13280a)

As we saw earlier, converting the sequence (1 1) to binary we have the decimal 20 (which is the maximum possibility), and converting the already given number (0 1 0 0 0) to decimal we have the number 8. This means that the actual solution is between 8 and 20. Let's check all the possibilities manually:
- (1 0 1 0 0) --> 20 --> 20 & 8 = 0 (no solution)
- (1 0 0 1 0) --> 18 --> 18 & 8 = 0 (no solution)
- (1 0 0 0 1) --> 17 --> 17 & 8 = 0 (no solution)
- (0 1 0 1 0) --> 10 --> 10 & 8 = 10 (solution) --> (0 1 0 1 0)

As you can see, 5 (0 0 1 0 1) is no longer a solution. We just need to check all possibilities between the given number so far (minimum) and the sequence number (maximum). In the example above, 10 is the only possible solution (0 1 0 1 0).

Given this, for every given two positive decimal numbers (for instance, 20 and 8), we can write a function that returns us a list of all possible solutions between them (it works with binary in background!):

```` py
# possible_solutions(20, 0) > [5, 9, 10, 17, 18, 20]
# possible_solutions(20, 8) > [9, 10]
# possible_solutions(20, 9) > [9]
# possible_solutions(20, 12) > []

    solutions = []
    n_min = n_actual if n_actual != 0 else int(bin(n_solution)[2:].rstrip('0'), 2)
    solution_seq = sequence(list(bin(n_solution)[2:]))
    for number in range(n_min, n_solution + 1):
        number_seq = sequence(list(bin(number)[2:]))
        if np.array_equal(number_seq, solution_seq) and number | n_actual == number and number not in solutions:
            solutions.append(number)
    return solutions
````

In summary, this algorithm's core to resolve with certainty a given row/column is:

![row_solve_info](https://github.com/alexaoliveira2000/nonogram/assets/77057098/c81f3123-1d30-43b9-a7c2-0cc0c382c0ba)

- Convert the solution sequence into the biggest decimal: (1 1) --> 1 0 1 0 0 --> 20
- Convert the solution so far into a decimal: (0 1 0 0 0) --> 8
- Get all possible solutions between these numbers: possible_solutions(20, 8) --> [9, 10]
  - 9 --> (0 1 0 0 1)
  - 10 --> (0 1 0 1 0)
- Compute the AND operator between all the possible solutions: reduce(operator.and_, [9, 10]) --> 8
- This means that we are sure that the solution for this row/column will be (0 1 0 0 0) --> 8 (no new information can be added to the grid in this case, which would be the same conclusion a human brain would get by looking at the above picture)
- If, by any means, the possible_solutions function returns 0, it means that the given numbers don't make sense and there's no solution for the given grid (wrong path!)

# Possibilities Search
The way any sane person would resolve a nonogram was to first "paint" the squares that they are sure of, and only then (if necessary), advance to those that require further analysis. We constantly switch between rows and columns because of new information. This algorithm also thinks like this.

After every attempt of "painting" certain squares on all rows and columns, this algorithm saves the grid temporarily in order to compare itself with the next grid (hopefully closer to the solution). If, after trying to reach new certainties, the grid does not get closer to the solution, it begins a tree search for all possibilities - given by the possible_solutions function!

Take a look at this seemingly easy nonogram:

![easy_nonogram](https://github.com/alexaoliveira2000/nonogram/assets/77057098/4242bbae-680c-4ce7-bc08-020301e421cb)

If you notice, this puzzle has two solutions - the two painted diagonals. While for us humans it is easy to see this - because we always think with several threads - it can be hard for computers to see it.

According to my algorithm, it starts by filling all squares that it is sure of being part of the solution. The problem is that there are none. So? It starts looking at every possible solution for the first row, which are the numbers [16, 8, 4, 2, 1]. For each of these possible solutions, the algorithm assumes that this is the right solution, and tries to fill the remaining grid. Eventually, in some search branch, it arrives at a correct solution, while others start making no sense, and giving up on those (returning False).

# In Summary
This algorithm is extremely simple, with the main focus being to abstract ourselves from the grid view and work with simpler data. It solves any given square grid generically, although it can take exponentially more time for puzzles bigger than 15x15. It thinks like a human, firstly solving what we are sure of, and only then what we are unsure.

This is to show the power of analysing a problem and how we can turn a seemingly hard puzzle into something simple using some math and logic, and by ignoring irrelevant "front end" information (such as the grid itself and the solution sequences). Every puzzle has, inherently, vital and simple math behind it. The hard part is to find it.

Alexandre Oliveira
