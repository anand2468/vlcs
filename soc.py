from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug=True
# socketio = SocketIO(app)
socketio = SocketIO(app, async_mode='threading', ping_timeout=60)

# render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# define a handler for the 'message' event
@socketio.on('message')
def somefun(message):
    print(message)
    emit('message', message, broadcast=True)
# @socketio.on()

@socketio.on('add')
def somefun(a,b):
    emit('message', int(a)+int(b), broadcast=True)

@socketio.on('sub')
def somefun(a,b):
    emit('message', int(a)-int(b), broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
