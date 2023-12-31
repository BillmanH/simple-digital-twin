{% load static %}

const canvas = document.getElementById("renderCanvas");
const engine = new BABYLON.Engine(canvas, true);

const createScene = function () {
    const scene = new BABYLON.Scene(engine);
    scene.clearColor = new BABYLON.Color3.Black;

    const camera = new BABYLON.ArcRotateCamera("Camera", -Math.PI / 2, 0, 2, 0);
    camera.lowerRadiusLimit = 1 
    camera.upperRadiusLimit = 3 
    camera.attachControl(canvas, true);
    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0));

    const ground = BABYLON.MeshBuilder.CreateGround("ground", {height: 1.5, width: 2.5, subdivisions: 4});
    

    const groundMat = new BABYLON.StandardMaterial("groundMat");
    groundMat.diffuseTexture = new BABYLON.Texture("{% static 'assets/pnid1.png' %}")
    ground.material = groundMat;
    
    scene.registerBeforeRender(function () {
        followCamBorderFunc(camera, ground);
    });

    return scene;
}   

const scene = createScene();
engine.runRenderLoop(function () {
    scene.render();
});

function followCamBorderFunc(camera, ground){
    if (camera.beta < 0.1)
        camera.beta = 0.1;
    else if (camera.beta > (Math.PI / 2) * 0.95)
        camera.beta = (Math.PI / 2) * 0.95;
        
    if (typeof lastCameraOffsetX == "undefined") {
        lastCameraOffsetX = camera.position.x;
    }
    if (typeof lastCameraOffsetZ == "undefined") {
        lastCameraOffsetZ = camera.position.z;
    }
    if ((Math.abs(camera.position.x - lastCameraOffsetX) >= camera.cameraOffsetStep) || (Math.abs(camera.position.z - lastCameraOffsetZ) >= camera.cameraOffsetStep)) {

        lastCameraOffsetX = camera.position.x;
        lastCameraOffsetZ = camera.position.z;
        var y = ground.getHeightAtCoordinates(camera.position.x, camera.position.z);
        if ((camera.position.y <= y + 1) ) {
            camera.setPosition(new BABYLON.Vector3(camera.position.x, y + 1, camera.position.z));
        }
    }
}

// Resizing
function resizeCanvas (canvas) {
    canvas.width = window.innerWidth;
    // canvas.width = window.innerWidth - myDrawerWidth;
    canvas.height = window.innerHeight;
    // canvas.height = window.innerHeight - (myHeaderHeight + myFooterHeight);
    }

resizeCanvas(canvas);

window.addEventListener('resize', () => {
resizeCanvas(this._canvas);
this._engine.resize();
});