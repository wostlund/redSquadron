import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("INSERT INTO user (name, password) VALUES ('testname','abc123')")
conn.commit()
conn.close()