import flask
from flask import Flask, request
from psql_utils import database_exists, table_exists
from hashlib import md5
import json
import psycopg2
from psycopg2 import extras
import TOKENS
import datetime

conn = psycopg2.connect(dbname='postgres', user='postgres', password=TOKENS.psql_pwd)
conn.autocommit = True
app = Flask(__name__)
cur = conn.cursor()

if not database_exists(cursor=cur, name="signup"):
    cur.execute('CREATE DATABASE signup')

conn.commit()
conn.close()
conn = psycopg2.connect(dbname='signup', user='postgres', password=TOKENS.psql_pwd)
cur = conn.cursor()
if not table_exists(conn, "signup"):
    cur.execute('CREATE TABLE signup('
                'position SERIAL UNIQUE NOT NULL, '
                'score INT NOT NULL,'
                'name TEXT NOT NULL,'
                'email TEXT UNIQUE PRIMARY KEY NOT NULL, '
                'job TEXT NOT NULL, '
                'referral CHAR(32) NOT NULL,'
                'created_on TIMESTAMP NOT NULL)')


def already_signedup(email):
    cur.execute(f"select exists(SELECT * FROM signup WHERE email='{email}')")
    return cur.fetchone()[0]


@app.route("/signup", methods=['GET'])
def getsignups():
    print("SIGNUP RECIEVED")
    cur.execute('SELECT COUNT(*) FROM signup;')
    v = cur.fetchall()
    resp = flask.Response(
        f'<div class=\"contents\"><p style=\"text-align: center; line-height: 21px; font-size: 15px;\"><b>{v[0][0]} people ahead of you</b></p></div>')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    print(resp)
    return resp


@app.route('/', methods=['POST', 'GET'])
def foo():
    print("RECIEVED")
    print(request.data)
    data = request.values.to_dict()
    print(data)
    referral_source = data["referralsource"]
    if "?referral=" in referral_source:
        referral = referral_source.split("?referral=")[1]
        referred_from(referral)
    if not already_signedup(data["email"]):
        insert_signup(data["name"], data["email"], data["workplace"])
        return "OK"
    else:
        return "Already Signed Up"

x
def generate_referral(name, email, job):
    return md5((name + email + job).encode('utf-8')).hexdigest()


def insert_signup(name, email, job):
    referral = generate_referral(name, email, job)
    cur.execute(f"INSERT INTO signup(score, name, email, job, referral, created_on) "
                f"VALUES (0, '{name}', '{email}', '{job}', '{referral}', '{datetime.datetime.utcnow()}');")
    conn.commit()
    print(referral)
    return referral


def referred_from(referral):
    print(referral)
    cur.execute(f"SELECT * FROM signup WHERE referral='{referral}'")
    v = cur.fetchall()
    print(v)
    print("\n\na\n")
    cur.execute(f"UPDATE signup "
                f"  SET score = score + 1 "
                f"WHERE referral='{referral}' RETURNING score, position, email")
    v = cur.fetchall()
    conn.commit()
    print(v)
    print("endrefer")


def get_position(email):
    cur.execute(f"SELECT ss.rank FROM "
                f"(SELECT score, position, email, rank() OVER (ORDER BY score-position DESC) AS rank FROM signup) AS ss "
                f"WHERE email='{email}';")
    return cur.fetchone()[0]


def printall():
    cur.execute(f"SELECT *, score-position FROM signup ORDER BY score-position DESC")paymen
    v = cur.fetchall()
    for subv in v:
        print(subv)
    conn.commit()







    # a = insert_signup("testname","testemail","testjob")
    # input()

    # insert_signup("testnamesub","testemailsub","testjobsub")

    # print(a)

    # for i in range(20):
    #     insert_signup("name"+str(i), "email"+str(i), "job"+str(i))

    # print(get_position("testemailsub"))
    # printall()

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port="9001")
