function buildGraph(nodes, edges, matrix, stability) {
    var container = document.getElementById('graph-canvas');
    var visEdges = [];
    var visNodes = [];
    for(var j = 0; j < nodes.length; j++) {
        visNodes.push({id: nodes[j].id, label: (nodes[j].id + 1).toString()});
    }
    for(var i = 0; i < edges.length; i++) {
        visEdges.push({from: edges[i].source, to: edges[i].target, label: matrix[edges[i].source][edges[i].target],
            style:'arrow', length: 200,
            color: {
                color: matrix[edges[i].source][edges[i].target] > 0 ? '#990000' : '#3232ff',
                highlight: matrix[edges[i].source][edges[i].target] > 0 ? '#990000' : '#3232ff',
                hover: matrix[edges[i].source][edges[i].target] > 0 ? '#990000' : '#3232ff'
            }});
    }
    var data = {
        nodes: visNodes,
        edges: visEdges
    };
    var jContainer = $('#graph-canvas');
    var options = {
        width: jContainer.width().toString() + 'px',
        height: jContainer.height().toString() + 'px'
    };
    var network = new vis.Network(container, data, options);

    // stability mark
    for(var k = 0; k < 3; k++) {
        $('#stab' + k).attr("src", '/static/' + (stability[k] > 0 ? 'yes' : 'no') + '.png');
    }
}