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


        link2d = document.createElement('a');
        link2d.innerHTML = boundaryName + " 2D View";
        link2d.href = '/simple_twin_2d/2d/twin/?boundary_id=' + boundaryID;

        link3d = document.createElement('a');
        link3d.innerHTML = boundaryName + " 3D View";
        link3d.href = '/simple_twin_2d/3d/twin/?boundary_id=' + boundaryID;

        item.appendChild(childNode);
        item.appendChild(link2d);
        item.appendChild(document.createElement('p'));
        item.appendChild(link3d);
        
        
    }
}   


