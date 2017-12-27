document.addEventListener('mouseup', function (mouse) {
    if (mouse.button == 2) {
        var coor = { x: mouse.clientX, y: mouse.clientY, url:window.location.href };
        chrome.runtime.sendMessage(coor);
    }
}) 


var annoText;
var xhttp = new XMLHttpRequest();
xhttp.open("GET", "http://34.210.127.92:8000/list_annotations/?url="+encodeURIComponent(window.location.href));
xhttp.setRequestHeader("Authorization", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTE0MzM1OTU5LCJqdGkiOiJmMzljYzE1NWE2YTA0ODUxOWFhNzljZThiMjI0NGJhOSIsInVzZXJfaWQiOjZ9.U7riDfHeCdt030Mn2LWOF7UYWZ2K70YSKidOCUZyzcw");
xhttp.onload = function(){
    annoText=JSON.parse(this.response)[0].body[0].value;
}
xhttp.send();


var popla=document.createElement("div");
popla.innerHTML="<div class='ui red empty circular label' style='position:absolute; left:500px; top:100px'></div>";
popla.onmouseenter = function(){
    var div=document.createElement("div");
    div.innerHTML="<div class='ui card' style='position:absolute; left:495px; top:120px'><div class='content'><div class='description'>"+annoText+"</div></div></div>";
    popla.appendChild(div);
    console.log("oz");
}
popla.onmouseleave = function(){
    popla.innerHTML="<div class='ui red empty circular label' style='position:absolute; left:500px; top:100px'></div>";
    console.log("an");
}

document.body.appendChild(popla);
console.log("Start Page Script");