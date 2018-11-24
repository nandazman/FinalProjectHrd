from flask import Flask, request, json, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal, fields
from flask_cors import CORS
from requests.utils import quote
import datetime
import os
import jwt
import requests





app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Dewa626429@localhost:5432/DataNext'
app.config['SECRET_KEY'] = os.urandom(24)

CORS(app)

db = SQLAlchemy(app)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_code = db.Column(db.Integer())
    position = db.Column(db.String())
    company = db.Column(db.String())
    cost_center = db.Column(db.String())
    personal_area = db.Column(db.String())
    personal_sub_area = db.Column(db.String())
    employee_type = db.Column(db.String())
    employee_group = db.Column(db.String())
    employee_sub_group = db.Column(db.String())


class Departemen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String())

class AccessUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    npk = db.Column(db.Integer())
    email = db.Column(db.String())
    name = db.Column(db.String())
    password = db.Column(db.String())
    photo = db.Column(db.String())
    token = db.Column(db.String())
    role = db.Column(db.String())
    departemen_id = db.Column(db.Integer, db.ForeignKey('departemen.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    npk = db.Column(db.Integer())
    nama = db.Column(db.String())
    departemen_id = db.Column(db.Integer, db.ForeignKey("departemen.id"))
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer())
    record_id = db.Column(db.Integer())
    distribution_cost_center = db.Column(db.Integer())
    dates = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    coment = db.Column(db.String())
    requester_id = db.Column(db.Integer, db.ForeignKey("access_user.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("access_user.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))

@app.route('/')
def hallo():
    return "Sup Bro"

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        request_data = request.get_json()

        req_email = request_data.get('email')
        req_password = request_data.get('password')
        userDB = AccessUser.query.filter_by(email=req_email, password=req_password).first()
        if userDB is not None:
            
            payload = {
                "email" : userDB.email
            }
            
            encoded = jwt.encode(payload, 'tralala', algorithm='HS256')

            return encoded, 200

        else:
            return 'Email or Password is not found' , 404
    else:
        return 'Method Not Allowed', 405
    

#########################################################
####################### Nextflow ########################
#########################################################

@app.route('/submitToHRD', methods = ['GET', 'POST'])
##### inisasi nextflow atau create record #####
def create_record():
    
    request_data = request.get_json()
    req_email = request_data.get('email')
    req_comment = request_data.get('comment')

    userDB = AccessUser.query.filter_by(email = req_email).first()
    
    if userDB is not None:
        user_token = userDB.token
  
        # data template untuk ngecreate record di body json
        record_instance = {
            "data": {
                "definition": {
                    # mosaic bla bla records
                    "id" : os.getenv('DEFINITION_ID')
                }
            }
        }

        # submit ke nextflow untuk dapetin record_id tiap pesanan masuk
        r = requests.post(os.getenv("BASE_URL_RECORD"), data = json.dumps(record_instance), headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

        # resulit from create record
        result = json.loads(r.text)

        # ambil record id nya terus masukin ke variabel
        record_id = result['data']['id']

        # submit flow pake record_id dan token
        # ke fungsi submit_record
        submit_record(record_id, user_token)

        # gerakin flow dari requester ke manager
        # dimasukin variabel karena butuh task list
        process_instance = submit_to_HRD(req_comment, user_token)

        # masukin data ke database
        # ngriim record id sama process id dari process_instance
        # data_db = submit_to_database(record_id, process_instance['data']['process_id'])

        # return berupa id, dan statusnya
        return "Submitted", 200

    else:
        return "Token not found", 404

# fungsi untuk submit record
def submit_record(record_id, user_token):
    # data template untuk ngesubmit record di body nya nextflow
    record_instance = {
        "data": {
            "form_data": {
                # ada siapa yang yang berkaitan di seluruh flow
                "pvRequester": "rudi_hrd@makersinstitute.id",
                "pvHrdept": "Hader_hrd@makersinstitute.id",
                "pvHrcomp": "Haper_hrd@makersinstitute.id",
                "pvDeptman": "Germen_hrd@makersinsitute.id",
                "pvSenman": "sena_hrd@makersinstitute.id",
                "pvHrprop": "haprop_hrd@makersinstitute.id"
            },
            "comment": "New Record Initiated"
        }
    }

    request_data = json.dumps(record_instance)

    # submit ke nextflow untuk dapetin process_id tiap pesanan masuk.flow
    # https://mosaic-engine.dev.nextflow.tech/makers/api/records/record:test-20181122-6/submit API buat submit
    # data itu body nya
    r = requests.post(os.getenv("BASE_URL_RECORD") + "/" + record_id + "/submit", data = request_data, headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

    result = json.loads(r.text)

    return result

# fungsi untuk gerakin flow dari requester ke manager
# submit tar gerak flownya dari start ke proses selanjutnya
def submit_to_HRD(req_comment, user_token):
    # get task id and pVmanager
    # name = requester dari nama flow nya
    # definition id = dari .env
    # get task listnya dlu sesuai [name]
    query = "folder=app:task:all&page[number]=1&page[size]=10&filter[name]=Requester&filter[state]=active&filter[definition_id]=%s" % (
        os.getenv("DEFINITION_ID"))
    
    # ngubah url nya
    url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")

    # bearer %s user tokennya
    # buat ngambil task ddari si requesternya apa aja
    r = requests.get(url , headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

    result = json.loads(r.text)

    # get manager email dan task id
    
    hrdDepartment = result['data'][0]['form_data']['pvHrdept']
    hrdCompany = result['data'][0]['form_data']['pvHrcomp']
    task_id = result['data'][0]['id']

    # gerakin flow dari requester ke hrd
    # task list dari requester bakal pindah ke hrd
    submit_data = {
        "data": {
            "form_data": {
                # ini ngirim ke siapa aja
                "pvHrdept": hrdDepartment,
                "pvHrcomp": hrdCompany
            },
            "comment": req_comment
        }
    }

    # buat ngirim requestnya
    r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
        "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
    })

    result = json.loads(r.text)

    return result
    
# fungsi untuk memasukan data ke db
# def submit_to_database(record_id, process_id):
#     # request_data = request.get_json()
#     # req_code = request_data['data']['code']
#     # req_price = request_data['data']['price']

#     # buat ada template ke dbnya
#     data_db = Summary(
#         # code = req_code,
#         # price = req_price,
#         process_id = process_id,
#         record_id = record_id
#     )

#     db.session.add(data_db)
#     db.session.commit()
#     db.session.flush()

#     if data_db is not None:
#         return str(data_db.id)
#     else:
#         return None

@app.route('/GetTask', methods = ['GET', 'POST'])
#### Get access user task ####
def get_task():
    request_data = request.get_json()
    print(request_data)
    req_email = request_data['email']

    userDB = AccessUser.query.filter_by(email = req_email).first()

    if userDB is not None:
        user_token = userDB.token
        name = userDB.role
        # print(name)
        query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s" % (name, os.getenv("DEFINITION_ID"))
        
        # https://mosaic-engine.dev.nextflow.tech/makers/api/tasks?folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s
        # https://mosaic-engine.dev.nextflow.tech/makers/api/tasks?folder=app:task:all&filter[name]=%s&filter%5Bstate%5D=active&filter%5Bdefinition_id%5D=definitions%3Abpmn%3Afabf8af1-4516-4876-ba13-a7c9ee118133
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
        print(url)
        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)

        return json.dumps(result)

@app.route('/HRDCheck', methods = ['GET', 'POST'])
#### hrd department to manager department ####
def hrd_check():

    request_data = request.get_json()
    req_email = request_data.get('email')
    req_comment = request_data.get('comment')

    userDB = AccessUser.query.filter_by(email = req_email).first()
    
    if userDB is not None:
        user_token = userDB.token

        query = "folder=app:task:all&page[number]=1&page[size]=10&filter[name]=HR Department&filter[state]=active&filter[definition_id]=%s" % (
            os.getenv("DEFINITION_ID"))
        
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")

        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)
        ####### ngefilter tasknya pake task id aja yang ditanem di depan front end ######

        manager_department = result['data'][0]['form_data']['pvDeptman']

        task_id = result['data'][0]['id']

        submit_data = {
        "data": {
            "form_data": {
                # ini ngirim ke siapa aja
                "pvDeptman": manager_department,
            },
            "comment": req_comment
        }
    }

        # buat ngirim requestnya
        r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

        result = json.loads(r.text)

        return "Success", 200

    else:
        return "Bad Request", 404

@app.route('/HRCompanyCheck', methods = ['GET', 'POST'])
#### hrd company to manager department ####
def hrd_company_check():

    request_data = request.get_json()
    req_email = request_data.get('email')
    req_comment = request_data.get('comment')

    userDB = AccessUser.query.filter_by(email = req_email).first()
    
    if userDB is not None:
        user_token = userDB.token
     
        query = "folder=app:task:all&page[number]=1&page[size]=10&filter[name]=HR Company&filter[state]=active&filter[definition_id]=%s" % (
            os.getenv("DEFINITION_ID"))
        
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")

        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)
        ####### ngefilter tasknya pake task id aja yang ditanem di depan front end ######
     
        manager_department = result['data'][0]['form_data']['pvDeptman']

        task_id = result['data'][0]['id']

        submit_data = {
        "data": {
            "form_data": {
                # ini ngirim ke siapa aja
                "pvDeptman": manager_department,
            },
            "comment": req_comment
        }
    }

        # buat ngirim requestnya
        r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

        result = json.loads(r.text)

        return "Success", 200

    else:
        return "Bad Request", 404

@app.route('/ManagerDepartmentCheck', methods = ['GET', 'POST'])
#### Manager department to senior manager ####
def manager_department_check():

    request_data = request.get_json()
    req_email = request_data.get('email')
    req_comment = request_data.get('comment')
    req_status = request_data.get('status')

    userDB = AccessUser.query.filter_by(email = req_email).first()
    
    if userDB is not None:
        user_token = userDB.token
  
        query = "folder=app:task:all&page[number]=1&page[size]=10&filter[name]=Department Manager&filter[state]=active&filter[definition_id]=%s" % (
            os.getenv("DEFINITION_ID"))
        
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")

        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)
        ####### ngefilter tasknya pake task id aja yang ditanem di depan front end ######

        task_id = result['data'][0]['id']

        submit_data = {
        "data": {
            "form_data": {
                # ngirim status revisi atau tidadk
                "pvAction": req_status,
            },
            "comment": req_comment
        }
    }

        # buat ngirim requestnya
        r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

        result = json.loads(r.text)

        return "Success", 200

    else:
        return "Bad Request", 404

@app.route('/SeniorManagerCheck', methods = ['GET', 'POST'])
#### senior manager to hrd proposed ####
def manager_senior_check():

    request_data = request.get_json()
    req_email = request_data.get('email')
    req_comment = request_data.get('comment')
    req_status = request_data.get('status')

    userDB = AccessUser.query.filter_by(email = req_email).first()
    
    if userDB is not None:
        user_token = userDB.token
  
        query = "folder=app:task:all&page[number]=1&page[size]=10&filter[name]=Senior Manager &filter[state]=active&filter[definition_id]=%s" % (
            os.getenv("DEFINITION_ID"))
        
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")

        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)
        ####### ngefilter tasknya pake task id aja yang ditanem di depan front end ######

        task_id = result['data'][0]['id']

        submit_data = {
        "data": {
            "form_data": {
                # ngirim status revisi atau tidadk
                "pvAction": req_status,
            },
            "comment": req_comment
        }
    }

        # buat ngirim requestnya
        r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

        result = json.loads(r.text)

        return "Success", 200

    else:
        return "Bad Request", 404

@app.route('/HRProposedCheck', methods = ['GET', 'POST'])
#### hrd proposed confirm ####
def hrd_proposed_check():

    request_data = request.get_json()
    req_email = request_data.get('email')
    req_comment = request_data.get('comment')

    userDB = AccessUser.query.filter_by(email = req_email).first()
    
    if userDB is not None:
        user_token = userDB.token

        query = "folder=app:task:all&page[number]=1&page[size]=10&filter[name]=Proposed HR Department&filter[state]=active&filter[definition_id]=%s" % (
            os.getenv("DEFINITION_ID"))
        
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")

        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)
        ####### ngefilter tasknya pake task id aja yang ditanem di depan front end ######


        task_id = result['data'][0]['id']

        submit_data = {
        "data": {
            "comment": req_comment
        }
    }

        # buat ngirim requestnya
        r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

        result = json.loads(r.text)

        return "Success", 200

    else:
        return "Bad Request", 404

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT"))
