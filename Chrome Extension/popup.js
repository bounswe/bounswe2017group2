window.onload = function () {
    var showButton = document.getElementById("showButton");
    var isShow;
    chrome.runtime.sendMessage({ greetings: "get isShow" }, function (response) {
        isShow = response.isShow;
        if (!isShow) showButton.innerHTML = "Show Annotations";
        else showButton.innerHTML = "Hide Annotations";
        console.log("set Onclick");
        showButton.onclick = function () {
            console.log("Clicked");
            chrome.runtime.sendMessage({ greetings: "get isShow" }, function (response) {
                isShow = response.isShow;
                console.log("isShow=" + isShow);
                if (isShow == false) {
                    chrome.runtime.sendMessage({ greetings: "set isShow", "isShow": true });
                    showButton.innerHTML = "Hide Annotations";
                    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
                        chrome.tabs.sendMessage(tabs[0].id, { greetings: "show annos" });
                    });
                }
                else if (isShow == true) {
                    console.log("should set false");
                    chrome.runtime.sendMessage({ greetings: "set isShow", "isShow": false });
                    showButton.innerHTML = "Show Annotations";
                    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
                        chrome.tabs.sendMessage(tabs[0].id, { greetings: "hide annos" });
                    });
                }
            });
        }
    });
    console.log("Window Onload");
}
console.log("Start Popup");