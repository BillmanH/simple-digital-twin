var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");

var textblock = new BABYLON.GUI.TextBlock();
    textblock.text = "Side Window";
    textblock.fontSize = 24;
    textblock.top = -100;
    textblock.color = "white";
    advancedTexture.addControl(textblock);
    
advancedTexture.addControl(button1);   