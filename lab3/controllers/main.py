import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import urllib.parse
from numpy import linalg as la


def build_request(form):
    request = '/graph/?data='
    request += urllib.parse.quote_plus(form.cleaned_data['graph_matrix'].replace('\n', ' ').replace('\r', ''))
    return request


def get_graph(request):
    input_data = request.GET.get('data')
    matrix = np.matrix(input_data)
    graph = nx.from_numpy_matrix(matrix)
    if graph is not None:
        np.set_printoptions(suppress=True, precision=5)
        eigenvals, eigenvecs = la.eig(matrix)
        eigenstring = ''
        matrix_string = ''
        eig_num = 0
        for i in range(eigenvals.size):
            val = eigenvals[i]
            matrix_string += str(matrix[i, :]) + '<br>'
            eig_num += 1
            eigenstring += '<b>&lambda;<sub>' + str(i+1) + '</sub></b> = ' + str(val) + '<br>'
        return json_graph.node_link_data(graph), matrix_string, eigenstring
    return None


