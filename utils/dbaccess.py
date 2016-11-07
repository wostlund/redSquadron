import sqlite3
import time


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
    curs.execute(
        "INSERT INTO users (name, password) "
        "VALUES ({p_user}, {p_password})".format(
            p_user=username, p_password=password))
    db.commit()

def add_story(body, title, contributor, uid):
    # 1. Get the uid of the contributor
    curs = db.cursor()
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
            "INSERT INTO story (body, title, contributors, uid) "
            "VALUES ({p_body}, {p_title}, {p_contributors}, {p_uid})".format(
                p_body=body, p_title=title, p_contributors=contributors, p_uid=uid))
        db.commit()
        return True

def add_contribution(title, contributor, text):
    curs = db.cursor()
    row = curs.execute("SELECT sid from story where title={p_title}".format(p_title=title))
    sid = ""
    if row:
        sid = row[0]["sid"]
    row = curs.execute("SELECT uid from user where username={p_username}".format(p_username))
    uid = ""
    if row:
        uid = row[0]["uid"]
    curs.execute(
        "INSERT INTO contribution(sid, uid, story_update, date_added) "
        "VALUES ({p_sid}, {p_uid}, {p_update}, {p_date})".format(
            p_sid=sid, p_uid=uid, p_update=story_update, p_date=time.strftime("%c"))


