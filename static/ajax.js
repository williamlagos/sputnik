<script>
/*function post_url(path, params, method) {
    method = method || "post"; // Set method to post by default, if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

post_url("https://accounts.google.com/o/oauth2/token",{"code":code,"client_id":client_id,"client_secret":client_secret,"redirect_uri":redirect_uri,"grant_type":grant_type}); 

var code = "{{ form["code"].value() }}";
var client_id = "{{ form["client_id"].value() }}";
var client_secret = "{{ form["client_secret"].value() }}";
var redirect_uri = "{{ form["redirect_uri"].value() }}";
var grant_type = "{{ form["grant_type"].value() }}";

$(function(){
	var a = $.ajax({
		type: "POST",
		url: "https://accounts.google.com/o/oauth2/token",
		data: { code: code, 
			client_id: client_id, 
			client_secret: client_secret, 
			redirect_uri: redirect_uri, 
			grant_type: grant_type },
		dataType: "text",
	});   
	$("#message_ajax").html(a);
	$("#message_ajax").html("ABC");
});*/
</script>
