import sqlite3
import json
from datetime import datetime

timeframe = '2019-06' # File time
sql_transaction = [] # Lots of inserts in one go

connection = sqlite3.connect('{}.db'.format(timeframe))
c = connection.cursor()


def createTable(): # subreddit can be used to make "different" bots later, adding more complexity
    c.execute("CREATE TABLE IF NOT EXISTS parentReply(parentID TEXT PRIMARY KEY, commentID TEXT UNIQUE, parent TEXT, comment TEXT, subreddit TEXT, unix INT, score INT)")

def formatData(data):
    data = data.replace("\n"," newlinechar ").replace("\r"," newlinechar ").replace('""'," ' ")
    return data

def findParent(pid):
    try:
        sql = "SELECT comment FROM parentReply WHERE commentID = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("findParent", e)
        return False

def findExistingScore(pid):
    try:
        sql = "SELECT score FROM parentReply WHERE parentID = '{}' LIMIT 1".format(pid)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        print("findExistingScore", e)
        return False

def acceptable(data):
    if len(data.split(" ")) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True

def transaction_bldr(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
            except:
                pass
        connection.commit()
        sql_transaction = []

def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO parent_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

if __name__ == "__main__":
    createTable()
    rowCounter = 0
    paired_rows = 0

    with open("E:RC_2019-06".format(timeframe.split('-')[0], timeframe), 'r', 1000) as f:
        for row in f:
            rowCounter += 1
            row = json.loads(row)
            commentID = row['id']
            parentID = row['parent_id'].split('_')[1]
            body = formatData(row['body'])
            createdUTC = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            parent_data = findParent(parentID)
            print(parent_data)
            if score >= 2 and acceptable(body):
                existingScore = findExistingScore(parentID)
                if existingScore:
                    if score > existingScore:
                        sql_insert_replace_comment(commentID, parentID, parent_data, body, subreddit, createdUTC, score)
                else:
                    if parent_data:
                        paired_rows += 1
                        sql_insert_has_parent(commentID, parentID, parent_data, body, subreddit, createdUTC, score)
                    else:
                        sql_insert_no_parent(commentID, parentID, body, subreddit, createdUTC, score)
            if rowCounter % 10000 == 0:
                print("Total rows read: {}, Paired rows: {}, Time: {}".format(rowCounter, paired_rows, str(datetime.now())))
