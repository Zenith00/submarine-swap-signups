from flask import Flask, request
from psql_utils import database_exists
from hashlib import md5
import json
import psycopg2
from psycopg2 import extras
import TOKENS
import datetime
conn = psycopg2.connect(dbname='postgres', user='postgres', password=TOKENS.psql_pwd)
app = Flask(__name__)
dict_cur = conn.cursor(cursor_factory=extras.DictCursor)
cur = conn.cursor()
if not database_exists(cursor=cur, name="signup"):
    cur.execute('CREATE TABLE signup('
                'position SERIAL UNIQUE NOT NULL, '
                'score INT NOT NULL,'
                'name TEXT NOT NULL,'
                'email TEXT UNIQUE PRIMARY KEY NOT NULL, '
                'job TEXT NOT NULL, '
                'referral CHAR(32) NOT NULL,'
                'created_on TIMESTAMP NOT NULL)')


@app.route('/', methods=['POST', 'GET'])
def foo():
    print("RECIEVED")
    data = json.loads(request.data)
    print(data)
    return "OK"


def genreate_referral(name, email, job):
    return md5(name + email + job).hexdigest()

def insert_signup(name, email, job):
    cur.execute(f"INSERT INTO signup(score, name, email, job, referral, created_on) VALUES (0, {name}, {email}, {job}, {genreate_referral(name, email, job)}, {datetime.datetime.utcnow()});")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8080")
