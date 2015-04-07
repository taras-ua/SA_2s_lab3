from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django import forms

import lab3.controllers.main as controller


class GraphForm(forms.Form):
    input_data = forms.IntegerField(min_value=0)


def home(request):
    if request.method == 'GET':
        form = GraphForm(initial={'input_data': 1})
        return render_to_response('home.html', {'form': form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = GraphForm(request.POST)
        if form.is_valid():
            return redirect(controller.build_request(form))
        else:
            return HttpResponse(status=500)


def graph(request):
    graph_json, matrix, eig = controller.get_graph(request)
    return render_to_response('graph.html', {'nodes': graph_json['nodes'],
                                             'edges': graph_json['links'],
                                             'matrix': matrix, 'eigenvalues': eig},
                              context_instance=RequestContext(request))
