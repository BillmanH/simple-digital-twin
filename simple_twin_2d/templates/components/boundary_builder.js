function build_canvas(image_sas) {
    scene_width = 1000
    scene_height = 1000

    var center = [scene_width/2,scene_height/2]

    
    svg = d3.select('#container').append('svg')
    .attr('width', scene_width)
    .attr('height', scene_height)

    var myimage = svg.append('image')
        .attr('xlink:href', image_sas)
        .attr('width', scene_width)
        .attr('height', scene_height)
}


