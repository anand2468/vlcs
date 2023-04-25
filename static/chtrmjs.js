var socket = io();

        $('#submit').click(function(){
            var user= $("#user").val();
            socket.emit('updateuser',user );
        });

        // socket 
        socket.on('updateuser',function(data){
            console.log(data);
            $("main").append($('p').text(data));
        });

        socket.on('connect',function(){
            console.log('connected');
        });

        function join(){
            var sid = socket.io.engine.id;
            console.log(sid, seid);
            socket.emit('whoami',sid);
        }

        socket.on('disconnect',function(){
            console.log('disconnected');
        });