document.addEventListener('mouseup', function(mouse){
    if(mouse.button==2){
        var coor={x: mouse.clientX, y:mouse.clientY};
        chrome.runtime.sendMessage(coor);
    }
});
console.log("Start Page Script");