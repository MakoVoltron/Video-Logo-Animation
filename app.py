from flask import Flask, render_template, url_for, session
import os
# import config


app = Flask(__name__)
app.secret_key = os.urandom(24)



@app.route("/home")
@app.route("/")
def index():
    session['user'] = 'Mate'
    return render_template('home.html')


@app.route("/checkout")
def checkout():
    if 'user' in session:
        return session['user']
    
    return 'You must be logged in to checkout.'


if __name__ == '__main__':
    app.run(debug=True)
