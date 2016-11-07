import sqlite3, time, hashlib

<<<<<<< HEAD
#db = sqlite3.connect("data/data.db")
=======
>>>>>>> eb8e4736e9a9762ba1fbf4031b10d06c6f08c51c

def check_reg(username, password):
    db = sqlite3.connect("data/data.db")
    if not valid_username(username):
        return "Invalid username"
<<<<<<< HEAD
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from user where name='{p_name}'".format(p_name=username))
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
            return "Username taken"
        return "Success"
=======
    curs = db.cursor()
    q = "SELECT name from user where name={p_name}".format(p_name=username)
    rows = curs.execute(q)
    if rows:
        return "Username taken"
    return "Success"
>>>>>>> eb8e4736e9a9762ba1fbf4031b10d06c6f08c51c

def valid_username(username):
    if username.isspace() or username.len() < 1:
        return False
<<<<<<< HEAD
    else:
        return True

def add_account(username, password):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        curs.execute(
            "INSERT INTO user (name, password) "
            "VALUES ('{p_user}', '{p_password}')".format(
                p_user=username, p_password=hashlib.sha224(password).hexdigest()))
     

def check_log(username, password):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        user = curs.execute(
            "SELECT name,password from user where name = '{p_name}' and password = '{p_password}'".format(
                p_name=username, p_password=hashlib.sha224(password).hexdigest()))
        if not user:
            return "Bad Login"
        else:
            return "Good Login" #shouldn't be used though
=======
    return True

def add_account(username, password):
    db = sqlite3.connect("data/data.db")
    curs = db.cursor()
    curs.execute(
        "INSERT INTO users (name, password) "
        "VALUES ({p_user}, {p_password})".format(
            p_user=username, p_password=hashlib.sha224(password).hexdigest()))
    db.commit()

def check_log(username, password):
    db = sqlite3.connect("data/data.db")
    curs = db.cursor()
    user = curs.execute("SELECT name,password from user where name = {p_name} and password = {p_password}".format(p_name=username, p_password=hashlib.sha224(password).hexdigest()))
    if not user:
        return "Bad Login"
    else:
        return "Good Login" #shouldn't be used though

def show_unjoined(user):
    db = sqlite3.connect("data/data.db")
    info[0][0]=""
    curs = db.cursor()
    row = curs.execute("SELECT title, body, uid from user where contributor!={p_name}".form(p_name=user))
    for i in row:
        info[i][0] = i["title"]
        info[i][1] = i["uid"]
        info[i][2] = i["body"]
    return info

def show_joined(user):
    db = sqlite3.connect("data/data.db")
    info[0][0]=""
    curs = db.cursor()
    row = curs.execute("SELECT title, body, uid from user where contributor={p_name}".form(p_name=user))
    for i in row:
        info[i][0] = i["title"]
        info[i][1] = i["uid"]
        info[i][2] = i["body"]
    return info
>>>>>>> eb8e4736e9a9762ba1fbf4031b10d06c6f08c51c
    

def add_story(title, body, contributor):
    db = sqlite3.connect("data/data.db")
    # 1. Get the uid of the contributor
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row = curs.execute("SELECT uid from user where name={p_name}".format(p_name=contributor))
        story_creator = ""
        contributors = ""
        if row:
            story_creator = row[0]["uid"]
            contributors = story_creator
        # 2. Check if story exists.  Story exists if title exists
        row = curs.execute("SELECT sid from story where title={p_title}".format(p_title=title))
        if row:
            return False
        else:
            curs.execute(
                "INSERT INTO story (title, body, uid, contributors) "
                "VALUES ({p_title}, {p_body}, {p_uid}, {p_contributors})".format(
                    p_title=title, p_body=body, p_uid=story_creator, p_contributors=contributors))
            return True

def add_contribution(title, contributor, text):
<<<<<<< HEAD
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row = curs.execute("SELECT sid, contributors from story where title={p_title}".format(p_title=title))
        sid = ""
        contributors = []
        if row:
            sid = row[0]["sid"]
            contributors = row[0]["contributors"].split(",")
        row = curs.execute("SELECT uid from user where username={p_username}".format(p_username))
        uid = ""
        if row:
            uid = row[0]["uid"]
        if uid in contributors:
            #means this person has already contributed
            return False
        # insert to contribution table
        curs.execute(
            "INSERT INTO contribution(sid, uid, story_update, date_added) "
            "VALUES ({p_sid}, {p_uid}, {p_update}, {p_date})".format(
                p_sid=sid, p_uid=uid, p_update=story_update, p_date=time.strftime("%c")))
        # update story table
        new_contributors = ','.join(contributors.append(uid))
        curs.execute(
            "UPDATE story SET contributors={p_contributors} WHERE sid={p_sid}".format(
                p_contributors=new_contributors, p_sid=sid))
        return True
=======
    db = sqlite3.connect("data/data.db")
    curs = db.cursor()
    row = curs.execute("SELECT sid, contributors from story where title={p_title}".format(p_title=title))
    sid = ""
    contributors = []
    if row:
        sid = row[0]["sid"]
        contributors = row[0]["contributors"].split(",")
    row = curs.execute("SELECT uid from user where username={p_username}".format(p_username))
    uid = ""
    if row:
        uid = row[0]["uid"]
    if uid in contributors:
        #means this person has already contributed
        return False
    # insert to contribution table
    curs.execute(
        "INSERT INTO contribution(sid, uid, story_update, date_added) "
        "VALUES ({p_sid}, {p_uid}, {p_update}, {p_date})".format(
            p_sid=sid, p_uid=uid, p_update=story_update, p_date=time.strftime("%c")))
    # update story table
    new_contributors = ','.join(contributors.append(uid))
    curs.execute(
        "UPDATE story SET contributors={p_contributors} WHERE sid={p_sid}".format(
            p_contributors=new_contributors, p_sid=sid))
    return True
>>>>>>> eb8e4736e9a9762ba1fbf4031b10d06c6f08c51c




