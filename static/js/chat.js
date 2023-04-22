// socket = io();
const socket = io.connect('http://127.0.0.1:5000');

//connect and disconnect handlers
socket.on('connect', () => {
    console.log(`Connected with SID: ${socket.id}`);
});

socket.on('disconnect', () => {
    console.log(`Disconnected from server with SID: ${socket.id}`);
});


//appends about new user details
socket.on('append_user_list',function(data){
    console.log(`append user list ${data}`);
    // $('p:contains("hello")').remove()
    $('#user_list').append($('<p>').text(data));
});
socket.on('remove_user_list',function(data){
    console.log(data);
    $(`p:contains("${data}")`).remove();
});


//send the message to the server
var nn = $('#message_view');
$('#send_message').click(function(){
    var message = $("#message").val();
    var sid = socket.io.engine.id;
    console.log(sid);
    socket.emit('send_message', sid, message);
    $('#message').val('');
});

// write the message in the page
socket.on('app_message',function(data) {
    console.log(data);
    $('#message_view').append($('<p>').text(data));
});






//code to woek with enter
var input = document.getElementById("message");
input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send_message").click();
    }
});




// var sid = socket.io.engine.id;
// socket.on('connect',function(){
//     var sid = socket.io.engine.id;
//     console.log('connected');
//     console.log(sid);
//     socket.emit(sid);
// });