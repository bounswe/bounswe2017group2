var xClick = 0;
var yClick = 0;

var openAnnotationWindow = function(e, tab){
    popupWindow = window.open("popup_window.html","",
        "width=460, height=260, top="+yClick+", left="+xClick);
    console.log("top="+yClick+", left="+xClick);    
}

chrome.runtime.onMessage.addListener(function(msg, sender){
    console.log(msg);
    xClick = msg.x;
    yClick = msg.y;
});

chrome.contextMenus.create({
    title: "Add Annotation",
    type: "normal",
    id: "menuItem",
    contexts: ["all"],
    onclick: openAnnotationWindow,
});

console.log("Started Background.js");