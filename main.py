from flask import Flask, render_template,url_for, request, session, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.debug= True
app.config['SECRET_KEY'] = 'secret-key-here'
socketio = SocketIO(app)

users=list()

#flask cals
@app.route('/')
def index():
    user = request.cookies.get('username')
    print('get cookies ', user)
    if user:
    #return render_template('in.html')
        return redirect('/chat')
    else:
        return redirect('/log')
@app.route('/chatrm')
def chatrm():
    return render_template('chtrm.html')
@app.route('/chatrarea')
def chatarea():
    return render_template('chatarea.html')

@app.route('/chat')
def chat():
    return render_template('chat.html',users = users, username = request.cookies.get('username'))

@app.route('/log')
def log():
    return render_template('login.html')

# from chat gpt
#handle connect and disconnect
@socketio.on('connect')
def handle_connect():
    users.append(request.cookies.get('username'))
    emit('append_user_list',request.cookies.get('username'), broadcast=True)
    print(f'Client connected with SID: {request.sid}')
@socketio.on('disconnect')
def handle_disconnect():
    users.remove(request.cookies.get('username'))
    emit('remove_user_list',request.cookies.get('username'), broadcast=True)
    print(f'Client disconnected with SID: {request.sid}')


# send message
@socketio.on('send_message')
def send_message(message):
    print(message, 'message and recever')
    emit('app_message',{'message':message, 'sender':request.cookies.get('username')},broadcast=True)

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