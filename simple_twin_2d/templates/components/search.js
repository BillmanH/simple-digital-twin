function produce_searches(data){
    var results_pane = document.getElementById("search_results");
    // console.log(data['search_results'])
    for (i=0; i < data['search_results'].length; i++){
        console.log(data['search_results'][i]);
        item = results_pane.appendChild(document.createElement('div'));
        item.className = "search_result";

        var nodeName = data['search_results'][i]['objects'][0]['displayname']
        var nodeID = data['search_results'][i]['objects'][0]['description']

        var boundaryName = data['search_results'][i]['objects'][2]['displayname']
        var boundaryID = data['search_results'][i]['objects'][2]['dtid']
        var childNode = document.createElement('p');
        childNode.innerHTML = "displayname: " + nodeName + " <br> description: " + nodeID;


        link = document.createElement('a');
        link.innerHTML = boundaryName;
        link.href = 'http://localhost:8000/simple_twin_2d/2d/twin/?boundary_id=' + boundaryID;
        
        // childNode.appendChild(link)

        item.appendChild(childNode);
        item.appendChild(link);
        
        
    }
}   


