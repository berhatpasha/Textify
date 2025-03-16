import threading

def server():
    from flask import Flask, render_template

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/info')
    def info():
        return render_template('info.html')

    @app.route('/try')
    def try_page():
        return render_template('try.html')

    if __name__ == '__main__':
        app.run(debug=True)

serverThread = threading.Thread(target=server)
serverThread.start()

def main():
    print("Hello World!")

mainThread = threading.Thread(target=main)
mainThread.start()
