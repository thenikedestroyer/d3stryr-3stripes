javascript:(function(){
var f = document.createElement("form");
f.setAttribute('id',"destroyer");
f.setAttribute('method',"post");
f.setAttribute('action',"{{ atc_url }}");

var masterPid = document.createElement("input");
masterPid.setAttribute('type',"hidden");
masterPid.setAttribute('name',"masterPid");
masterPid.setAttribute('value',"{{ master_pid }}");

var pid = document.createElement("input");
pid.setAttribute('type',"hidden");
pid.setAttribute('name',"pid");
pid.setAttribute('value',"{{ pid }}");

var ajaxOption = document.createElement("input");
ajaxOption.setAttribute('type',"hidden");
ajaxOption.setAttribute('name',"ajax");
ajaxOption.setAttribute('value',"true");

var responseOption = document.createElement("input");
responseOption.setAttribute('type',"hidden");
responseOption.setAttribute('name',"responseformat");
responseOption.setAttribute('value',"json");

var sessionSelectedStoreID = document.createElement("input");
sessionSelectedStoreID.setAttribute('type',"hidden");
sessionSelectedStoreID.setAttribute('name',"sessionSelectedStoreID");
sessionSelectedStoreID.setAttribute('value',"null");

var captchaToken = document.createElement("input");
captchaToken.setAttribute('type',"hidden");
captchaToken.setAttribute('name',"g-recaptcha-response");
captchaToken.setAttribute('value',"{{ captcha_token }}");

var captchaDuplicate = document.createElement("input");
captchaDuplicate.setAttribute('type',"hidden");
captchaDuplicate.setAttribute('name',"{{ captcha_duplicate }}");
captchaDuplicate.setAttribute('value',"{{ captcha_token }}");

var s = document.createElement("input");
s.setAttribute('type',"submit");
s.setAttribute('value',"Submit");

f.appendChild(masterPid);
f.appendChild(pid);
f.appendChild(ajaxOption);
f.appendChild(responseOption);
f.appendChild(sessionSelectedStoreID);
f.appendChild(captchaToken);
f.appendChild(captchaDuplicate);
f.appendChild(s);

document.getElementsByTagName('body')[0].appendChild(f);

})();

document.getElementById(document.querySelector("[id^='destroyer']").id).submit();

