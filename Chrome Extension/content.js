document.addEventListener('mouseup', function (mouse) {
    if (mouse.button == 2) {
        var coor = { x: mouse.clientX, y: mouse.clientY, url: window.location.href };
        chrome.runtime.sendMessage(coor);
    }
})


var annotations;
var xhttp = new XMLHttpRequest();
xhttp.open("GET", "http://34.210.127.92:8000/list_annotations/?url=" + encodeURIComponent(window.location.href));
xhttp.setRequestHeader("Authorization", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTE0MzM4NzYzLCJqdGkiOiI5YWQyODFlOGU5OWQ0ZjI4YWNhZTM5YTE3MDNkYzNlOCIsInVzZXJfaWQiOjZ9.wuvsNSTHGAe3qH8gIdLRrWyYfqLD418nCEYgMk5Y1fw");
xhttp.onload = function () {
    annotations = JSON.parse(this.response);
    var annoPointer = new Array(annotations.length);
    var annoX = new Array(annotations.length);
    var annoY = new Array(annotations.length);
    for (annoN in annotations) {
        (function (annoN) {
            var anno = annotations[annoN];
            console.log(anno);
            var coors = anno.target[0].target_id;
            coors = coors.substring(coors.indexOf('#'));
            annoX[annoN] = parseInt(coors.substring(4, coors.indexOf(',')));
            annoY[annoN] = parseInt(coors.substring(coors.indexOf(',') + 1));
            annoPointer[annoN] = document.createElement("div");
            console.log(annoX[annoN] + ' ' + annoY[annoN] + ' ' + anno.body[0].value);
            annoPointer[annoN].innerHTML = "<div class='ui red empty circular label' style='position:absolute; left:" + annoX[annoN] + "px; top:" + annoY[annoN] + "px'></div>";
            annoPointer[annoN].onmouseenter = function () {
                var div = document.createElement("div");
                div.innerHTML = "<div class='ui card' style='position:absolute; left:" + annoX[annoN] + "px; top:" + annoY[annoN] + "px'><div class='content'><div class='description'>" + anno.body[0].value + "</div></div></div>"
                annoPointer[annoN].appendChild(div);
            }
            annoPointer[annoN].onmouseleave = function () {
                annoPointer[annoN].innerHTML = "<div class='ui red empty circular label' style='position:absolute; left:" + annoX[annoN] + "px; top:" + annoY[annoN] + "px'></div>";
            }
            document.body.appendChild(annoPointer[annoN]);
        })(annoN);
    }
}
xhttp.send();
console.log("Start Page Script");