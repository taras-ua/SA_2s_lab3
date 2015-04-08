import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import urllib.parse
from numpy import linalg as la


def build_request(data):
    request = '/graph/?data='
    request += urllib.parse.quote_plus(data.replace('\n', ' ').replace('\r', ''))
    return request


def make_adjacency(matrix):
    adj = ''
    row_strings = str(matrix).replace('[[', '').replace(']]', '').replace('\n', '').replace('\r', '').split('] [')
    for row in row_strings:
        single_row = row.split()
        for elem in single_row:
            if float(elem) != 0.0:
                adj += '1 '
            else:
                adj += '0 '
        adj += ';'
    return adj[:-2].replace(' ;', '; ')


def get_graph(request):
    input_data = request.GET.get('data')
    matrix = np.matrix(input_data)
    graph = nx.from_numpy_matrix(np.matrix(make_adjacency(matrix)), create_using=nx.DiGraph())
    if graph is not None:
        np.set_printoptions(suppress=True, precision=5)
        eigenvals, eigenvecs = la.eig(matrix)
        eigenstring = ''
        matrix_html = ''
        eig_num = 0
        for i in range(eigenvals.size):
            val = eigenvals[i]
            matrix_html += str(matrix[i, :]) + '<br>'
            eig_num += 1
            eigenstring += '<b>&lambda;<sub>' + str(i+1) + '</sub></b> = ' + str(val) + '<br>'
        return json_graph.node_link_data(graph), matrix_html,\
               str(matrix).replace(']', '],').replace('],],', ']]').replace('\n', '').replace('\r', '').replace('0. ', '0 ').replace(' 0', ', 0').replace(' -0', ', -0').replace('[,', '['),\
               eigenstring,\
               str(list_of_par_cycles(graph, matrix)).replace('[[', '[').replace(']]', ']').replace('], ', ']<br>').replace(',', ' ->')
    return None


def list_of_par_cycles(G, matr):
    cycles_list = nx.simple_cycles(G)
    list_of_par_cycles = []
    for cycle in cycles_list:
        i = 0
        cycle_value = 0
        while i < len(cycle)-1:
            if matr.item((cycle[i], cycle[i+1])) < 0:
                cycle_value -= 1
            else:
                cycle_value += 1
            i += 1
        if cycle_value % 2 == 0:
            cycle.append(cycle[0])
            for i in range(len(cycle)):
                cycle[i] += 1
            list_of_par_cycles.append(cycle)
    return list_of_par_cycles


def edit_graph(matr_string, x, y):
    matr = np.matrix(matr_string)
    matr[x-1, y-1] = 0
    return str(matr).replace('[', '').replace(',', ' ').replace(']]', '').replace(']', ';')
