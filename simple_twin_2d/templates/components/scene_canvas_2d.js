{% load static %}




svg = d3.select('#container').append('svg')
.attr('width', scene_width)
.attr('height', scene_height)

var myimage = svg.append('image')
    .attr('xlink:href', image_sas)
    .attr('width', scene_width)
    .attr('height', scene_height)