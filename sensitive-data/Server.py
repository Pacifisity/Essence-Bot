from flask import Flask
from threading import Thread
app = Flask('')

@app.route('/')
def main():
    return

def run():
    app.run(host = "0.0.0.0", port = 6969)
    
def Server():
    server = Thread(target=run)
    server.start
    print("Server Running")