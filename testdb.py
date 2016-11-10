import sqlite3, time
conn = sqlite3.connect('data.db')
title = 'test'
body = 'body'
curs = conn.cursor()
curs.execute(
    "INSERT INTO story (title, body, uid, contributors) "
    "VALUES ('{p_title}', '{p_body}', 1, '{p_contributors}')".format(
    	p_title=title, p_body=body, p_contributors=title))  
sid = curs.lastrowid
print ('last row ', sid)
# 4. Update contribution
curs.execute(
    "INSERT INTO contribution(sid, uid, story_update, date_added) "
    "VALUES ('{p_sid}', '{p_uid}', '{p_update}', '{p_date}')".format(
        p_sid=sid, p_uid=title, p_update=title, p_date=time.strftime("%c")))	


conn.commit()
conn.close()