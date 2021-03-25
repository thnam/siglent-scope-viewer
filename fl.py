from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def scope_viewer(ip='192.168.1.119'):
    return render_template('index.html', ip=ip)
