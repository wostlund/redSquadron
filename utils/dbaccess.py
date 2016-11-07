import sqlite3


db = sqlite3.connect(../data/data.db)

def check_reg(username, password):

    if not valid_username(username):
        return "Invalid username"
    curs = db.cursor()
    rows = curs.execute("SELECT name from user where name={p_name}".format(p_name=username))
    if rows:
        return "Username taken"
    return "Success"

def valid_username(username):
    if not username:
        return False

def add_account(username, password):
    curs = db.cursor()
    curs.execute("INSERT INTO users (name, password) VALUES ({p_user}, {p_password})".format(p_user=username, p_password=password))
    db.commit()

def add_story(body, title, contributor, uid):
    # 1. Get the uid of the contributor
    curs = db.cursor()
    row = curs.execute("SELECT uid from user where name={p_name}".format(p_name=contributor))
    story_creator = ""
    contributors = ""
    if row:
        story_creator = row["uid"]
        contributors = story_creator
    # 2. Check if story exists.  Story exists if title exists
    row = curs.execute("SELECT sid from story where title={p_title}".format(p_title=title))
    if row:
        return False
    else:
        curs.execute("INSERT INTO story (body, title, contributors, uid) VALUES ({p_body}, {p_title}, {p_contributors}, {p_uid})".format(p_body=body, p_title=title, p_contributors=contributors, p_uid=uid))
        db.commit()
        return True

