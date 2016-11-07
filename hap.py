from flask import Flask, render_template, request, session, url_for, redirect
from utils import dbaccess


app = Flask(__name__)

app.secret_key = '\x90\xfb\x0f6\x1dY\xa5i\x93+m\x83\xd8\xd9\xad\x91}\xef\x95]_\xe2i\xde\xcc\xb7\x03c\x83\xf3\xd1J'

@app.route("/")
@app.route("/login/")
def login():
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template('login.html', message="")

@app.route("/authenticate",methods=["POST"])
def authenticate():
    if request.method == "POST":
        u=request.form["username"]
        p=hashIt(request.form["pass"])
        button_val = request.form["value"]
        if button_val == "log":
            result = dbaccess.check_log(u, p)
            if result == "Bad Login":
                return render_template("login.html",message="Username or Password invalid. Try again.")
            else:
                session['username'] = request.form['username']
                return redirect(url_for('welcome'))
        elif button_val == "reg":
            result = dbaccess.check_reg(u, p)
            if result  == "Username taken":
                return render_template("login.html",message="Username taken. Be more original")
            elif result == "Invalid username":
                return render_template("login.html",message="Invalid username. Please change it.")
            else:
                dbaccess.add_account(u, p)
                return render_template("login.html",message="Success! Your account has been created.")
    else:
        return "You're in the wrong place"

@app.route("/welcome/")
def welcome():
    if 'username' in session:
        return render_template('home.html', name = session['username'])
    else:
        return "Not logged in. Error" #possible change this for redirect to login

@app.route("/logout/")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/settings")
def settings():
    if 'username' in session: #check if user can actually use settings
        return render_template('settings.html') #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login

@app.route("/add_story", methods=["POST"])
def add_story():
    if 'username' in session:
        text = request.form["storytext"]
        contributor = request.form["contributor"]
        title = request.form["title"]
        if dbaccess.add_story(title, body, contributor):
            #story already exists
            return render_template('story.html',message="Unable to create a story. Story title taken.")
        else:
            #story good to go
            return render_template('story.html',message="Success! Story created.")
    else:
        return "Not logged in. Error" #possible change this for redirect to login
        

@app.route('/add_contribution', methods=["POST"])
def add_contribution():
    if 'username' in session:
        #I want the form to give us story title, contributer, and text of contribution
        title = request.form["title"]
        contributor = request.form["contributor"]
        text = request.form["contribution"]
        if dbaccess.add_contribution(title, contributor, text):
            return render_template('story.html',message="Success! Contributed to story.")
        else:
            #this person has already contributed, not allowed to contribute to story
            return render_template('story.html',message="Unable to contribute. You have already contributed to this story!")
    else:
        return "Not logged in. Error" #possible change this for redirect to login
    
if __name__ == "__main__":
    app.debug = True
    app.run()
