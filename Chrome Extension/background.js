var xClick = 0;
var yClick = 0;
var pageHref;
var popupY;
var isShow = false;

var openAnnotationWindow = function (e, tab) {
    popupWindow = window.open("popup_window.html", "",
        "width=460, height=260, top=" + popupY + ", left=" + xClick);
}

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg.greetings == "right click") {
        xClick = msg.x;
        yClick = msg.y;
        pageHref = msg.url;
        popupY = msg.popupWindowY;
    }
    if (msg.greetings == "get isShow"){
        console.log("get isShow=" + isShow);
        sendResponse({ "isShow": isShow });
    }
    if (msg.greetings == "set isShow"){
        console.log(sender);
        console.log("set isShow="+msg.isShow);
        isShow = msg.isShow;
    }
});

chrome.contextMenus.create({
    title: "Add Annotation",
    type: "normal",
    id: "menuItem",
    contexts: ["all"],
    onclick: openAnnotationWindow,
});

chrome.webNavigation.onHistoryStateUpdated.addListener(function (details) {
    chrome.tabs.executeScript(null, { file: "content.js" });
});

console.log("Started Background.js");