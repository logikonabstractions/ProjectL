# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- raven-etw-2-base 


## coding notes
I realise that the cube generation is actually only implementing translations of the base layout provided in the config file. Actually, it should generate all translations for all distinct rotations of a piece. E.g. the class Piece.generate_cube(...), taking for example the piece corner_3 from the configs, only generates 16 layouts (all valid translations that remain fully within the 5x5 card matrix). But in fact it should generate 64, since we can do 4 rotated translations that result in distinct configurations. Please adapt the Piece class and its cube generation so it properly generates all configurations. This should be clearer with the comments in the code. 

## prompt


## Projet TODO
- implement rotations for cube generations (currently only implements translations of the base pieces)
