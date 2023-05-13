var socket;
var recever = window.location['href'].split('/')[5];
var username = getCookie("username");
if (checkCookie("username")){
    socket = io.connect('http://127.0.0.1:5000');
}
else{
    window.location.replace("/log");
}
$('h1.recever_username').text(recever);

//connect and disconnect handlers
socket.on('connect', () => {
    console.log(`Connected with SID: ${socket.id}`);
});
socket.on('disconnect', () => {
    console.log(`Disconnected from server with SID: ${socket.id}`);
});


$('#send_message').click(function(){
    var message = $('#message').val();
    var img = $('<img>',{ height:40, src:'/static/logos/profiles/23.png'});
    socket.emit('send_message_privately',{'message':message, 'receiver':recever});
    $('#message').val('');
    $('#message_view').append($('<section>',{ class:'sended_text'}).append(img,$('<h3>').text(username), $('<p>').text(message)));
})

// write the message in the page
socket.on('app_message',function(data) {
    console.log(data);
    $('#message_view').append($('<p>').text(`${data.sender}: ${data['message']}`));
});

socket.on('send_message_to', function(data){
    var img = $('<img>',{ height:40, src:'/static/logos/profiles/23.png'});
    $('#message_view').append($('<section>',{ class:'receieved_text'}).append( img, $('<h3>').text(data.sender)  ,$('<p>').text(data['message'])));
});






//code to work with enter
var input = document.getElementById("message");
input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send_message").click();
    }
});