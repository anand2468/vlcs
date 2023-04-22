from flask import Flask, render_template,url_for, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.debug= True
socketio = SocketIO(app)

users=list()

#flask cals
@app.route('/')
def index():
    return render_template('in.html')

@app.route('/chatrm')
def chatrm():
    return render_template('chtrm.html')

@app.route('/chatrarea')
def chatarea():
    return render_template('chatarea.html')

@app.route('/chat')
def chat():
    return render_template('chat.html', users = users)

# from chat gpt
#handle connect and disconnect
@socketio.on('connect')
def handle_connect():
    emit('append_user_list',request.sid, broadcast=True)
    print(f'Client connected with SID: {request.sid}')
@socketio.on('disconnect')
def handle_disconnect():
    emit('remove_user_list',request.sid, droadcast=True)
    print(f'Client disconnected with SID: {request.sid}')


# send message
@socketio.on('send_message')
def send_message(sid, message):
    print(sid, message)
    emit('app_message',message)

if __name__=='__main__':
    socketio.run(app)










# @socketio.event
# def connect(sid):
#     print(f'sid {sid} is connected')

# @socketio.event
# def disconnect(sid):
#     print(f'sid is disconnected ')


#chat gpt
# @socketio.on('message')
# def handle_message(message):
#     print(f'Received message "{message}" from client with SID: {request.sid}')
#     emit('message', f'Received message "{message}" from client with SID: {request.sid}')