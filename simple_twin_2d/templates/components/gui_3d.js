var leftUI = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("leftUI");

left_side_control = {
    title: "Side Window",
    top:20,
    left:500,
    width:"400px",
    height:"100px"
}

const label = new BABYLON.GUI.Rectangle(left_side_control.name)
        label.background = 'black'
        label.top = left_side_control.top 
        label.left = left_side_control.left 
        label.width = left_side_control.width
        label.height = left_side_control.height

        label.alpha = 0.5

        label.cornerRadius = 5
        label.thickness = 1
        label.linkOffsetY = 30

    label.verticalAlignment = BABYLON.GUI.Control.VERTICAL_ALIGNMENT_TOP;
    label.horizontalAlignment = BABYLON.GUI.Control.HORIZONTAL_ALIGNMENT_LEFT;

    leftUI.addControl(label);

