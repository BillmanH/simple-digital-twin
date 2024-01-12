
function createSphere(element,anchor){

    // console.log(element,anchor)
    const node = BABYLON.MeshBuilder.CreateSphere(element['dtid'][0], {diameter: .05});
    // todo: change the size of anchors to be relevant to .0 and .99
    node.position = new BABYLON.Vector3(anchor['local_x'][0], anchor['local_y'][0], anchor['local_z'][0]);
    console.log(anchor['local_x'])
    console.log(anchor['local_y'])
    console.log(anchor['local_z'])
    console.log(node.position)
    node.anchor = anchor
    node.element = element
    

    const surface = new BABYLON.StandardMaterial("surface");
    node.material = surface

    return node
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