from flask import Flask, render_template,url_for, request, session, redirect, jsonify
from flask_socketio import SocketIO, emit
import os
from dbcommands import *
from t2d import t2d, d2t

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
    
@app.route('/userdetails',methods = ['POST'])
def userdetails():
    response = userDetails(request.form['uid'])
    print('response is ', response)
    return jsonify(response)

@app.route('/chatbox/')
def chatbox():
    alluser = allusers()
    print('all user are ',alluser )
    return render_template('chatbox.html', users = alluser)

#to get previous messages
@app.route('/oldmessages', methods= ['POST'])
def oldmessages():
    res = get_messages(request.form['convoid'])
    print(res)
    return jsonify(res)
        
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/log')
def log():
    images = os.listdir('static/logos/profiles')
    return render_template('login.html', images = images, os=os)
#end chat

#ajax calls
@app.route('/createusr', methods=['POST'])
def your_function():
    print('request is ', request.form)
    username = request.form['username']
    profileid = request.form['profile']
    print(profileid, username)

    response = {}
    if len(findUser(username)) == 0:
        lastuser = findlast()
        decimal = t2d(lastuser) +1
        userid = d2t(decimal)
        create_user(userid, username, profileid)
        response['userid'] = userid
        response['message']='success'
    else:
        response['message']='failed'
    # do something with key
    print()
    return jsonify(response)

# from chat gpt
#handle connect and disconnect
@socketio.on('connect')
def handle_connect():
    username = request.cookies.get('userid')
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
    # online_users.remove(request.cookies.get('username'))
    # emit('remove_user_list',request.cookies.get('username'), broadcast=True)
    print(f'Client disconnected with SID: {request.sid}')


# send message
@socketio.on('send_message')
def send_message(message):
    print(message, 'message and recever')
    emit('app_message',{'message':message, 'sender':request.cookies.get('username')},broadcast=True)

#sends messages privates
@socketio.on('send_message_privately')
def send_message_privately(message):
    recv = message['receiver'].strip()
    try:
        receiverid = userlist[recv]['sid']
    except:
        receiverid= 'qqwert'
    convoid = message['sender']+ message['receiver'] if message['sender'] < message['receiver'] else message['receiver'] + message['sender']
    send_message_db(convoid, message['sender'],recv, message['message'])

    emit('send_message_to',message, to=receiverid)


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
