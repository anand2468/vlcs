from flask import Flask, render_template,url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatrm')
def chatrm():
    return render_template('chtrm.html')

@app.route('/chatrarea')
def chatarea():
    return render_template('chatarea.html')


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=80)