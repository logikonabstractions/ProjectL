# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- evaluate two models (etw)
- basis for prompt #2 of this project

## coding notes


## prompt

This codebase is a prototype for a game I am writing. For now, we only use a few pieces & cards, but the full game actually contains a lot more than that. I need you to implement a fuller version of the game. Here is the complete list of pieces:

Level 1: square (1 square only)
Level 2: line (2 squares)
Level 3: line (3 square) and a corner (3 squares)
Level 4: big square (4 squares), line (4 squares), L  shape (3 square, then one to the side)

In addition to adapting the code for those to be loaded at startup, the game currently assumes an endless supply of pieces. In reality, there's a finite bank of pieces of each type. For now, let's just update the code and start the game with 10 instances of each of the pieces. This should be configurable.
