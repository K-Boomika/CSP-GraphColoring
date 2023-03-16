# **Graph Coloring Problem**
This project implements a solution to the Graph Coloring Problem using Constraint Satisfaction Problem (CSP) with Backtracking Search and Arc Consistency algorithms.

## Problem Statement
We are given a graph in the form of a text file, that we are supposed to color.  The proper vertex coloring 
is such that each vertex is assigned a color and no two adjacent vertices are assigned the same color.

## Implementation
The project contains two Python files:

**GraphColoring.py**: the main file that implements the CSP algorithm with Backtracking Search, Heuristics and Arc Consistency, and provides a solution to the Graph Coloring Problem for a given graph.
**Test_GraphColoring.py**: a unit test file that tests the GraphColoring.py file against several test cases.

The GraphColoring.py file contains the following classes and functions:

- getData(filename): reads the data from a file and returns a tuple containing the number of colors and a list of edges.
- Constraint: an abstract class that represents a constraint that must be satisfied.
- CSP: a class that represents a Constraint Satisfaction Problem.
- MapColoringConstraint: a class that represents a Map Coloring constraint.
- getGraphColoringSolution(data, depth_limit=None): takes a tuple containing the number of colors and a list of edges, and returns a dictionary containing the solution to the Graph Coloring Problem.
- main(): reads the data from a file, gets the solution to the Graph Coloring Problem, and prints it to the console.
- 
The Test_GraphColoring.py file contains several test cases that test the GraphColoring.py file against different test cases.

 ## How to Use
To use the GraphColoring.py file, we need to call the main() function from the command line and pass the filename of the graph as the first argument. Optionally, we can also pass a depth limit as the second argument. The depth limit specifies the maximum depth of the search tree, and it is used to limit the search space.
```$ python GraphColoring.py filename.txt [depth_limit]```

To run the unit tests, you need to run the Test_GraphColoring.py file.
```$ python Test_GraphColoring.py```
