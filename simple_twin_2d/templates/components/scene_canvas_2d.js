{% load static %}

var center = [scene_width/2,scene_height/2]

svg = d3.select('#container').append('svg')
.attr('width', scene_width)
.attr('height', scene_height)

var myimage = svg.append('image')
    .attr('xlink:href', image_sas)
    .attr('width', scene_width)
    .attr('height', scene_height)

function createSphere(element,anchor) {
    console.log(anchor,element)
    svg.append('circle')
        .attr('cx', center[0]+(anchor['local_x']*1000))
        .attr('cy', center[1]+(anchor['local_z']*1000)*-1)
        .attr('r', 30)
        .style('fill', 'red')
        .on("mouseover", (event, d) => {
            return tooltip.style("visibility", "visible").html(dictToHtml(element));
        })
        .on("mousemove", (event) => {
            return tooltip.style("top", (event.pageY - 10) + "px").style("left", (event.pageX + 10) + "px")
        })
        .on("mouseout", (event) => {
            d3.pointer(event)
            return tooltip.style("visibility", "hidden");
        });
}


function render(data){
    var guiIter = 0
    for (let i = 0; i < data.length; i++) {
        element = data[i]['objects'][2]
        anchor = data[i]['objects'][3]
        // console.log(element,anchor)
        createSphere(element,anchor)
    }
}
    
    
render(data)