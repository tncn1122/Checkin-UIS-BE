import flask
import secrets
from flask import request, jsonify, session
import xlrd
from firebase import firebase
from getListStudent import getListSTD
from getListStudent import readJsonSTD
from getListStudent import writeJsonSTD


app = flask.Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
linkDB = "/UIS/Students/"
# app.config["DEBUG"] = True
# init
database = []
database = getListSTD()
firebase = firebase.FirebaseApplication('https://jsrealtime-37d04.firebaseio.com', None)


@app.route('/')
def index():
  return "<h1>Server ok</h1>"

@app.route('/api/checkin', methods=['POST', 'GET'])
def roll_call():
    if request.method == 'POST':
        mssv = request.form.get('MSSV')
        if not session.__contains__('ds'):
            session['ds'] = readJsonSTD()
        ds = session['ds']
        # print(ds)
        if ds.__contains__(mssv):
            firebase.put(linkDB+ds.get(mssv),'diemDanh','1')
            print(ds.get(mssv))
            return "SUCCESS"
        else:
            return "NOTFOUND"

@app.route('/api/database', methods=['DELETE', 'POST'])
def database():
    if request.method == 'DELETE':
        firebase.delete('/UIS/', 'Students')
        session['ds'] = {}
        writeJsonSTD(session['ds'])
        return "DELETED"
    if request.method == 'POST':
        body = request.form
        data =  { 'MSSV': body['MSSV'],
          'ho': body['ho'],
          'ten': body['ten'],
          'diemDanh' : '0',
          }
        row = []
        row.append(body['MSSV'])
        row.append(body['do'])
        row.append(body['ten'])
        row.append('0')
        database.append(row)
        ds = session['ds']
        ds[body['MSSV']] = firebase.post(linkDB, data).get('name')
        writeJsonSTD(ds)
        return "ADDED"

@app.route('/api/database/reload', methods=['GET'])
def reload_database():
    if request.method == 'GET':
        ds = {}
        firebase.delete('/UIS/', 'Students')
        database = getListSTD()
        for x in database:
            data =  { 'MSSV': x[0],
                'ho': x[1],
                'ten': x[2],
                'diemDanh' : '0',
                }
            result = firebase.post(linkDB,data)
            ds[x[0]] = result['name']
        writeJsonSTD(ds)
        session['ds'] = ds
        # print(ds)
        return "RELOADED"

if __name__ == "__main__":    
    app.run()