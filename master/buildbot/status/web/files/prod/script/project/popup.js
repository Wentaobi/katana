define(["jquery","helpers","libs/jquery.form","text!templates/popups.mustache","mustache","timeElements"],function(e,t,n,r,i,s){var o;return o={init:function(){var n=e("#tablesorterRt");o.registerJSONPopup(n),e(".popup-btn-js-2").click(function(t){t.preventDefault(),o.nonAjaxPopup(e(this))}),n.delegate(".popup-btn-js","click",function(n){n.preventDefault();var r=document.URL,i=document.createElement("a");i.href=r;var s=encodeURIComponent(e(this).attr("data-builderName")),u="{0}//{1}/json/pending/{2}/?".format(i.protocol,i.host,s),a=t.codebasesFromURL({}),f=t.urlParamsToString(a);o.pendingJobs(u+f)}),e("#getBtn").click(function(e){e.preventDefault(),o.codebasesBranches()}),n.delegate(".ajaxbtn","click",function(t){t.preventDefault(),o.externalContentPopup(e(this))}),e(".ajaxbtn").click(function(t){t.preventDefault(),o.externalContentPopup(e(this))})},showjsonPopup:function(n){var s=i.render(r,n),o=e(i.render(r,{MoreInfoBoxOuter:!0},{partial:s}));e("body").append(o),n.showRunningBuilds!=undefined&&t.delegateToProgressBar(e("div.more-info-box-js div.percent-outer-js")),t.jCenter(o).fadeIn("fast",function(){t.closePopup(o)})},validateForm:function(t){var n=e(".command_forcebuild",t),s=":button, :hidden, :checkbox, :submit";e(".grey-btn",n).click(function(t){var o=e("input",n).not(s),u=o.filter(function(){return this.name.indexOf("revision")>=0}),a=u.filter(function(){return this.value===""});if(a.length>0&&a.length<u.length){u.each(function(){e(this).val()===""?e(this).addClass("not-valid"):e(this).removeClass("not-valid")}),e(".form-message",n).hide();if(!e(".error-input",n).length){var f=i.render(r,{errorinput:"true",text:"Fill out the empty revision fields or clear all before submitting"}),l=e(f);e(n).prepend(l)}t.preventDefault()}})},nonAjaxPopup:function(n){var r=n.next(e(".more-info-box-js")).clone();r.appendTo(e("body")),t.jCenter(r).fadeIn("fast",function(){t.closePopup(r)}),e(window).resize(function(){t.jCenter(r)})},pendingJobs:function(n){var o=i.render(r,{preloader:"true"}),u=e(o);e("body").append(u).show();var a=document.URL,f=document.createElement("a");f.href=a;var l=f.protocol+"//"+f.host+f.pathname;e.ajax({url:n,cache:!1,dataType:"json",success:function(n){u.remove();var o=i.render(r,{pendingJobs:n,showPendingJobs:!0,cancelAllbuilderURL:n[0].builderURL}),a=e(i.render(r,{MoreInfoBoxOuter:!0},{partial:o})),f=a.find(".waiting-time-js");f.each(function(t){s.addElapsedElem(e(this),n[t].submittedAt),s.updateTimeObjects()}),a.appendTo("body"),t.jCenter(a).fadeIn("fast",function(){t.closePopup(a)})}})},codebasesBranches:function(){var n=e("#pathToCodeBases").attr("href"),s=i.render(r,{preloader:"true"}),u=e(s);e("body").append(u).show();var a=o.htmlModule("Select branches");e(a).appendTo("body"),e.get(n).done(function(n){require(["selectors"],function(r){var i=e("#content1");u.remove();var s=e(n).find("#formWrapper");s.children("#getForm").attr("action",window.location.href);var o=s.find('.blue-btn[type="submit"]').val("Update");s.appendTo(i),t.jCenter(a).fadeIn("fast",function(){r.init(),o.focus(),t.closePopup(a)}),e(window).resize(function(){t.jCenter(a)})})})},customTabs:function(){e(".tabs-list li").click(function(t){var n=e(this).index();e(this).parent().find("li").removeClass("selected"),e(this).addClass("selected"),e(".content-blocks > div").each(function(t){e(this).index()!=n?e(this).hide():e(this).show()})})},externalContentPopup:function(n){var s='<h2 class="small-head">'+n.attr("data-popuptitle")+"</h2>";console.log(s);var u=n.attr("data-b"),a=n.attr("data-indexb"),f=n.attr("data-returnpage"),l=n.attr("data-rt_update"),c=n.attr("data-contenttype"),h=n.attr("data-b_name"),p=i.render(r,{preloader:"true"}),d=e(p),v='<h2 class="small-head">Your build will show up soon</h2>',m=e(i.render(r,{MoreInfoBoxOuter:!0,popUpClass:"green"},{partial:v})),g=e("body");g.append(d);var y=e(i.render(r,{MoreInfoBoxOuter:!0},{partial:s}));y.append(e('<div id="content1"></div>')).appendTo(g);var b={rt_update:l,datab:u,dataindexb:a,builder_name:h,returnpage:f},w=window.location.search.substring(1),E=w.split("&");e.each(E,function(e,t){var n=t.split("=");n[0].indexOf("_branch")>=0&&(b[n[0]]=n[1])});var S=location.protocol+"//"+location.host+"/forms/forceBuild";e.get(S,b).done(function(n){var r=e("#content1");d.remove(),e(n).appendTo(r),t.tooltip(r.find(e(".tooltip"))),c==="form"&&(t.setFullName(e("#usernameDisabled, #usernameHidden",r)),o.validateForm(r)),t.jCenter(y).fadeIn("fast"),e(window).resize(function(){t.jCenter(y)}),t.closePopup(y),f!==undefined&&r.find("form").ajaxForm({beforeSubmit:function(){g.append(m),t.jCenter(m).fadeIn("fast",function(){t.closePopup(e(this)),e(this).delay(1500).fadeOut("fast",function(){e(this).remove()})}),r.closest(".more-info-box").find(".close-btn").click()},success:function(e){requirejs(["realtimePages"],function(t){m.remove();var n=f.replace("_json","");t.updateSingleRealTimeData(n,e)})}})})},htmlModule:function(t){var n=e('<div class="more-info-box remove-js"><span class="close-btn"></span><h3 class="codebases-head">'+t+"</h3>"+'<div id="content1"></div></div>');return n},registerJSONPopup:function(t){t.delegate("a.popup-btn-json-js","click",function(t){t.preventDefault(),o.showjsonPopup(e(this).data()),s.updateTimeObjects()})}},o});