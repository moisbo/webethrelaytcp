$(document).ready(function() {



});

function sendMessage(msg, cb){
    var message = {
        m1: msg.m1,
		m2: msg.m2,
		m3: msg.m3
    };

    $.when(
        $.ajax({
            url: "/sendMessage?_xsrf=" + getCookie('_xsrf'),
            type: "POST",
            data: message,
            dataType: "json"
        })
    ).done(function(response) {
			if(response.error || (response.data != '00')) {
				if(response.data == '01'){
					$('#errorMessage').html("Error! sending", message.m1);
				}else {
					$('#errorMessage').html(response.data);
				}
				$("#popupCloseLeft").popup("open");
			}else{
				cb(true)
			}
    });
}

function testButton(m1,m2,m3){
    sendMessage( { m1: m1,
		m2: m2,
		m3: m3}, function(){
		console.log('success');
	});
}
var i=0;
var inter;
function send(){
	i++;
	if(i>=20){clearInterval(inter)}
	console.log(decimalToHex(i))
	sendMessage( { m1: '20',
		m2: decimalToHex(i),
		m3: '05'}, function(next){
		if(!next){
		}
	});
}
function testCycle(){
	i=0;
	inter = setInterval(send, 500)
}
