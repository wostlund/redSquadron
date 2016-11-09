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
    if not username or len(username) < 1 or username.isspace():
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
        if not username or len(username) < 1 or username.isspace():
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
        row = curs.execute("SELECT title, body, story.uid, contributors, name from story, user where story.uid = user.uid")
        for i in row: 
            contributors = i[3].split(",")
            exist = False
            for q in contributors:
                if str(q) == str(id):
                    exist = True
            if not exist:
                info[i] = ["","",""] 
                info[i][0] = i[0] #title
                info[i][1] = i[4] #name of uid 
                info[i][2] = i[1] #body
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
        row = curs.execute("SELECT title, body, story.uid, contributors, name from story, user where story.uid = user.uid")
        for i in row: 
            print str(i[0])+ " " +  str(i[1]) + " " +str(i[2]) + " " + str(i[3]) + " " + str(i[4])
            contributors = i[3].split(",")
            exist = False
            for q in contributors:
                if str(q) == str(id):
                    exist = True
            if exist:
                info[i] = ["","",""] 
                info[i][0] = i[0] #title
                info[i][1] = i[4] #name of uid 
                info[i][2] = i[1] #body
        return info 


def add_story(title, body, contributor):
    # 1. Get the uid of the contributor
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row = curs.execute("SELECT uid from user where name='{p_name}'".format(p_name=contributor))
        story_creator = ""
        contributors = ""
        if row:
            for i in row:
                story_creator = i[0]
                contributors = story_creator
        # 2. Check if story exists.  Story exists if title exists
        curs.execute(
            "INSERT INTO story (title, body, uid, contributors) "
            "VALUES ('{p_title}', '{p_body}', '{p_uid}', '{p_contributors}')".format(
                p_title=title, p_body=body, p_uid=story_creator, p_contributors=contributors))


def add_contribution(title, contributor, text):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row = curs.execute("SELECT sid, contributors from story where title='{p_title}'".format(p_title=title))
        sid = ""
        contributors = []
        if row:
            sid = row[0]["sid"]
            contributors = row[0]["contributors"].split(",")
        row = curs.execute("SELECT uid from user where username='{p_username}'".format(p_username=contributor))
        uid = ""
        if row:
            uid = row[0]["uid"]
        if uid in contributors:
            #means this person has already contributed
            return False
        # insert to contribution table
        curs.execute(
            "INSERT INTO contribution(sid, uid, story_update, date_added) "
            "VALUES ('{p_sid}', '{p_uid}', '{p_update}', '{p_date}')".format(
                p_sid=sid, p_uid=uid, p_update=story_update, p_date=time.strftime("%c")))
        # update story table
        new_contributors = ','.join(contributors.append(uid))
        curs.execute(
            "UPDATE story SET contributors='{p_contributors}' WHERE sid='{p_sid}'".format(
                p_contributors=new_contributors, p_sid=sid))

        #update story body
        story_body = curs.execute("SELECT body from story where title={p_title}'".format(p_title=title))
        new_body = story_body + " " + new_body
        curs.execute(
            "UPDATE story SET body='{p_body}' WHERE sid='{p_sid}'".format(
                p_body=new_body, p_sid=sid))        
        return True

def get_storytext(title):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT body from story where title='{p_title}'".format(p_title=title))
        for i in row1:
            return i[0]

def get_storyauth(title):
    authid = ""
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



def last_contribution(title):
    with sqlite3.connect('data.db') as conn:
        curs = conn.cursor()
        row1 = curs.execute("SELECT sid from story where title='{p_title}'".format(p_title=title))
        sid = ""
        if row1:
            sid = row1[0]["sid"]
        row2 = curs.execute("SELECT story_update from contribution where cid=(SELECT max(cid) from contribution) GROUP BY sid='{p_sid}'".format(p_sid=sid))
        last = ""
        if row2:
            last = row2[0]["story_update"]
        return last




