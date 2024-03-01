const NODE_RADIUS = 10
const NODE_COLOR = 'red'

var data = {"nodes":[],
        "tags":[]}

function build_canvas(image_sas) {

    scene_width = 1000
    scene_height = 1000    
    svg = d3.select('#container').append('svg')
        .attr('width', scene_width)
        .attr('height', scene_height)
        .style('border', '1px solid black')
        .on('click', function(event) {
            var coordinates = d3.pointer(event)
            var x = coordinates[0];
            var y = coordinates[1];
            var scaled = scale_coordinates(x, y)
            console.log('Clicked position: ', x,",", y, "Scaled: ", scaled);
            create_node(x, y, NODE_RADIUS)
        });

    var center = [scene_width/2,scene_height/2]

    var myimage = svg.append('image')
        .attr('xlink:href', image_sas)
        .attr('width', scene_width)
        .attr('height', scene_height)
}

function create_node(x, y, r) {
    var i = data.nodes.length
    var node_id = 'node' + i
    var node_coords = scale_coordinates(x, y)
    data.nodes.push({'id': node_id, 'x': node_coords[0], 'y': node_coords[1]})
    svg.append('circle')
        .attr('cx', x)
        .attr('cy', y)
        .attr('r', r)
        .attr('id', node_id)
        .attr('fill', NODE_COLOR)
        .style('border', '1px solid black')

    svg.selectAll('circle')
        .on('mouseover', function(event, d) {
            tooltip();
        })
        .on('mousemove', function(event, d) {
            var coordinates = d3.pointer(event)
            var x = coordinates[0];
            var y = coordinates[1];
            tooltip.style('visibility', 'visible')
                .style('top', (event.pageY-10)+'px')
                .style('left', (event.pageX+10)+'px')
                .text('Node: ' + d.id + ' at (' + d.x + ', ' + d.y + ')');
        })
        .on('mouseout', function(event, d) {
            tooltip.style('visibility', 'hidden')
        })
        
    console.log("data: ",data)
}

function scale_coordinates(x, y) {
    var scale = 2 / (scene_width - 1);
    var center = [scene_width / 2, scene_height / 2];
    var new_x = (x - center[0]) * scale;
    var new_y = (center[1] - y) * scale;
    return [new_x, new_y];
}
    

var tooltip = d3.select('#container').append('div')
    .style('position', 'absolute')
    .style('visibility', 'hidden')
    .style('background', 'white')
    .style('border', '1px solid black')
    .style('padding', '5px')
    .text('This is a tooltip');
