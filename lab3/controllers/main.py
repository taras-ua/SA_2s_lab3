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

def number_of_par_cycles(G,matr):
    cycles_list = nx.simple_cycles(G)
    list_of_par_cycles = []
    for cycle in cycles_list:
        i = 0
        cycle_value = 0
        while i < len(cycle)-1:
            if matr.item((cycle[i], cycle[i+1]))< 0:
                cycle_value -= 1
            else:
                cycle_value += 1
            i+=1
        if (cycle_value % 2 == 0):
            cycle.append(cycle[0])
            list_of_par_cycles.append(cycle)
    return list_of_par_cycles

#matr1 = np.matrix('0 0 1 1;1 0 1 0; 1 1 0 0; 1 0 0 0')
#g1 = nx.from_numpy_matrix(matr1,create_using=nx.DiGraph())
#for element in nx.simple_cycles(g1):
#    print(element)
#matr2 = np.matrix('0.2 0 0.1 0.2; 0.2 0.2 0.2 0; 0.1 0.4 0.6 0.2; 0.1 -0.4 -0.6 -0.2')
#
#result = number_of_par_cycles(g1,matr2)
#print(result)