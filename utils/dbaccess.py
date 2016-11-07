def check_reg(username, password):
    if not valid_username(username):
        return "Invalid username"
    curs = db.cursor()
    rows = curs.execute("SELECT name from user where name={input_name}".format(input_name=username))
    if rows:
        return "Username taken"
    return "Success"

def valid_username(username):
    if not username:
        return False

def add_account(username, password):
    curs = db.cursor()
    curs.execute("INSERT INTO users (name, password) VALUES ({input_u}, {input_p})".format(input_u=username, input_p=password))
    db.commit()
