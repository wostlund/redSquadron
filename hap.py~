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

@app.route("/home", methods=["POST"])
def fred():
    return redirect(url_for("welcome"))
    
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

@app.route("/addStory1", methods = ["POST"])
def addstory1():
    if 'username' in session: #check if user can actually use settings
        return render_template('story.html',storyText = "") #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login
    

@app.route("/addstory", methods=["POST"])
def addstory():
    if 'username' in session:
        print request.form
        body = request.form["storypart"]
        contributor = session["username"]
        title = request.form["title"]
        dbaccess.add_story(title, body, contributor)
        return render_template('story.html',message="Success! Story created.",storyText = "" )
    else:
        return "Not logged in. Error" #possible change this for redirect to login
        
#@app.route('/addContribution', methods = ["POST"])
#def addcontribution():
#    if 'username' in session: #check if user can actually use settings
#        return render_template('list.html', info = dbaccess.show_unjoined(session["username"])) #add more arguments from Lorenz's db util files
#    else:
#        return "Not logged in. Error" #possible change this for redirect to login

@app.route('/addContributions', methods = ["POST"]) #in between -M
def incContributions():
    if 'username' in session: #check if user can actually use settings
        title = request.form["name"]
        print title
        return render_template('seenStory.html', storyText = dbaccess.last_contribution(title), Title=title, mine = dbaccess.mine(session['username'],title)) #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login


@app.route('/addContribution', methods=["POST"])
def add_contribution_redirect():
    if 'username' in session:
        #I want the form to give us story title, contributer, and text of contribution
        print request.form
        title = request.form["name"]
        contributor = session["username"]
        text = request.form["storypart"]
        if dbaccess.add_contribution(title, contributor, text):
            return redirect(url_for('welcome'))
        else:
            #this person has already contributed, not allowed to contribute to story
            return render_template('story.html',message="Unable to contribute. You have already contributed to this story!")
    else:
        return "Not logged in. Error" #possible change this for redirect to login

@app.route("/story", methods = ["POST"])
def display():
    if 'username' in session: #check if user can actually use settings
        story = request.form["name"]
        print request.form["name"]
        return render_template('seenStory.html',storyText =dbaccess.get_storytext(story), Title = story  ) #add more arguments from Lorenz's db util files
    else:
        return "Not logged in. Error" #possible change this for redirect to login

    
if __name__ == "__main__":
    app.debug = True
    app.run()


