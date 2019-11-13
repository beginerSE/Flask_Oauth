from flask import Flask, send_from_directory, session
import os
app = Flask(__name__)


@app.route('/')
def index():
    return "<html><h1>FlaskでSNSログインを実装する</h1><a href='/export'>twitterでログインする</a></html>"

@app.route("/oauth_login")
def login():
     return jsonify()
 


