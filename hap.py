from flask import Flask, render_template, request, session, url_for, redirect
from utils import dbaccess


app = Flask(__name__)

app.secret_key = '\x90\xfb\x0f6\x1dY\xa5i\x93+m\x83\xd8\xd9\xad\x91}\xef\x95]_\xe2i\xde\xcc\xb7\x03c\x83\xf3\xd1J'

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
            result = dbaccess.check_log(u, p)
            if result == "Username invalid":
                return render_template("login.html",message="Username invalid. Try again.")
            elif result == "Password invalid":
                return render_template("login.html",message="Password invalid. Try again.")
            else:
                session['username'] = request.form['username']
                return redirect(url_for('welcome'))
        elif button_val == "reg"
            result = dbaccess.check_reg(u, p)
            if result  == "Username taken":
                return render_template("login.html",message="Username taken. Be more original")
            elif result == "Invalid username":
                return render_template("login.html",message="Invalid username. Please change it.")
            else:
                dbaccess.add_account(u, p)
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
    if dbaccess.add_story(text, contributor, title):
        #do something when story is successfully added
    else:
        #do something if story does not exist

@app.route('/add_contribution', methods=["POST"])
def add_contribution:
    #I want the form to give us story title, contributer, and text of contribution
    title = request.form["title"]
    contributor = request.form["contributor"]
    text = request.form["contribution"]
    if not dbaccess.add_contribution(title, contributor, text):
        #this person has already contributed, not allowed to contribute to story

#latest contribution

if __name__ == "__main__":
    app.debug = True
    app.run()
