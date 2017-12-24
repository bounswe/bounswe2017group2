chrome.runtime.onConnect.addListener(function(port){
    console.log("connect");
    port.onMessage.addListener(function(msg){
        document.getElementById("clickCoor").innerHTML="oz";
    });
});
console.log("Start Popup");