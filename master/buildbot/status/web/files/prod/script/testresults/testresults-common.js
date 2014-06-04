define(["jquery","moment","helpers","datatables-plugin"],function(t,e,i){var n,a,s={dataTablesInit:function(){t.fn.dataTableExt.oApi.fnFilterAll=function(e,i,n,s,r){var o,l=t.fn.dataTableSettings;for(o=0;o<l.length;o+=1)l[o].oInstance.fnFilter(i,n,s,r);t(".dataTables_empty").closest(a).hide()},jQuery.fn.dataTableExt.oApi.fnFilterOnReturn=function(){var e=this;return this.each(function(i){t.fn.dataTableExt.iApiIndex=i;var n=t("input",e.fnSettings().aanFeatures.f);return n.unbind("keyup").bind("keypress",function(a){13===a.which&&(t.fn.dataTableExt.iApiIndex=i,e.fnFilter(n.val()))}),this}),this},n=t(".tablesorter-log-js").dataTable({asSorting:!1,bPaginate:!1,bFilter:!0,bSort:!1,bInfo:!1,bAutoWidth:!1})},addFailureButtons:function(){t(".failure-detail-cont",a).each(function(){var e=t(".failure-detail-txt",this);e.text(e.text().trim()),t(this).height(e.height()+40),e.is(":empty")||(t('<a href="#" class="new-window var-3 grey-btn">Open new window</a>').insertBefore(e),e.height()>=130&&t('<a class="height-toggle var-3 grey-btn" href="#">Show more</a>').insertBefore(e))}),t(".new-window").click(function(e){e.preventDefault();var i=t(this).parent().find(t(".failure-detail-txt")).html();s.openNewWindow(i)}),t(".height-toggle").click(function(e){e.preventDefault();var i=t(this).parent().find(t(".failure-detail-txt")),n=t(this).parent().parent();i.css({"max-height":"none",height:""}),t(this).hasClass("expanded-js")?(t(this).removeClass("expanded-js"),t(this).text("Show more"),i.css("max-height",130),n.css("height",170)):(t(this).addClass("expanded-js"),t(this).text("Show less"),i.css("height",""),n.css("height",i.height()+40))})},parseTimes:function(){t.each(t("[data-time]"),function(i,n){var a=1e3*parseFloat(t(n).attr("data-time")),s=e.utc(a).format(" (HH:mm:ss)");t(n).append(s)})},filterCheckboxes:function(){var e=t("#CheckBoxesList").find("input:checked"),i=[];a.show(),e.each(function(){i.push("("+t(this).val()+")")}),n.fnFilterAll(i.join("|"),1,!0)},setupFilterButtons:function(){var e=t("#filterinput"),i=t("#submitFilter"),n=t(".log-main").attr("data-failed-tests");e.keydown(function(t){var e=window.event||t;13===e.keyCode&&s.filterTables(this.value)}),i.click(function(){s.filterTables(e.val())}),t("#clearFilter").click(function(){e.val(""),i.click()}),0===n&&(t("#failedinput").attr("checked",!1),t("#passinput").attr("checked",!0))},filterTables:function(t,e,i){a.show(t),n.fnFilterAll(t,e,i)},openNewWindow:function(e){var i=window.open();e="<style>body {padding:0 0 0 15px;margin:0;font-family:'Courier New';font-size:12px;white-space: pre;overflow:auto;}</style>"+e,t(i.document.body).html(e)},addCodebasesBar:function(){var e=t(".top");""!==window.location.search&&i.codeBaseBranchOverview(e)}},r={init:function(){a=t(".table-holder"),s.dataTablesInit(),s.parseTimes(),s.setupFilterButtons(),s.addCodebasesBar();var e=t("#CheckBoxesList").find("input");e.click(function(){s.filterCheckboxes()}),s.filterCheckboxes(),setTimeout(s.addFailureButtons,100)}};return t(document).ready(function(){r.init()}),r});
//# sourceMappingURL=testresults-common.js.map