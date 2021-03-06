# PyMaze #
by Kai Zhu

Version 1.1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

![picture](scr.png)

An interactive maze generator and solver with GUI implemented in Python.

### Features ###

* Generates custom-sized mazes
* Custom placed starting and end points
* Easily add and remove maze walls by clicking on them
* Automatically generates solution-guaranteed maze if start and end points are set
* BFS maze solver
* GUI
* Tunable parameters for generating organic-looking mazes
* Option to visualize BFS search patterns

### How to use ###
1. Set custom maze column and row counts if needed, press "New" to generate
2. (optional) Click on maze to set start and end points
3. Click "Randomize" to generate random map, if start and end points are set, will guarantee valid path in between
4. Click on walls to add or remove
5. Click on "Solve" to solve maze
6. Check "Show search" and then press "Solve" to visualize BFS search paths

### To-do ###
* Port GUI to Kivy for more design freedom
* Rewrite in C# to port to Unity for a-maze-in 3D?