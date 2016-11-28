var url='{{ injection_url }}';
document.getElementById(document.querySelector("[id^='dwfrm_cart']").id).action = url;
document.getElementById(document.querySelector("[id^='dwfrm_cart']").id).submit();
