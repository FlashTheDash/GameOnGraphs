#Game on Graphs
This repository includes code that was used to simulate a game on graphs for a Graph Theory final project.

This project was not done with the intent of being easily portable, so there are some variables that need to be changed in order for everything to work on other people's computers. Off the top of my head, this mostly means that some directory addresses will need to be changed.

##Dependencies
This project is dependent on the [networkx](https://networkx.github.io) and [graphviz](https://github.com/xflr6/graphviz) python libraries and on the [graphviz](http://www.graphviz.org) graph visualization software.

##Functions
A brief description of what most of the functions do:

###game\_core.py
- draw: creates an image of the input graph
- setup: prepares a standard networkx graph for the game (labels vertices A and B, etc.)
- cut: performs the cut operation on a graph, on a specified edge
- save: performs the save operation (contraction for the purposes of the simulation) on a graph, on a specified edge
- trim: removes all edges and vertices not on a path between A and B to increase simulation efficiency
###simulator.py
- recursive\_play: this is a recursive function that simulates all possible outcomes of a game on the input graph
- recursive\_algorithmic\_play: similar to recursive\_play, this function only checks moves that fall under the heuristics that we created to increase efficiency for larger graphs
- decision\_tree\_starter, decision\_tree, and decision\_tree\_maker: these functions operate recursively to create a decision tree of all possible outcomes that follow basic optimal play, as defined in the paper
###efficient\_sim.py
This is the same as simulator.py, but the decision tree maker functionality is modified to significantly reduce memory usage while the program runs
###create\_petersen\_tree.py
This file can be excecuted in order to create a decision tree for a game played on the petersen graph. It turns out that the petersen graph is sufficiently complex to make this take way too long. I do not recommend running this file, but it can be used as an example of how to use the code otherwise. 




