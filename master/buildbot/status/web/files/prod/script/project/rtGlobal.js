define(["jquery","helpers","dataTables","extend-moment"],function(e,t,a,i){var s=e("#buildQueueTotal"),n=e("#buildSlavesTotal"),r=e("#verticalProgressBar"),l=e("#buildLoad"),o=l.find("span"),u=e("#attentionBox"),d={init:function(){requirejs(["realtimePages"],function(e){d.initDataTable();var t=e.defaultRealtimeFunctions();e.initRealtime(t)})},processGlobalInfo:function(e){i.setServerTime(e.utc),t.isRealTimePage()===!1&&u.addClass("show-desktop");var a=e.build_load;s.show(),n.show(),r.show();var d=100>=a?"green":a>=101&&200>=a?"yellow":"red";l.attr({"class":"info-box "+d}).show();var b=e.slaves_count,c=e.slaves_busy/b*100,v=b-e.slaves_busy,f=e.running_builds;t.verticalProgressBar(r.children(),c),r.attr("title","{0} builds are running, {1}, agents are idle".format(f,v)),n.text(b),o.text(a)},initDataTable:function(){var t=void 0;t=e(e(".tablesorter-js").length?".tablesorter-js":"#tablesorterRt"),e.each(t,function(t,i){a.initTable(e(i),{})})}};return d});
//# sourceMappingURL=rtGlobal.js.map