from flask import Flask, request, jsonify, abort
import random
import psycopg2
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'application/json'


conn = psycopg2.connect(database = "Students", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "admin",
                        port = 5432)


def generateToken():
    return ''.join(random.choices(
        population='abcdefghijklmnopqrstuvwxwz1234567890!@#$%^&*()', k=128))

# Key is token, value is access type
access_tokens = {}
@app.after_request
def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true,X-Requested-With')
        response.headers.add('Access-Control-Allow-Credentials',True)
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

@app.route('/login/<username>/<password>')
def login(username, password):
    cur = conn.cursor()
    cur.execute('SELECT * FROM USERS;')
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    for row in rows:
        if row[1] == username and row[2] == password:
            token = generateToken()
            if row[3]:
                access_tokens.update({token:"admin"})
                return f'{token}'
            else:
                access_tokens.update({token:"user"})
                return 'user page'
    abort(403)

@app.route('/student', methods=['POST'])
def accessStudentData():
    data = request.get_json()
    try:
        id = data['id'],data['access_key']
    except:
        abort(415)
    print(data)
    """
    check data base for data
    parse student data from database and replace the data in the html page with student data
    """
    return 'ss'

app.run(debug=True)