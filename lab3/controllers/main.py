import random
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
from numpy import linalg as la


def build_request(form):
    request = '/graph/?'
    request += 'data={}'.format(form.cleaned_data['input_data'])
    return request


def get_graph(request):
    input_data = int(request.GET.get('data'))
    graph = sample_graph()
    if graph is not None:
        matrix = nx.to_numpy_matrix(graph)
        np.set_printoptions(suppress=True, precision=5)
        eigenvals, eigenvecs = la.eig(matrix)
        eigenstring = ''
        matrix_string = ''
        eig_num = 0
        for i in range(eigenvals.size):
            val = eigenvals[i]
            matrix_string += str(matrix[i, :]).replace('[', '').replace(']', '') + '<br>'
            if val != 0:
                eig_num += 1
                eigenstring += '<b>&lambda;<sub>' + str(eig_num) + '</sub></b> = ' + str(val) + '; '
                eigenstring += '<b>f<sub>' + str(eig_num) + '</sub></b> = ( '
                eigenstring += str(eigenvecs[:, i]).replace('[', '').replace(']', '')
                eigenstring += ' )<sup>T</sup><br>'
        return json_graph.node_link_data(graph), matrix_string, eigenstring


def sample_graph():
    G = nx.MultiDiGraph()
    for i in range(3):
        for j in range(3):
            v = i * 3 + j
            G.add_node(v)
            probability = random.uniform(0, 1)
            prob_sum = 1 / (2 * G.number_of_nodes() - 1)
            if probability < prob_sum:
                G.add_edge(v, v)
            else:
                for node in range(G.number_of_nodes()):
                    prob_sum += G.degree(node) / (2 * G.number_of_nodes() - 1)
                    if probability < prob_sum:
                        G.add_edge(v, node)
                        break
    return G