import csv, hashlib

info = 'data/passwords.csv'

def register(inusername, inpassword):
    if len(inusername) < 3:
        return "Your username must be longer than 2 characters" #USERNAME LENGTH LESS THAN 3
    with open(info) as csvfile:
        reader = csv.reader(csvfile)
        unlocked = dict(reader)
        for username in unlocked:
            if username == inusername:
                return "Your username has been taken" #USERNAME TAKEN
    if len(inpassword) < 3:
        return "Your password must be longer than 2 characters" #PASSWORD LENGTH LESS THAN 3
    with open(info, "a") as csvfile:
        FieldNames = ['username','password']
        writer = csv.DictWriter(csvfile, fieldnames = FieldNames)
        hexedpass = hashlib.sha224(inpassword).hexdigest()
        writer.writerow({'username' : inusername , 'password' : hexedpass})
    return "You have been registered" #REGISTER SUCCESSFUL


def authuser(inusername):
    with open(info) as csvfile:
        reader = csv.reader(csvfile)
        dictreader = dict(reader)
        for username in dictreader:
            if username == inusername:
                return True
    return False


def auth(inusername,inpassword):
    with open(info) as csvfile:
        rawreader = csv.reader(csvfile)
        reader = dict(rawreader)
        for username in reader:
            if username == inusername:
                if (hashlib.sha224(inpassword).hexdigest() == reader[username]):
                    return -1 #SUCCESSFUL
                else:
                    return -2 #PASSWORD INCORRECT
    return -3 #USERNAME INCORRECT

        
