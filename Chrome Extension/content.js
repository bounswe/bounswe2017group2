document.addEventListener('mouseup', function (mouse) {
    if (mouse.button == 2) {
        var msg = {
            greetings: "right click",
            x: mouse.clientX,
            y: mouse.clientY + window.pageYOffset,
            popupWindowY: mouse.clientY,
            url: window.location.href
        };
        chrome.runtime.sendMessage(msg);
    }
})

function showAnnotations() {
    var annotations;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://34.210.127.92:8000/list_annotations/?url=" + encodeURIComponent(window.location.href));
    xhttp.onload = function () {
        annotations = JSON.parse(this.response);
        var oldAnnos = document.getElementsByClassName("annoPoi");
        console.log(oldAnnos);
        for (anno = oldAnnos.length - 1; anno >= 0; anno--) {
            document.body.removeChild(oldAnnos[anno]);
        }
        var annoPointer = new Array(annotations.length);
        var annoX = new Array(annotations.length);
        var annoY = new Array(annotations.length);
        for (annoN in annotations) {
            (function (annoN) {
                var anno = annotations[annoN];
                var coors = anno.target[0].target_id;
                coors = coors.substring(coors.indexOf('#'));
                annoX[annoN] = parseInt(coors.substring(4, coors.indexOf(',')));
                annoY[annoN] = parseInt(coors.substring(coors.indexOf(',') + 1));
                annoPointer[annoN] = document.createElement("div");
                annoPointer[annoN].className += " annoPoi";
                annoPointer[annoN].innerHTML = "<div class='ui empty circular label' style='background-color: #800000; position:absolute; left:" + annoX[annoN] + "px; top:" + annoY[annoN] + "px'></div>";
                annoPointer[annoN].onmouseenter = function () {
                    var div = document.createElement("div");
                    div.innerHTML = "<div class='ui raised segment' style='text-align:justify; max-width: 300px; position:absolute; left:" + annoX[annoN] + "px; top:" + (annoY[annoN] + 15) + "px'><div class='content'><div class='description'>" + anno.body[0].value + "</div></div></div>"
                    annoPointer[annoN].appendChild(div);
                }
                annoPointer[annoN].onmouseleave = function () {
                    annoPointer[annoN].innerHTML = "<div class='ui empty circular label' style='background-color: #800000; position:absolute; left:" + annoX[annoN] + "px; top:" + annoY[annoN] + "px'></div>";
                }
                document.body.appendChild(annoPointer[annoN]);
            })(annoN);
        }
    }
    xhttp.send();
}

function hideAnnotations() {
    var oldAnnos = document.getElementsByClassName("annoPoi");
    console.log(oldAnnos);
    for (anno = oldAnnos.length - 1; anno >= 0; anno--) {
        document.body.removeChild(oldAnnos[anno]);
    }
}

var isShow;

chrome.runtime.sendMessage({ greetings: "get isShow" }, function (response) {
    isShow = response.isShow;
    if (isShow) showAnnotations();
    else hideAnnotations();
})


chrome.runtime.onMessage.addListener(
    function (msg, sender) {
        if (msg.greetings == "show annos") {
            showAnnotations();
            chrome.runtime.sendMessage({greetings: "set isShow", "isShow": true});
        }
        if (msg.greetings == "hide annos") {
            hideAnnotations();
            chrome.runtime.sendMessage({greetings: "set isShow", "isShow": false});
        }
    }
)

console.log("Start Page Script");