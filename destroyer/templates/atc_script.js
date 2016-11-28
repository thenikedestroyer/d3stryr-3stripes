$.ajax({
  url: '{{ atc_url }}',
  data: {{ data }},
  method: 'POST',
  crossDomain: true,
  contentType: 'application/x-www-form-urlencoded',
  xhrFields: {
      withCredentials: true
  },
  complete: function(data, status, xhr) {
    console.log(status);
    console.log(data);
  }
});
