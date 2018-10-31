import networkx as nx
import matplotlib.pyplot as plt
import graphviz
from game_core import *


def recursive_play(player_output, cutter_flag=False):
    '''
    this one will check all legal moves in the recusive step

    base case:
        if the graph is a winner
        return the winner

    recursive step:
        return this function 

    player_output is the return value of the cut or save functions
    cutter_flag is a bool for the identity of the player that should play
        True => cutter, False => saver
    '''
    graph = player_output[0]

    # base case
    if player_output[1] == 'saver':
        # draw(graph, 'saver_' + str(hash(graph)))
        return {'saver_wins': 1, 'cutter_wins': 0}
    if player_output[1] == 'cutter':
        # draw(graph, 'cutter_' + str(hash(graph)))
        return {'saver_wins': 0, 'cutter_wins': 1}
    
    # recursive step
    # get all the result dicts in a list
    results = []

    if cutter_flag:
        for edge in list(graph.edges):
            results.append(recursive_play(cut(graph, edge), False))
            
    else: # saver move
        for edge in list(graph.edges):
            # we don't want to remove A or B from the graph when contracting
            # so we make sure A, then B are at the beginning of the edge
            if edge[1] == 'B':
                edge = edge[1], edge[0]
            if edge[1] == 'A':
                edge = edge[1], edge[0]
            results.append(recursive_play(save(graph, edge), True))
                
    # add them together
    output = {'saver_wins': 0, 'cutter_wins': 0}
    for result in results:
        output['saver_wins'] += result['saver_wins']
        output['cutter_wins'] += result['cutter_wins']

    return output


def recursive_algorithmic_play(player_output, cutter_flag=True):
    '''
    this one will check all algorithmically approved moves in the step
        (according to our playing algorithms)
    
    what I need to change is the edges that are recursed into
        so, remove edges from the thing.
        also, run the trim function
    '''
    graph = player_output[0]
    drawn_name = str(hash(graph))
    draw(graph, drawn_name)    
    # base case
    if player_output[1] == 'saver':
        # draw(graph, 'saver_' + str(hash(graph)))
        return (drawn_name, []), {'saver_wins': 1, 'cutter_wins': 0}
    if player_output[1] == 'cutter':
        # draw(graph, 'cutter_' + str(hash(graph)))
        return (drawn_name, []), {'saver_wins': 0, 'cutter_wins': 1}

    trim(graph) # edit the graph in place to remove all extra nodes

    # recursive step
    # get all the result dicts in a list
    results = []
    recursive_step = []

    if cutter_flag: # cutter move
        #TODO
        # get list of edges to try cutting
        move_list = []
        if ('A', 'B') in list(graph.edges()):
            move_list = [('A', 'B')]
        elif nx.has_bridges(nx.Graph(graph)):# cut a bridge between A and B
            # get bridges from a simple graph (not implemented for multi)
            possible_bridges = list(nx.bridges(nx.Graph(graph)))
            # remove the ones that are parallel edges and thus not bridges
            for edge in possible_bridges:
                if (edge[0], edge[1], 1) not in list(graph.edges):
                    move_list.append((edge[0], edge[1], 0))
        elif False: # TODO implement creation of long bridge test
            pass
        else:
            move_list = list(graph.edges)

        for edge in move_list:
            recursive_step.append(recursive_algorithmic_play(cut(graph, edge), False))

    else: # saver move
        # get list of edges to try saving
        # list(graph.edges) is the list of edges in the graph
        move_list = []
        if ('A', 'B') in list(graph.edges()): # winning move for saver
            move_list = [('A', 'B')]
        elif nx.has_bridges(nx.Graph(graph)):# save a bridge between A and B
            # get bridges from a simple graph (not implemented for multi)
            possible_bridges = list(nx.bridges(nx.Graph(graph)))
            # remove the ones that are parallel edges
            for edge in possible_bridges:
                if (edge[0], edge[1], 1) not in list(graph.edges):
                    move_list.append((edge[0], edge[1], 0))
        else:
            move_list = list(graph.edges)

        for edge in move_list:
            # we don't want to remove A or B from the graph when contracting
            # so we make sure A, then B are at the beginning of the edge
            if edge[1] == 'B':
                edge = edge[1], edge[0]
            if edge[1] == 'A':
                edge = edge[1], edge[0]
            recursive_step.append(recursive_algorithmic_play(save(graph, edge), True))

    # we currently have recursive_step as a tuple as below
    
    # get the results for game winners
    results = [item[1] for item in recursive_step]
    # add them together
    output = {'saver_wins': 0, 'cutter_wins': 0}
    for result in results:
        output['saver_wins'] += result['saver_wins']
        output['cutter_wins'] += result['cutter_wins']

    lower_levels = [item[0] for item in recursive_step]

    # graph is the current graph's state
    # lower levels is a list of these tuples
    return (str(hash(graph)), lower_levels), output

import graphviz

def decision_tree_starter(monstrosity):
    graph = graphviz.Digraph(strict=False)

    # create a node with the picture of the drawn graph as a label
    drawn_name = monstrosity[0]
    # draw(graph_to_draw, drawn_name)
    file_address = drawn_name + '.png'
    graph.node(drawn_name, label = f'<<TABLE><TR><TD><IMG SRC="/Users/oskar/Desktop/graph_theory_pics/{file_address}"/></TD></TR></TABLE>>')

    decision_tree(monstrosity, graph, drawn_name)

    return graph

def decision_tree(monstrosity, graph, node):
    '''
    this is a recursive function
    the input it the monstrosity that is returned from the playing function

    the graph is the networkx graph

    the output is a graphviz graph
    the labels all point to images of the intermediate graphs
        in the graphviz style
    '''

    for sub_monstrosity in monstrosity[1]:
        drawn_name = sub_monstrosity[0]
        file_address = drawn_name + '.png'
        graph.node(drawn_name, label = f'<<TABLE><TR><TD><IMG SRC="/Users/oskar/Desktop/graph_theory_pics/{file_address}"/></TD></TR></TABLE>>')
        
        # connect new node to above node
        graph.edge(node, drawn_name, constraint='false')

        decision_tree(sub_monstrosity, graph, drawn_name)

def decision_tree_maker(graph, name):
    graph_copy = setup(graph)
    rec_play = recursive_algorithmic_play(graph_copy)
    print('recursive play done!')
    monstrosity = rec_play[0]
    results = rec_play[1]
    decision_tree_graph = decision_tree_starter(monstrosity)
    decision_tree_graph.render(name)
    print('decision tree done!')
    print(results)
