# Nonogram Solver Algorithm
Developed by Alexandre Oliveira in Python.

## Introduction
A nonogram puzzle is a type of logic puzzle that involves filling in cells in a grid to reveal a hidden picture. The puzzle consists of a rectangular grid of cells, typically black-and-white, and a set of clues provided for each row and column.

The clues are numbers that indicate the lengths and sequences of consecutive filled cells in that row or column. Using these clues, the goal is to deduce which cells should be filled and which should be left blank, forming a coherent picture when completed.

![Nonogram Example](/nonogram/nonogram_example.png)

In this document, I explain my thought process, which eventually lead to my developed algorithm. 

## Algorithms
Nonogram is an NP-complete problem, meaning that until now, there is no efficient algorithms that can solve nonograms. This implies that a programmer can develop his own algorithms and heuristics which may reduce solving time. It is important to note that nonograms can have multiple solutions or even none, which increases the solving complexity by implying the use of search trees for these problems.

The focus of this algorithm isn't to beat other algorithms solving times (although this can be analysed further), but to solve this game with a big level of abstraction from what a player normally sees when playing. This abstraction is explained further ahead. The developed algorithm shown in this document doesn't have an heuristic for simplicity - instead it searches, in a BFS manner, all possible solutions when it get's stuck.

## Levels of Abstraction

### Level 1 - Grid Squares as Values
Initially, we can easily see that each square of the grid is essentialy a boolean value (especially if we're into programming). In this algorithm, I assign 1 as "painted" square, and 0 as an "unpainted" square. Some algorithms go even deeper, giving a third value in case we are sure that that square will not be painted in the future (typically represented with a cross by players).

A solution, with this level of abstraction, is a matrix of 1's and 0's which respect the given rows and columns sequences. This type of abstraction isn't anything out of this world, especially because this is the main way programmers save this type of data.

![Row Solve](/nonogram/matrix.png)

### Level 2 - Work with Base 10
If we think of each row/column as a list of binary numbers, that list corresponds to a decimal number. This means that instead of having a matrix of NxM size, we can just have a list of N+M size with decimal numbers. The state of the algorithm (the current grid), is given by this list of decimal numbers, instead of a binary matrix.

![Row Solve](/nonogram/binary_to_decimal.png)

Initially, the state is given by a list full of zeros.

### Level 3 - Bit Operations
If we (humans) try to solve this line:

![Row Solve](/nonogram/row_solve.png)

we can only be sure of a square that is going to be "painted" - the middle one. If you don't understand why, look at this:

![Row Solve](/nonogram/row_solve_solution.png)

The only square that is always painted in every solution is the middle one, hence the certainty.

Here things start getting interesting. In a practical term, the comparison of these 3 solutions can be seen as an AND operator between bits, more specifically between those 3 row possibilities.

![Row Solve](/nonogram/row_solve_solution_binary.png)

So, if we have all row possibilities in a list we can easily check all the certain "painted" squares. This is especially good in Python, where we can make these comparisons with decimal numbers:
```` py
# 1 1 1 0 0 = 28
# 0 1 1 1 0 = 14
# 0 0 1 1 1 = 7
row_values = [28, 14, 7]

# certain_value = 28 & 14 & 7 = 4 = 0 0 1 0 0
certain_value = reduce(operator.and_,row_values)
````

### Level 4 - Solution Possibilities
So far so good. Until now, this information can be enough to solve a grid if we are sure of every square we "paint", but what if we can't be sure without looking further ahead? This is where the solution possibilites come in.

Every row/column sequence can be transformed into a decimal number. In this algorithm, each row and column sequence is represented by the biggest binary number possible, even if the solution is a smaller number:

![Row Solve](/nonogram/sequences.png)

Why do I do these? It's easier to see with an example. Imagine we have this row:

![Row Solve](/nonogram/possibilities.png)

If we apply what was said earlier, The sequence (1 1) is converted to the binary (1 0 1 0 0), which is converted to the decimal 20. Initially the possibilities are between the number 20 (1 0 1 0 0) and 0 (0 0 0 0 0). We can manually check all the possibilities for the sequence (1 1):
- (1 0 1 0 0) --> 20
- (0 1 0 1 0) --> 10
- (0 0 1 0 1) --> 5+

As you can see, the solution is indeed between 0 and 20.

The efficiency comes in when we already have some info about the row/column. By instance, assume we have this information:

![Row Solve](/nonogram/row_solve_info.png)

Converting the sequence (1 1) to binary we have the decimal 20 (which is the maximum possibility), and converting the already given number (0 1 0 0 0) to decimal we have the number 8. This means that the actual solution is between 8 and 20. Let's check manually:
- (1 0 1 0 0) --> 20
- (0 1 0 1 0) --> 10

As you can see, 5 (0 0 1 0 1) is no longer a solution. We just need to check all possibilities between the given number (minimum) and the sequence number (maximum). 












## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading


## Horizontal Rules

___

---

***


## Typographic replacements

Enable typographer option to see result.

(c) (C) (r) (R) (tm) (TM) (p) (P) +-

test.. test... test..... test?..... test!....

!!!!!! ???? ,,  -- ---

"Smartypants, double quotes" and 'single quotes'


## Emphasis

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## Blockquotes


> Blockquotes can also be nested...
>> ...by using additional greater-than signs right next to each other...
> > > ...or with spaces between arrows.


## Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## Code

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```

Syntax highlighting

``` js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```

## Tables

| Option | Description |
| ------ | ----------- |
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

Right aligned columns

| Option | Description |
| ------:| -----------:|
| data   | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |


## Links

[link text](http://dev.nodeca.com)

[link with title](http://nodeca.github.io/pica/demo/ "title text!")

Autoconverted link https://github.com/nodeca/pica (enable linkify to see)


## Images

![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

Like links, Images also have a footnote style syntax

![Alt text][id]

With a reference later in the document defining the URL location:

[id]: https://octodex.github.com/images/dojocat.jpg  "The Dojocat"


## Plugins

The killer feature of `markdown-it` is very effective support of
[syntax plugins](https://www.npmjs.org/browse/keyword/markdown-it-plugin).


### [Emojies](https://github.com/markdown-it/markdown-it-emoji)

> Classic markup: :wink: :crush: :cry: :tear: :laughing: :yum:
>
> Shortcuts (emoticons): :-) :-( 8-) ;)

see [how to change output](https://github.com/markdown-it/markdown-it-emoji#change-output) with twemoji.


### [Subscript](https://github.com/markdown-it/markdown-it-sub) / [Superscript](https://github.com/markdown-it/markdown-it-sup)

- 19^th^
- H~2~O


### [\<ins>](https://github.com/markdown-it/markdown-it-ins)

++Inserted text++


### [\<mark>](https://github.com/markdown-it/markdown-it-mark)

==Marked text==


### [Footnotes](https://github.com/markdown-it/markdown-it-footnote)

Footnote 1 link[^first].

Footnote 2 link[^second].

Inline footnote^[Text of inline footnote] definition.

Duplicated footnote reference[^second].

[^first]: Footnote **can have markup**

    and multiple paragraphs.

[^second]: Footnote text.


### [Definition lists](https://github.com/markdown-it/markdown-it-deflist)

Term 1

:   Definition 1
with lazy continuation.

Term 2 with *inline markup*

:   Definition 2

        { some code, part of Definition 2 }

    Third paragraph of definition 2.

_Compact style:_

Term 1
  ~ Definition 1

Term 2
  ~ Definition 2a
  ~ Definition 2b


### [Abbreviations](https://github.com/markdown-it/markdown-it-abbr)

This is HTML abbreviation example.

It converts "HTML", but keep intact partial entries like "xxxHTMLyyy" and so on.

*[HTML]: Hyper Text Markup Language

### [Custom containers](https://github.com/markdown-it/markdown-it-container)

::: warning
*here be dragons*
:::
