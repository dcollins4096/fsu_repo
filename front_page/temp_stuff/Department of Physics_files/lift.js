(function(){"function"!=typeof Object.assign&&(Object.assign=function(t,e){"use strict";if(null==t)throw new TypeError("Cannot convert undefined or null to object");for(var n=Object(t),i=1;i<arguments.length;i++){var r=arguments[i];if(null!=r)for(var o in r)Object.prototype.hasOwnProperty.call(r,o)&&(n[o]=r[o])}return n});var t=function(){function t(t,e){var n=[],i=!0,r=!1,o=void 0;try{for(var c,a=t[Symbol.iterator]();!(i=(c=a.next()).done)&&(n.push(c.value),!e||n.length!==e);i=!0);}catch(t){r=!0,o=t}finally{try{!i&&a.return&&a.return()}finally{if(r)throw o}}return n}return function(e,n){if(Array.isArray(e))return e;if(Symbol.iterator in Object(e))return t(e,n);throw new TypeError("Invalid attempt to destructure non-iterable instance")}}();window.AcquiaLift=window.AcquiaLift||{},window.AcquiaLift.internal=window.AcquiaLift.internal||{},window.AcquiaLiftPublicApi=window.AcquiaLiftPublicApi||{},window.AcquiaLift.liftAssetsURL=window.AcquiaLift.liftAssetsURL||"http://lift3assets.lift.acquia.com/stable",window.AcquiaLift.liftDecisionAPIURL=window.AcquiaLift.liftDecisionAPIURL||"https://us-east-1-decisionapi.lift.acquia.com",function(e,n){function i(t){var e=Object.assign({},t);return r(e,{propertyName:"profile"}),r(e,{propertyName:"identity",namePrefix:"identity:"}),e}function r(t,n){var i=n.propertyName,r=n.namePrefix,o=void 0===r?"":r;if(e.hasOwnProperty(i)){var c=e[i];Object.keys(c).forEach(function(e){t[""+o+e]=c[e]})}}function o(t){var e=new RegExp("(?:(?:^|.*;\\s*)"+t+"\\s*\\=\\s*([^;]*).*$)|^.*$");return document.cookie.replace(e,"$1")}function c(){var t=o("tc_ptid"),e=void 0;if(t){e=t;var n=o("tc_ptuid");n&&(e+=n)}return e}function a(t){t.identity_source="tracking";var e=c();e&&(t.identity=e);var n=parseInt(o("tc_ptidexpiry"));isNaN(n)||(t.identity_expiry=parseInt(n));var i=o("tc_ttid");i&&(t.touch_identifier=i)}function s(e){var n=Object.keys(e),i=n.filter(function(e){var n=e.split(":");return"identity"===t(n,1)[0].toLowerCase()});if(0!==i.length){var r={};return i.forEach(function(n){var i=n.split(":"),o=t(i,2),c=o[1];r[e[n]]=c,delete e[n]}),r}}function u(t){var e=void 0;if(t instanceof Date)e=t;else{var n=parseInt(t);if(isNaN(t))return;e=new Date(n)}if(e.toISOString)return e.toISOString()}function d(t){return function(e,n){t.hasOwnProperty(e)&&(t[e]=parseInt(t[e]),isNaN(t[e])&&(t[e]=n))}("engagement_score",g),t}function f(t){var e=new Date,n=s(t),i={event_name:"Content View",event_source:"Web",content_title:document.title,url:window.location.href,referral_url:document.referrer,user_agent:navigator.userAgent,client_timezone:String(e.getTimezoneOffset()),javascript_version:y,engagement_score:g};return n&&(i.identities=n),Object.keys(t).forEach(function(e){i[e]=t[e]}),d(i)}function l(t){return 0===t.indexOf("person_udf")||0===t.indexOf("touch_udf")||0===t.indexOf("event_udf")||-1!==L.indexOf(t)}function p(e){var n=[],i=o("tc_q");return i?(i=decodeURIComponent(i),i.split("|").forEach(function(i){var r=i.split("&"),o={};if(r.forEach(function(e){var n=e.split("="),i=t(n,2),r=i[0],c=i[1];r&&c&&r.length&&r.length>0&&(o[decodeURIComponent(r)]=decodeURIComponent(c))}),o.tcptid===e.identity&&o.tcttid===e.touch_identifier){var c={event_name:o.tcvc,event_source:"Web",event_date:u(o.tcect),url:o.tcvv,referral_url:o.tcvr,content_title:o.tcvt,user_agent:navigator.userAgent,platform:o.tcep,capture_identifier:o.tcctid,client_timezone:o.tcectz,javascript_version:o.tclv};o.site_id&&(c.site_id=o.site_id),Object.keys(o).forEach(function(t){0===t.indexOf("tci")?(c.identities||(c.identities={}),c.identities[t.substring("tci".length)]=o[t]):l(t)&&(c[t]=o[t])}),n.push(c)}}),n):n}function v(t,e){var n=e.slots,i=e.url,r={captures:[]};return a(r),p(r).forEach(function(t){r.captures.push(t)}),r.captures.push(f(t)),n&&(r.slots=n),i&&(r.url=i),r.hasOwnProperty("slots")||r.hasOwnProperty("url")||(r.url=window.location.href),r}function _(){return"true"!==o("tc_dnt")}function w(t){if(_()){var n=new m;n.onreadystatechange=function(){if(4===n.readyState&&200===n.status){var i=function(){e.lastDecisionRequest=t;var i=n.getResponseHeader("Content-Type");if(i&&i.indexOf("javascript")>-1)return A(n.responseText),{v:void 0};if(!e.internal||!e.internal.decisionCallback||"function"!=typeof e.internal.decisionCallback)return{v:void 0};if(!i||-1===i.indexOf("json"))return{v:void 0};var r=e.internal.decisionCallback,o=void 0,c=void 0,a=void 0,s=void 0;try{s=JSON.parse(n.responseText),o=s.decisions,c=s.slots,a=s.segments,window.AcquiaLift.currentSegments=a}catch(t){console.warn("Cannot parse decisions, slots or segments."),console.warn("Error: "+t)}return"loading"===document.readyState?(document.addEventListener("DOMContentLoaded",function(){return r(o,c,a)},!1),{v:void 0}):(r(o,c,a),{v:void 0})}();if("object"==typeof i)return i.v}},t.source=O;var i=e.internal&&e.internal.decisionCallback?"decide":"decide-js",r=e.liftDecisionAPIURL+"/"+i;r+=r.indexOf("?")>=0?"&":"?",r+="account_id="+e.account_id,r+="&site_id="+e.site_id,r+="&version="+y,n.open("post",r,!0),n.withCredentials=!0,n.setRequestHeader("Content-Type","text/plain"),n.send(JSON.stringify(t))}}var g=1,y="1.27.0",h=["account_id","site_id","contentOrigin","userAccess","liftDecisionAPIURL","liftAssetsURL","authEndpoint","contentReplacementMode"],m=XMLHttpRequest,A=eval,O=function(){for(var t=document.getElementsByTagName("script"),e=0;e<t.length;e++){var n=t[e].getAttribute("src");if(n&&n.match(/lift\.js$/gi))return n}return window.AcquiaLift.liftAssetsURL+"/lift.js"}();(function(){window._tcaq=window._tcaq||[]})();var b=function(){for(var t={},n=document.querySelectorAll("meta[itemprop]"),i=0;i<n.length;i++){var r=n[i];0===r.getAttribute("itemprop").indexOf("acquia_lift:")&&r.content&&0!==r.content.length&&(t[r.getAttribute("itemprop").substr("acquia_lift:".length)]=r.content)}return h.forEach(function(n){t.hasOwnProperty(n)&&(e[n]=t[n],delete t[n])}),t}();if(e.hasOwnProperty("account_id")&&e.hasOwnProperty("site_id")){e.internal.readCookie=o;var L=["persona","engagement_score","decision_slot_id","decision_slot_name","decision_rule_id","decision_rule_name","decision_rule_type","decision_rule_segment_id","decision_rule_segment_name","decision_content_id","decision_content_name","decision_goal_id","decision_goal_name","decision_goal_value","decision_view_mode","decision_policy","post_id","page_type","content_id","content_uuid","content_title","content_type","content_section","content_keywords","author","published_date"];n.personalize=function(){var t=arguments.length<=0||void 0===arguments[0]?{}:arguments[0];w(v(i(b),t))},n.customize=function(){e.internal.broadcastNow=!0},n.personalize()}}(window.AcquiaLift,window.AcquiaLiftPublicApi)})();
//# sourceMappingURL=lift-1.27.0.map