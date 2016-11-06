from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)

app.secret_key = '\x90\xfb\x0f6\x1dY\xa5i\x93+m\x83\xd8\xd9\xad\x91}\xef\x95]_\xe2i\xde\xcc\xb7\x03c\x83\xf3\xd1J'

@app.route("/")
def login():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template('login.html', error = False)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/welcome/")
def welcome():
    if 'username' in session:
        return render_template('home.html', name = session['username'])
    else:
        return "Not logged in. Error?" #possible change this for redirect to login

@app.route("/logout/")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/settings")
def settings():
    if 'username' in session: #check if user can actually use settings
        return render_template('settings.html') #add more arguments from Lorenz's db util files

#@app.route("/contribute")
def add():
    if 'username' in session:
        return render_template('add.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
