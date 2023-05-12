var socket;
if (checkCookie("username")){
    socket = io.connect('http://127.0.0.1:5000');
}
else{
    window.location.replace("/log");
}

//connect and disconnect handlers
socket.on('connect', () => {
    console.log(`Connected with SID: ${socket.id}`);
});
socket.on('disconnect', () => {
    console.log(`Disconnected from server with SID: ${socket.id}`);
});


//appends and remove new user details
socket.on('append_user_list',function(data){
    var img = $('<img>', { src:`/static/logos/profiles/${data.profile}.png`});
    var h1 = $('<h1>').text(data.username);
    $('#user_list').append($('<article>').append($('<a>',{ href:data.link}).append(img,h1)));
    console.log(`append user list ${data['username']}`);
});
socket.on('remove_user_list',function(data){
    console.log(data);
});

// notifies the message
socket.on('send_message_to', function(data){
    $('#user_list article a').append($('<p>',{style:'margin-left:10px; border:1px solid red;'}).text(data['message']));
})



$('#send_message').click(function(){
    var message = $('#message').val();
    socket.emit('send_message_privately',{'message':message, 'receiver':$('#receivernm').text()});
    $('#message').val('');
})







//code to work with enter
var input = document.getElementById("message");
input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send_message").click();
    }
});
