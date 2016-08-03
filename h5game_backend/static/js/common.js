// check is weixin browser
// only support open in weixin

var isWeixin = false;

if (typeof WeixinJSBridge == "object" && typeof WeixinJSBridge.invoke == "function") {
    isWeixin = true;
} else {
    if (document.addEventListener) {
        document.addEventListener("WeixinJSBridgeReady", function() { isWeixin = true; }, false);
    } else if (document.attachEvent) {
        document.attachEvent("WeixinJSBridgeReady", function() { isWeixin = true; });
        document.attachEvent("onWeixinJSBridgeReady", function() { isWeixin = true; });
    }
}