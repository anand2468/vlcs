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
    console.log(`append user list ${data['username']}`);
    $('#user_list').append($('<a>',{
        href: data.link
    }).text(data.username));
});
socket.on('remove_user_list',function(data){
    console.log(data);
    $(`a:contains("${data}")`).remove();
});


//send the message to the server
// $('#send_message').click(function(){
//     var message = $("#message").val();
//     socket.emit('send_message', message);
//     $('#message').val('');
// });

$('#send_message').click(function(){
    var message = $('#message').val();
    socket.emit('send_message_privately',{'message':message, 'receiver':$('#receivernm').text()});
    $('#message').val('');
})

// write the message in the page
socket.on('app_message',function(data) {
    console.log(data);
    $('#message_view').append($('<p>').text(`${data.sender}: ${data['message']}`));
});

socket.on('send_message_to', function(data){
    $('#message_view').append($('<p>').text(`${data.sender}: ${data['message']}`));
});






//code to work with enter
var input = document.getElementById("message");
input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send_message").click();
    }
});
