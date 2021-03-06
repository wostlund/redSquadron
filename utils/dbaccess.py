import sqlite3, time, hashlib

def check_reg(username, password):
    if not valid_username(username):
        return "Invalid username"
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from user where name='{p_name}'".format(p_name=username))
        result = cursor.fetchall()
        cursor.close()
        if len(result) > 0:
            return "Username taken"
        return "Success"

def valid_username(username):
    if not username or len(username) < 1 or username.isspace() or "'" in username:
        return False
    else:
        return True

def add_account(username, password):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (name, password) "
            "VALUES ('{p_user}', '{p_password}')".format(
                p_user=username, p_password=hashlib.sha224(password).hexdigest()))
     

def check_log(username, password):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name from user where name='{p_name}'".format(p_name=username))
        result = cursor.fetchall()
        cursor.close()
        if len(result) < 1:
            return "Bad Login"
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        user = curs.execute(
            "SELECT name,password from user where name = '{p_name}'".format(
                p_name=username))
        if not valid_username(username):
            return "Bad Login"
        if not user:
            return "Bad Login"
        for i in user: #should only return one
            if i[0] != username:
                return "Bad Login"
            if i[1] != hashlib.sha224(password).hexdigest():
                return "Bad Login"
        return "Good Login" #shouldn't be used though

#def add_account(username, password):
#    with sqlite3.connect('data.db') as conn:
#        curs = conn.cursor()
#    curs.execute(
#        "INSERT INTO user (name, password) "
#        "VALUES ('{p_user}', '{p_password}')".format(
#            p_user=username, p_password=hashlib.sha224(password).hexdigest()))

#def check_log(username, password):
#    with sqlite3.connect('data.db') as conn:
#        curs = conn.cursor()
#        user = curs.execute("SELECT name,password from user where name = '{p_name}' and password = '{p_password}'".format(p_name=username, p_password=hashlib.sha224(password).hexdigest()))
#        if not user:
#            return "Bad Login"
#        else:
#            return "Good Login" #shouldn't be used though

def show_unjoined(user): 
    id = "" #current user id
    with sqlite3.connect('data.db') as conn: 
        curs = conn.cursor()
        row = curs.execute("SELECT uid from user where name = '{p_name}'".format(p_name = user))
        for i in row:
            id = i[0]           
    with sqlite3.connect('data.db') as conn: 
        curs = conn.cursor() 
        info = {}         
        row = curs.execute("SELECT title, body, story.uid, contributors, name, sid from story, user where story.uid = user.uid")
        for i in row: 
            contributors = i[3].split(",")
            exist = False
            for q in contributors:
                if str(q) == str(id):
                    exist = True
            if not exist:
                info[i] = ["","","",""] 
                info[i][0] = i[0] #title
                info[i][1] = i[4] #name of uid 
                info[i][2] = i[1] #body
                info[i][3] = i[5]
        return info 
        
def show_joined(user): 
    id = "" #current user id
    with sqlite3.connect('data.db') as conn: 
        curs = conn.cursor()
        row = curs.execute("SELECT uid from user where name = '{p_name}'".format(p_name = user))
        for i in row:
            id = i[0]       
    with sqlite3.connect('data.db') as conn: 
        curs = conn.cursor() 
        info = {} 
        row = curs.execute("SELECT title, body, story.uid, contributors, name, sid from story, user where story.uid = user.uid")
        for i in row: 
            contributors = i[3].split(",")
            exist = False
            for q in contributors:
                if str(q) == str(id):
                    exist = True
            if exist:
                info[i] = ["","","",""] 
                info[i][0] = i[0] #title
                info[i][1] = i[4] #name of uid 
                info[i][2] = i[1] #body
                info[i][3] = i[5]
        return info 

def mine(user,title):
    id = "" #current user id
    title = quotechecker(title)
    with sqlite3.connect('data.db') as conn: 
        curs = conn.cursor()
        row = curs.execute("SELECT uid from user where name = '{p_name}'".format(p_name = user))
        for i in row:
            id = i[0]       
    with sqlite3.connect('data.db') as conn: 
        curs = conn.cursor() 
        row = curs.execute("SELECT title, story.uid, contributors from story,contribution where title = '{p_title}'".format(p_title = title))
        for i in row: 
            contributors = i[2].split(",")
            exist = False
            for q in contributors:
                if str(q) == str(id):
                    exist = True
            return exist
        return False

def add_story(title, body, contributor):
    # 1. Get the uid of the contributor
    title = quotechecker(title)
    body = quotechecker(body)
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row = curs.execute("SELECT uid from user where name='{p_name}'".format(p_name=contributor))
        story_creator = ""
        contributors = ""
        if row:
            for i in row:
                story_creator = i[0]
                contributors = story_creator
        # 2. Update story
        curs.execute(
            "INSERT INTO story (title, body, uid, contributors) "
            "VALUES ('{p_title}', '{p_body}', '{p_uid}', '{p_contributors}')".format(
                p_title=title, p_body=body, p_uid=story_creator, p_contributors=contributors))
        # 3. Get the last inserted row id
        sid = curs.lastrowid
        # 4. Update contribution
        curs.execute(
            "INSERT INTO contribution(sid, uid, story_update, date_added) "
            "VALUES ('{p_sid}', '{p_uid}', '{p_update}', '{p_date}')".format(
                p_sid=sid, p_uid=contributor, p_update=body, p_date=time.strftime("%c")))


def add_contribution(title, contributor, text):
    title = quotechecker(title)
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row = curs.execute("SELECT sid, contributors from story where title='{p_title}'".format(p_title=title))
        sid = ""
        contributors = []
        if row:
            for i in row:
                sid = i[0]
                contributors = i[1].split(",")
        row = curs.execute("SELECT uid from user where name='{p_username}'".format(p_username=contributor))
        uid = ""
        if row:
            for i in row:
                uid = i[0]
        if uid in contributors:
            #means this person has already contributed
            return False
        # insert to contribution table
        curs.execute(
            "INSERT INTO contribution(sid, uid, story_update, date_added) "
            "VALUES ('{p_sid}', '{p_uid}', '{p_update}', '{p_date}')".format(
                p_sid=sid, p_uid=uid, p_update=quotechecker(text), p_date=time.strftime("%c")))
        # update story table
        contributors.append(uid)
        new_contributors = ','.join([str(i) for i in contributors])
        curs.execute(
            "UPDATE story SET contributors='{p_contributors}' WHERE sid='{p_sid}'".format(
                p_contributors=new_contributors, p_sid=sid))
        #update story body
        story_body = curs.execute("SELECT body from story where title='{p_title}'".format(p_title=title))
        current = ""
        for stuff in story_body:
            current = stuff[0]
        new_body = current + " " + text
        curs.execute(
            "UPDATE story SET body='{p_body}' WHERE sid='{p_sid}'".format(
                p_body=quotechecker(new_body), p_sid=sid))        
        return True

def get_storytext(title):
    title = quotechecker(title)
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT body from story where title='{p_title}'".format(p_title=title))
        for i in row1:
            return i[0]

def get_storyauth(title):
    authid = ""
    title = quotechecker(title)
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT uid from story where title='{p_title}'".format(p_title=title))
        for i in row1:
            authid = i[0] #should only be one
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT name from user where user.id = '{p_uid}'".format(p_uid = authid))
        for i in row1:
            return i[0]

def usernametoid(name):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT uid from user where name='{p_name}'".format(p_name=name))
        for i in row1:
            return i[0]

def nametoid(name):
    name = quotechecker(name)
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT sid from story where title='{p_title}'".format(p_title=name))
        for i in row1:
            return i[0]

def idtoname(id):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT title from story where sid='{psid}'".format(psid=id))
        for i in row1:
            return i[0]


def last_contribution(title):
    title = quotechecker(title)
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT sid from story where title='{p_title}'".format(p_title=title))
        sid = ""
        for i in row1:
            sid = i[0]
        print sid
        last = ""
        row2 = curs.execute("SELECT story_update from contribution where cid=(SELECT max(cid) from contribution where sid='{p_sid}')".format(p_sid=sid))
        for q in row2:
            print q
            last = q[0]
        print last
        return last

def quotechecker(string):
    return string.replace("'","''")




