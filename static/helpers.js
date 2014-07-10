$(document).ready(function() {


    /*Start jquery configuration*/
    $.ajaxSetup({
        data: {
            _xsrf: getCookie('_xsrf')
        }
    });


});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    if (!r && name.localeCompare("_xsrf")==0){
        return 'cookie_not_found'
    }
    return r ? r[1] : undefined;
}

function decimalToHex(d, padding) {
	var hex = Number(d).toString(16);
	padding = typeof (padding) === "undefined" || padding === null ? padding = 2 : padding;

	while (hex.length < padding) {
		hex = "0" + hex;
	}

	return hex;
}