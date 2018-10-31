import networkx as nx
import matplotlib.pyplot as plt
import graphviz



def draw(graph, file_name):
    pydot_graph = nx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write_png(f'/Users/oskar/Desktop/graph_theory_pics/{file_name}.png')

def setup(graph):
    '''
    prepare a graph for the game
    assigns the names A and B to two vertices
    creates a multigraph
    returns the prepared graph
    '''
    graph_copy = nx.MultiGraph(graph)

    n = nx.number_of_nodes(graph_copy)
    mapping = {n-2: 'A', n-1: 'B'}
    nx.relabel_nodes(graph_copy, mapping, copy=False)

    return graph_copy, ''
#TODO update the cut, etc. functions to use this dict ^


def cut(graph, edge):
    '''
    returns a copy of the graph with the specified edge deleted

    edge is an edge tuple

    returns tuple of (cut graph, string specifying that the cutter won)
        if the cutter wins via this move tuple[1] == 'cutter'
    '''
    assert edge[0] in graph.neighbors(edge[1]), "Edge doesn't exist"
    
    graph_copy = nx.MultiGraph(graph)

    #remove the edge
    graph_copy.remove_edge(*edge) # the * unpacks the edge tuple

    winner = ''
    if not nx.is_connected(graph_copy):
        if not (nx.node_connected_component(graph_copy, 'A') == nx.node_connected_component(graph_copy, 'B')):
            winner = 'cutter'

    return (graph_copy, winner)

def save(graph, edge):
    '''
    returns a copy of the graph with a contraction along the specified edge

    edge is an edge tuple

    the output works the same way as the cut function
    '''
    assert edge[0] in graph.neighbors(edge[1]), "Edge doesn't exist"

    two_tuple_edge = edge[:2]
    graph_copy = nx.contracted_edge(graph, two_tuple_edge, self_loops=False)
    
    winner = ''
    if 'A' in edge and 'B' in edge:
        winner = 'saver'

    return graph_copy, winner

def trim(graph):
    '''
    edits a graph to only include relevant nodes and edges 
    irrelevant parts include:
        connected components without A or B in them
        vertices that are not on a path between A and B
    '''
    # this is to handle if A and B are contracted so one of them is unfindable
    try:
        all_nodes = set(graph.nodes)

        # connected components without A or B in them
        # get all the nodes in the component with A (and B) in it
        connected_nodes = set(nx.node_connected_component(graph, 'A')) | set(nx.node_connected_component(graph, 'B'))
        non_connected_nodes = all_nodes - connected_nodes
        graph.remove_nodes_from(non_connected_nodes)

        # vertices not on a path between A and B
    
        all_paths = nx.all_simple_paths(graph, 'A', 'B')
        path_nodes = set([node for path in all_paths for node in path])
        non_path_nodes = all_nodes - path_nodes
        graph.remove_nodes_from(non_path_nodes)
    except nx.exception.NodeNotFound:
        pass
    except KeyError:
        pass

