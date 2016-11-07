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
        print request.form
        u=request.form["user"]
        p=request.form["password"]
        button_val = request.form["submit"]
        print button_val
        if button_val == "log":
            result = dbaccess.check_log(u, p)
            if result == "Bad Login":
                return render_template("login.html",message="Username or Password invalid. Try again.")
            else:
                session['username'] = request.form['user']
                return redirect(url_for('welcome'))
        elif button_val == "reg":
            print ('before check reg')
            result = dbaccess.check_reg(u, p)
            print ('after check reg')
            if result  == "Username taken":
                return render_template("login.html",message="Username taken. Be more original")
            elif result == "Invalid username":
                return render_template("login.html",message="Invalid username. Please change it.")
            else:
                print ('before add account')
                dbaccess.add_account(u, p)
                return render_template("login.html",message="Success! Your account has been created.")
    else:
        return "You're in the wrong place"

@app.route("/welcome/")
def welcome():
    if 'username' in session:
        name = session['username']
        return render_template('home.html', info1 = dbaccess.show_unjoined(name), info2 = dbaccess.show_joined(name))
    else:
        return "Not logged in. Error" #possible change this for redirect to login

@app.route("/logout", methods = ["POST"])
def logout():
    if 'username' in session:
        session.pop('username', None)
    else:
        return "ERROR.  You're in the wrong place"
    return redirect(url_for('login'))

@app.route("/settings")
def settings():
    if 'username' in session: #check if user can actually use settings
        return render_template('settings.html') #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login

@app.route("/addStory", methods = ["POST"])
def addstory():
    if 'username' in session: #check if user can actually use settings
        return render_template('story.html',storyText = "") #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login
    

@app.route("/add_story", methods=["POST"])
def add_story():
    if 'username' in session:
        text = request.form["storypart"]
        contributor = session["username"]
        title = "jeff"
        if dbaccess.add_story(title, text, contributor):
            #story already exists
            return render_template('story.html', message="Unable to create a story. Story title taken.",storyText = "")
        else:
            #story good to go
            return render_template('story.html',message="Success! Story created.",storyText = "" )
    else:
        return "Not logged in. Error" #possible change this for redirect to login
        
@app.route('/addContribution', methods = ["POST"])
def addcontribution():
    if 'username' in session: #check if user can actually use settings
        return render_template('list.html', info = dbaccess.show_unjoined(session["username"])) #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login

@app.route('/addContributionM', methods = ["POST"]) #in between -M
def addcontributionM():
    if 'username' in session: #check if user can actually use settings
        title = request.form["title"]
        return render_template('story.html', storyText = last_contribution(title)) #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login

     

@app.route('/add_contribution', methods=["POST"])
def add_contribution():
    if 'username' in session:
        #I want the form to give us story title, contributer, and text of contribution
        title = request.form["title"]
        contributor = session["username"]
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
