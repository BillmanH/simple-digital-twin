function dictToHtml(d) {
    html = "<div><strong>"+ d['displayname'] +"</strong>" + ": "+ d['name']+ "</div>"
    var dt = Object.assign({}, d);
    for (var k in dt) {
        x = k
        y = dt[k]
        if (y.toString().indexOf(".") != -1) {y = parseFloat(y.toString())};
        if (typeof (y) == "string") {
            y = dt[k]
        } else if (typeof (y) == "number") {
            y = r(y)
        } else if (typeof (y) == "object") {
            y = dt[k].toString()
        }
        html += x + ": " + y + "<br>"
    }
    return html
}
 



var tooltip = d3.select("body")
    .append("div")
    .style("background-color", 'white')
    .attr("id", "hover-tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .style("padding-top", "5px")
    .style("padding-right", "5px")
    .style("padding-bottom", "5px")
    .style("padding-left", "5px")
    .html("<p>Default Text</p>");