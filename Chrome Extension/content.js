function sendCoordinates(){
    var port = chrome.runtime.connect({ name: "LFCConnect" });
    port.postMessage({x: event.pageX, y: event.pageY});
}
console.log("Start Page Script");