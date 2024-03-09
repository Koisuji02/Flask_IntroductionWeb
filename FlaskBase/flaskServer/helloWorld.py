from flask import Flask

app = Flask(__name__)

@app.route('/')             # Quando il server riceve una get (percorso = '/')
def hello_world():          # risponde con la funzione hello_world
    return 'Hello, world!'