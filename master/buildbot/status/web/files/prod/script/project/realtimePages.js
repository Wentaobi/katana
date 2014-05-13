define(["jquery","rtglobal","helpers","timeElements"],function(e,t,n,r){var i=null,s={},o={},u={},a="krtJSONData",f="krtURLDropped",l="krtRegisterURL",c=3e4,h=3e4,p=5e3,d={createWebSocket:function(t){return i==null&&("WebSocket"in window?i=new WebSocket(t):"MozWebSocket"in window?i=new MozWebSocket(t):(log("Browser does not support WebSocket!"),window.location="http://autobahn.ws/unsupportedbrowser"),i&&(i.onopen=function(){e("#bowlG").remove(),e.each(o,function(e,t){d.sendCommand(l,t)})},i.onclose=function(){i=null,console.log("We lost our connection, retrying in {0} seconds...".format(h/1e3)),setTimeout(function(){d.createWebSocket(t)},h)},i.onmessage=function(e){var t=e.data;typeof t=="string"&&(t=JSON.parse(t)),d.parseRealtimeCommand(t)})),i},initRealtime:function(t){s=t;var n=d.getInstantJSON();n!==undefined&&(console.log("Loaded from instant JSON"),d.updateRealTimeData(n,!0));var r=e("body").attr("data-realTimeServer");r!==undefined&&r!=""?(console.log(r),d.createWebSocket(r)):console.log("Realtime server not found, disabling realtime.")},sendCommand:function(e,t){if(i){var n=JSON.stringify({cmd:e,data:t});i.send(n)}},parseRealtimeCommand:function(e){e.cmd===a&&d.updateRealTimeData(e.data,!1),e.cmd===f&&(console.log("URL Dropped by server will retry in {0} seconds... ({1})".format(c/1e3,e.data)),setTimeout(function(){d.sendCommand(l,e.data)},c))},updateRealTimeData:function(t,n){if(n===!0)e.each(t,function(e,t){var n=t.data;typeof n=="string"&&(n=JSON.parse(n),o[e]=t.url),d.updateSingleRealTimeData(e,n)});else{var r=d.getRealtimeNameFromURL(t.url);d.updateSingleRealTimeData(r,t.data)}},getRealtimeNameFromURL:function(t){var n=undefined;return e.each(o,function(e,r){return r===t?(n=e,!1):!0}),n},updateSingleRealTimeData:function(e,t,n){var r=!0,i=new Date;(n==undefined||!n)&&u.hasOwnProperty(e)&&i-u[e]<p&&(r=!1),r&&s.hasOwnProperty(e)&&(s[e](t),u[e]=i,console.log("Reloading data for {0}...".format(e)))},getInstantJSON:function(){var t=e("#instant-json");return e("#bowlG").remove(),e(".initjson").show(),t.length?(t.remove(),instantJSON):undefined},defaultRealtimeFunctions:function(){return{global:t.processGlobalInfo}}};return d});