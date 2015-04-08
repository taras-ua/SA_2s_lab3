from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django import forms

import lab3.controllers.main as controller


class GraphForm(forms.Form):
    graph_matrix = forms.CharField(widget=forms.Textarea())


def valid_matrix(form):
    matrix_string = form.cleaned_data['graph_matrix'].replace('\n', ' ').replace('\r', '')
    row_strings = matrix_string.split(';')
    row_count = len(row_strings)
    if row_count < 1:
        return False
    else:
        for row in row_strings:
            if len(row.split()) != row_count:
                return False
    return True


def home(request):
    if request.method == 'GET':
        form = GraphForm(initial={'graph_matrix':
                                      '   0 -0.7    0    0 -0.8 -0.5    0    0    0;\n' +
                                      '-0.5    0    0  0.1 -0.2 -0.3    0 -0.2    0;\n' +
                                      '   0    0    0    0  0.5  0.2    0 -0.1    0;\n' +
                                      '   0    0    0    0 -0.1    0    0 -0.1    0;\n' +
                                      '   0    0  0.2    0    0    0    0    0    0;\n' +
                                      ' 0.1  0.2  0.6    0  0.2    0  0.7  0.1  0.3;\n' +
                                      '   0    0    0    0 -0.1    0    0    0  0.9;\n' +
                                      '   0    0  0.3  0.5    0    0    0    0  0.1;\n' +
                                      '   0    0  0.1  0.1    0    0    0    0    0'
                                  })
        return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid() and valid_matrix(form):
            return redirect(controller.build_request(form))
        else:
            return HttpResponse(status=500)


def graph(request):
    graph_json, matrix, eig = controller.get_graph(request)
    return render_to_response('graph.html', {'nodes': graph_json['nodes'],
                                             'edges': graph_json['links'],
                                             'matrix': matrix, 'eigenvalues': eig},
                              context_instance=RequestContext(request))
