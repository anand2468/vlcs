import mysql.connector
db ={
    'host':'localhost',
    'user':'root',
    'port':3306,
    'database':'webapp',
    'password':'1029anand'
}

def findUser(username):
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'select userid from accounts where username = "{username}"'
    cur.execute(sq)
    print(sq)

    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def create_user(userid, username:str, profile):
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'INSERT INTO accounts (userid, username, profile) VALUES ( "{userid}" ,"{username}",{profile});'
    cur.execute(sq)
    conn.commit()
    print(sq)
    print('fectaoo', cur.fetchall())

    cur.close()
    conn.close()

def userDetails(uid):
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'SELECT * FROM accounts where userid = {uid}'
    cur.execute(sq)
    res = cur.fetchall()
    print('tye and res is', type(res), res)

    cur.close()
    conn.close()
    return res[0]

def allusers():
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'SELECT * FROM accounts'
    cur.execute(sq)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def findlast():
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'SELECT userid FROM accounts ORDER BY userid DESC LIMIT 1'
    cur.execute(sq)
    res = cur.fetchall()

    cur.close()
    conn.close()
    return res[0][0] # output is like [('002',)]

def send_message_db(convoid, sendBy, receievedBy, message):
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'INSERT INTO convos (convoid, sendBy, receievedBy, message) VALUES ( "{convoid}" ,"{sendBy}","{receievedBy}", "{message}");'
    cur.execute(sq)
    conn.commit()
    print(sq)
    print('updated successful', cur.fetchall())

    cur.close()
    conn.close()

def get_messages(convoid):
    conn = mysql.connector.connect(**db)
    cur= conn.cursor()

    sq = f'SELECT * FROM convos where convoid = {convoid} limit 20'
    cur.execute(sq)
    res = cur.fetchall()

    cur.close()
    conn.close()
    return res