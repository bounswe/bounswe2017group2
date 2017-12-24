var doIt = function(e){
    console.log("oz");
}

chrome.contextMenus.create({
    title: "Add Annotation",
    type: "normal",
    id: "menuItem",
    contexts: ["all"],
    onclick: doIt,
});

console.log("Started Background.js");