define(["jquery","realtimePages","helpers","dataTables","mustache","libs/jquery.form","text!templates/builders.mustache","timeElements","rtGenericTable","popup"],function(t,e,a,l,i,n,s,r,d,u){var o,m;return o={init:function(){m=o.dataTableInit(t(".builders-table"));var l=e.defaultRealtimeFunctions();l.builders=o.realtimeFunctionsProcessBuilders,e.initRealtime(l);var i=t(".dataTables_wrapper .top");""!==window.location.search&&a.codeBaseBranchOverview(i)},realtimeFunctionsProcessBuilders:function(t){r.clearTimeObjects(m),m.fnClearTable();try{m.fnAddData(t.builders),r.updateTimeObjects()}catch(e){}},dataTableInit:function(e){var n={};return n.aoColumns=[{mData:null,sWidth:"20%"},{mData:null,sWidth:"15%"},{mData:null,sWidth:"10%"},{mData:null,sWidth:"15%"},{mData:null,sWidth:"5%"},{mData:null,sWidth:"15%"},{mData:null,sWidth:"10%"},{mData:null,sWidth:"10%",bSortable:!1}],n.aoColumnDefs=[{aTargets:[0],sClass:"txt-align-left",mRender:function(t,e,a){return i.render(s,{name:a.name,friendly_name:a.friendly_name,url:a.url})}},d.cell.buildProgress(1,!1),{aTargets:[2],sClass:"txt-align-left last-build-js",mRender:function(t,e,a){return i.render(s,{showLatestBuild:!0,latestBuild:a.latestBuild})},fnCreatedCell:function(e,l,i){if(void 0!==i.latestBuild){r.addTimeAgoElem(t(e).find(".last-run"),i.latestBuild.times[1]);var n=a.getTime(i.latestBuild.times[0],i.latestBuild.times[1]).trim();t(e).find(".small-txt").html("("+n+")"),t(e).find(".hidden-date-js").html(i.latestBuild.times[1])}}},{aTargets:[3],mRender:function(t,e,a){return i.render(s,{showStatus:!0,latestBuild:a.latestBuild,data:a})},fnCreatedCell:function(e,a,l){var i=void 0===l.latestBuild?"":l.latestBuild;t(e).removeClass().addClass(i.results_text)}},{aTargets:[4],mRender:function(t,e,a){return i.render(s,{showArtifacts:!0,data:a})},fnCreatedCell:function(e,a,l){void 0!==l.latestBuild&&void 0!==l.latestBuild.artifacts&&u.initArtifacts(l.latestBuild.artifacts,t(e).find(".artifact-js"))}},d.cell.revision(5,function(t){return void 0!==t.latestBuild?t.latestBuild.sourceStamps:void 0},a.urlHasCodebases()),d.cell.buildLength(6,function(t){return void 0!==t.latestBuild?t.latestBuild.times:void 0}),{aTargets:[7],mRender:function(t,e,a){return i.render(s,{customBuild:!0,url:a.url,builderName:a.name})},fnCreatedCell:function(e){var a=t(e);u.initRunBuild(a.find(".custom-build"),a.find(".instant-build"))}}],l.initTable(e,n)}}});
//# sourceMappingURL=rtBuilders.js.map