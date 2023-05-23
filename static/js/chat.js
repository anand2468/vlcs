var socket;
var recever = window.location['href'].split('/')[5];
const username = getCookie("username");
const profileid = getCookie("profile");
const uid = getCookie("userid")

console.log('chat loaded');
if (checkCookie("username")){
    socket = io.connect('http://127.0.0.1:5000');
}
else{
    window.location.replace("/log");
}

//to find user details
$.ajax({
    url: "/userdetails",
    type: "POST",
    dataType: "json",
    data: {'uid':recever},
    success: function(response) {
        console.log(response);
        $('h1.recever_username').text(response[1]);
        rpic = response[2];
        rname = response[1];
        console.log('out');
    },
    error: function(xhr, status, error) {
        console.log(error);
    }
});

if (recever > uid){
    cid = uid + recever;
}
else{
    cid = recever + uid ;
}
// retreve previos msgs
$.ajax({
    url:"/oldmessages",
    type: "POST",
    dataType: "json",
    data:{'convoid': cid},
    success: function(response){
        console.log(response);
        // appends old messages
        for (i of response) {
            if (uid == i[1]) {
                var img = $('<img>', { height: 40, src: '/static/logos/profiles/' + profileid + '.png' });
                $('#message_view').append($('<section>', { class: 'sended_text' }).append(img, $('<h3>').text(username), $('<p>').text(i[3])));
            }
            else {
                var img = $('<img>', { height: 40, src: `/static/logos/profiles/${rpic}.png` });
                $('#message_view').append($('<section>', { class: 'receieved_text' }).append(img, $('<h3>').text(rname), $('<p>').text(i[3])));
            }
        }
        scrol();
    },
    error: function(xhr, status, error){
        console.log(error);
    }
});


//connect and disconnect handlers
socket.on('connect', () => {
    console.log(`Connected with SID: ${socket.id}`);
});
socket.on('disconnect', () => {
    console.log(`Disconnected from server with SID: ${socket.id}`);
});


$('#send_message').click(function(){
    var message = $('#message').val();
    var img = $('<img>',{ height:40, src:'/static/logos/profiles/'+profileid+ '.png'});
    socket.emit('send_message_privately',{'message':message, 'receiver':recever, 'sender':uid});
    $('#message').val('');
    $('#message_view').append($('<section>',{ class:'sended_text'}).append(img,$('<h3>').text(username), $('<p>').text(message)));
    scrol();
})

// write the message in the page
socket.on('app_message',function(data) {
    console.log(data);
    $('#message_view').append($('<p>').text(`${data.sender}: ${data['message']}`));
});

socket.on('send_message_to', function(data){
    var img = $('<img>',{ height:40, src: `/static/logos/profiles/${rpic}.png` });
    console.log(data);
    if (data.sender == recever){
        $('#message_view').append($('<section>',{ class:'receieved_text'}).append( img, $('<h3>').text(rname)  ,$('<p>').text(data['message'])));
        scrol();
    }
    else{
        console.log(data);
    }
});






//code to work with enter
var input = document.getElementById("message");
input.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send_message").click();
    }
});

//to scroll top
function scrol() {
    $("#message_view").scrollTop($("#message_view").height()+60);
}