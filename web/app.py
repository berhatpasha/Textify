import threading
import flask
from flask import Flask, render_template


def main(): #! buraya model ile alakalı kodlar gelecek, burası web sitesinin arkaplanı olacak
    print("Hello World")

mainThread = threading.Thread(target=main) 
mainThread.start()


#* flask app 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/try')
def try_page():
    return render_template('try.html')

@app.route('/info')
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)
