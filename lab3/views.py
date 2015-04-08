from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django import forms

import lab3.controllers.main as controller


class GraphForm(forms.Form):
    graph_matrix = forms.CharField(widget=forms.Textarea())


class RecreateForm(forms.Form):
    x = forms.IntegerField(min_value=1, required=True)
    y = forms.IntegerField(min_value=1, required=True)


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
                                      '   0    0  0.3  0.5    0    0    0    0    0;\n' +
                                      '   0    0  0.1  0.1    0    0    0    0    0'
                                  })
        return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid() and valid_matrix(form):
            return redirect(controller.build_request(form.cleaned_data['graph_matrix']))
        else:
            return HttpResponse(status=500)


def graph(request):
    if request.method == 'GET':
        graph_json, matrix, matrix_json, eig, cycles, stability = controller.get_graph(request)
        form = RecreateForm()
        return render_to_response('graph.html', {'nodes': graph_json['nodes'],
                                                 'edges': graph_json['links'],
                                                 'matrix_html': matrix,
                                                 'matrix_json': matrix_json,
                                                 'eigenvalues': eig,
                                                 'cycles': cycles,
                                                 'stability': stability,
                                                 'form': form},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        form = RecreateForm(request.POST)
        if form.is_valid():
            matrix = request.GET.get('data')
            x = int(form.cleaned_data['x'])
            y = int(form.cleaned_data['y'])
            return redirect(controller.build_request(controller.edit_graph(matrix, x, y)))
        else:
            return HttpResponse(status=500)