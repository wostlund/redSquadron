from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

app = Flask(__name__)

app.secret_key = '\x90\xfb\x0f6\x1dY\xa5i\x93+m\x83\xd8\xd9\xad\x91}\xef\x95]_\xe2i\xde\xcc\xb7\x03c\x83\xf3\xd1J'

dbaccess.create_db()
db = sqlite3.connect(data/data.db)

@app.route("/")
@app.route("/login/")
def login():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template('login.html', error = False)

@app.route("/authenticate",methods=["POST"])
def registration():
    if request.method=="POST":
        u=request.form["username"]
        p=hashIt(request.form["pass"])
        button_val = request.form["val"]
        if button_val == "log":
            login()
        elif button_val == "reg"
            result = check_reg(u, p)
            if result  == "Username taken":
                return render_template("login.html",message="Username taken. Be more original")
            elif result == "Invalid username":
                return render_template("login.html",message="Invalid username. Please change it.")
            else:
                add_account(u, p)
                return render_template("login.html",message="Success! Your account has been created.")

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

@app.route("/add_story", methods=["POST"])
def add_story:
    text = request.form["storytext"]
    contributor = request.form["contributor"]
    title = request.form["title"]
    dbaccess.add_story(text, contributor, title)

if __name__ == "__main__":
    app.debug = True
    app.run()
