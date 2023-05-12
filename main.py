from flask import Flask, render_template,url_for, request, session, redirect
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.debug= True
app.config['SECRET_KEY'] = 'secret-key-here'
socketio = SocketIO(app)

online_users=list()
userlist = dict()

#flask cals
@app.route('/')
def index():
    user = request.cookies.get('username')
    print('get cookies ', user)
    if user:
    #return render_template('in.html')
        return redirect('/home')
    else:
        return redirect('/log')



#chat
@app.route('/chat/t/<user>')
def chat(user):
    if user == None:
        return render_template('chat.html',users = online_users, stat = 'des')
    else:
        return render_template('chat.html',users = online_users)

@app.route('/chatbox/')
def chatbox():
    return render_template('chatbox.html')

        
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/log')
def log():
    images = os.listdir('static/logos/profiles')
    return render_template('login.html', images = images, os=os)
#end chat

# from chat gpt
#handle connect and disconnect
@socketio.on('connect')
def handle_connect():
    username = request.cookies.get('username')
    profile = request.cookies.get('profile')
    if username not in userlist:
        userlist[username]={
            'sid':request.sid,
            'profile': request.cookies.get('profile')
        }
    else:
        userlist[username]['sid'] = request.sid
    print(userlist)
    online_users.append(username)
    emit('append_user_list',{'username':username, 'link':'/chat/t/'+username, 'profile':profile}, broadcast=True)
    print(f'Client connected with SID: {request.sid}')
@socketio.on('disconnect')
def handle_disconnect():
    online_users.remove(request.cookies.get('username'))
    emit('remove_user_list',request.cookies.get('username'), broadcast=True)
    print(f'Client disconnected with SID: {request.sid}')


# send message
@socketio.on('send_message')
def send_message(message):
    print(message, 'message and recever')
    emit('app_message',{'message':message, 'sender':request.cookies.get('username')},broadcast=True)

#sends messages privates
@socketio.on('send_message_privately')
def send_message_privately(message):
    message['sender'] = request.cookies.get('username')
    recv = message['receiver'].strip()
    receiverid = userlist[recv]['sid']
    emit('send_message_to',message, to=receiverid)
    print('message and rec ',message,type(message),userlist[recv])
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