from flask import Flask, request, json, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal, fields
from flask_cors import CORS
from requests.utils import quote
import datetime
import os
import jwt
import requests
from sqlalchemy import and_





app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test@localhost:5432/DatabaseHRD'
app.config['SECRET_KEY'] = os.urandom(24)

CORS(app)

db = SQLAlchemy(app)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_code = db.Column(db.Integer())
    position = db.Column(db.String())
    company = db.Column(db.String())
    cost_center_code = db.Column(db.String())
    cost_center = db.Column(db.String())
    personal_area = db.Column(db.String())
    personal_sub_area = db.Column(db.String())
    employee_type = db.Column(db.String())
    employee_group = db.Column(db.String())
    employee_sub_group = db.Column(db.String())
    departemen_id = db.Column(db.Integer, db.ForeignKey("departemen.id"))


class Departemen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String())

class AccessUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    npk = db.Column(db.Integer())
    email = db.Column(db.String())
    nama = db.Column(db.String())
    password = db.Column(db.String())
    photo = db.Column(db.String())
    token = db.Column(db.String())
    role = db.Column(db.String())
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    npk = db.Column(db.Integer())
    nama = db.Column(db.String())
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.String())
    record_id = db.Column(db.String())
    distribution_cost_center = db.Column(db.String())
    dates = db.Column(db.String())
    coment = db.Column(db.String())
    behalf_name = db.Column(db.String())
    behalf_position = db.Column(db.String())
    requester_id = db.Column(db.Integer, db.ForeignKey("access_user.id"))
    receiver_id = db.Column(db.Integer, db.ForeignKey("access_user.id"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"))
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))

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


@app.route('/getProfile', methods = ["GET"])
def profile():
    if request.method == 'GET':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])

        user = AccessUser.query.filter_by(email=decoded['email']).first()
        position = Position.query.filter_by(id=user.position_id).first()

        user_nama = {
            "nama": user.nama,
            "npk": user.npk,
            "role": position.position,
            "departemen_id": position.departemen_id
        }
        user = json.dumps(user_nama)

        return user
    else:
        return "Method not allowed", 405

@app.route('/employee', methods = ["GET"])
def employee():
    if request.method == 'GET':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])

        user = AccessUser.query.filter_by(email=decoded['email']).first()
        position = Position.query.filter_by(id=user.position_id).first()
        departemenManager = position.departemen_id
        employeeDB = Employee.query.all()

        employee_data = []

        for data in employeeDB:
            departemenEmployee = (Position.query.filter_by(id=data.position_id).first()).departemen_id
            if departemenManager == departemenEmployee:
                employee = {
                    'npk': data.npk,
                    'nama': data.nama,
                    'position_id': data.position_id
                }
                employee_data.append(employee)

        data = json.dumps(employee_data)
        # print(data)
        return data, 200

@app.route('/current', methods = ['POST'])
def current_data():
    if request.method == 'POST':

        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
    

        request_data = request.get_json()
        position_id = request_data['id']

        position_data = Position.query.filter_by(id=position_id).first()


        employee = {
                'id': position_data.id,
                'position_code': position_data.position_code,
                'position': position_data.position,
                'company': position_data.company,
                'cost_center': position_data.cost_center,
                'cost_center_code': position_data.cost_center_code,
                'personal_area': position_data.personal_area,
                'employee_group': position_data.employee_group,
                'employee_sub_group': position_data.employee_sub_group
            }

        data = json.dumps(employee)
        
        return data, 200

@app.route('/proposed', methods = ['POST'])
def proposed_position():
    if request.method == 'POST':
    
        request_data = request.get_json()
        position_id = request_data['id']
        # print(position_id)
        position_data = Position.query.filter_by(id = position_id).first()

        position_list = Position.query.filter(and_(Position.id != position_data.id, Position.departemen_id != position_data.departemen_id, Position.departemen_id != 1)).all()
        positions = []
        for data in position_list:
            position = {
                    'id': data.id,
                    'position_code': data.position_code,
                    'position': data.position
                }
            positions.append(position)
        data = json.dumps(positions)

        return data, 200


@app.route('/proposeddata', methods = ['POST'])
def proposed_data():
    if request.method == 'POST':

        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
    

        request_data = request.get_json()
        position_id = request_data['id']
        position_data = Position.query.filter_by(id=position_id).first()
        # print(position_data)
        
        receiver = AccessUser.query.join(Position).add_columns(Position.departemen_id).filter(Position.departemen_id == position_data.departemen_id).first()
        receiver_email = receiver[0].email
        receier_id = receiver[0].id
        # print(receiver)
        # print(receiver[0].email)
        employee = {
                'id': position_data.id,
                'position_code': position_data.position_code,
                'position': position_data.position,
                'company': position_data.company,
                'cost_center': position_data.cost_center,
                'cost_center_code': position_data.cost_center_code,
                'personal_area': position_data.personal_area,
                'personal_sub_area': position_data.personal_sub_area,
                'employee_type': position_data.employee_type,
                'receiver': receiver_email,
                'receier_id': receier_id
            }

        data = json.dumps(employee)
        
        return data, 200


@app.route('/tableSummary', methods = ["POST"])
def get_Summary():
    if request.method == 'POST':
        
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        request_data = request.get_json()
        record_id = request_data['recordid']
        summary_data = Summary.query.filter_by(record_id = record_id).first()
        
        
        # GET requester data
        requester_data = AccessUser.query.join(Position).add_columns(AccessUser.nama, AccessUser.npk, Position.position).filter(AccessUser.id == summary_data.requester_id).first()
        # GET receiver data
        receiver_data = AccessUser.query.filter_by(id = summary_data.receiver_id).first()
        # GET employee data
        employee_data = Employee.query.join(Position).add_columns(Employee.nama, Employee.npk, Position.position_code, Position.position, Position.company, Position.cost_center, Position.cost_center_code, Position.personal_area, Position.employee_group, Position.employee_sub_group).filter(Employee.id == summary_data.employee_id).first()
        # print(employee_data)
        # GET target position
        proposed_position = Position.query.filter_by(id = summary_data.position_id).first()
        # Summary data for form
        summary = {
            'requester': {
            'name': requester_data[1],
            'npk': requester_data[2],
            'position': requester_data[3]
            },
            'behalf': {
            'behalf_name': summary_data.behalf_name,
            'behalf_position': summary_data.behalf_position
            },
            'employee': {
            'employee_name': employee_data[1],
            'employee_npk': employee_data[2]
            },
            'record_id': summary_data.record_id,
            'current': {
            'position_code': employee_data[3],
            'position': employee_data[4],
            'company': employee_data[5],
            'cost_center_code': employee_data[7],
            'cost_center': employee_data[6],
            'personal_area': employee_data[8],
            'employee_group': employee_data[9],
            'employee_sub_group': employee_data[10]
            },
            'proposed': {
            'position_code': proposed_position.position_code,
            'position': proposed_position.position,
            'distribution_cost_center': summary_data.distribution_cost_center,
            'company': proposed_position.company,
            'cost_center_code': proposed_position.cost_center_code,
            'cost_center': proposed_position.cost_center,
            'personal_area': proposed_position.personal_area,
            'personal_sub_area': proposed_position.personal_sub_area,
            'type': proposed_position.employee_type
            },
            'receiver': receiver_data.nama,
            'date': summary_data.dates,
            'comment': summary_data.coment
        }
       
        userDB = AccessUser.query.filter_by(email = decoded['email']).first()
        user_token = userDB.token

        user = AccessUser.query.join(Position).order_by(AccessUser.id).add_columns(AccessUser.role, AccessUser.nama, Position.position).all()
        
        positions = {}
        activities = ['Prepare Rotation', 'HRCS Verification', 'MAIN HR Verification', 'SM Approval', 'MBD Approval', 'HRBD Verification']
        i = 0
        for data in user:
            print(data)
            positions[data[2]] = {
                'position' : data[3],
                'activity': activities[i]
            }
            i = i +1
            # print(positions)

       
        # print(positions)
        # GET comment history
        r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + request_data['recordid'] + "/stageview", headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
                })

        result = json.loads(r.text)
        
        # Put form data and comment history in one variable to send to Front End
        summarize = {
            'form_data': summary,
            'comment_history': result,
            'comment_history_from_db': positions
        }
        
        summarize = json.dumps(summarize)
        return summarize , 200

@app.route('/getSAP', methods = ["GET"])
def get_SAP():
    if request.method == 'GET':
        flow_before = {
            'Department Manager': ['HR Department', 'HR Company'],
            'Senior Manager ': 'Department Manager',
            'Proposed HR Department': 'Senior Manager'
            }
        
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        
        SAP = Summary.query.all()
        userDB = AccessUser.query.filter_by(email = decoded['email']).first()
        user_token = userDB.token
        
        allSAP = []
        for data in SAP:
            
            r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + data.record_id + "/stageview", headers = {
                        "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
                    })
            
            result = json.loads(r.text)

            # GET last person who submit when record finished
            if result['data'][-1]['type'] == 'record:state:completed':
                data = {
                    'last_submitted' : 'Proposed HR Department',
                    'record_id' : data.record_id
                }
            # When there is revision to requester
            elif result['data'][-1]['type'] == 'task:assigned' and result['data'][-1]['target']['display_name'] == "Requester":
                data = {
                    'last_submitted' : '',
                    'record_id' : data.record_id
                }
                
            # GET last person who submit when 2 hr have not approved
            elif result['data'][-1]['type'] == 'task:assigned' and result['data'][-2]['type'] == 'task:assigned':
                data = {
                    'last_submitted' : 'Requester',
                    'record_id' : data.record_id
                }

            # GET last person who submit when one hr already submitted
            elif result['data'][-1]['type'] == 'task:completed:comment':
                data = {
                    'last_submitted' : result['data'][-1]['object']['display_name'],
                    'record_id' : data.record_id
                }
            # GET last person who submit when after all hr submitted
            elif result['data'][-1]['type'] == 'task:assigned':
                data = {
                    'last_submitted' : flow_before[result['data'][-1]['target']['display_name']],
                    'record_id' : data.record_id
                }

            

            allSAP.append(data)
        SAP = json.dumps(allSAP)
        
        # print(allSAP)

        return SAP, 200
        
# @app.route('/getProfile', methods = ["GET"])
# def profile():
#     if request.method == 'GET':
#         decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])

#         user = AccessUser.query.filter_by(email=decoded['email']).first()
#         position = Position.query.filter_by(id=user.position_id).first()
#         user_nama = {
#             "nama": user.nama,
#             "npk": user.npk,
#             "role": position.position
#         }
#         user = json.dumps(user_nama)

#         return user

# @app.route('/employee', methods = ["GET"])
# def employee():
#     if request.method == 'GET':
#         decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])



#########################################################
####################### Nextflow ########################
#########################################################

@app.route('/submitRecord', methods = ['GET', 'POST'])
##### inisasi nextflow atau create record #####
def create_record():
    decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
    request_data = request.get_json()
    
    req_comment = request_data.get('comment')

    userDB = AccessUser.query.filter_by(email = decoded['email']).first()

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
        submit_record(record_id, user_token,request_data)

        # gerakin flow dari requester ke manager
        # dimasukin variabel karena butuh task list
        # process_instance = submit_to_HRD(req_comment, user_token)

        # masukin data ke database
        # ngriim record id sama process id dari process_instance
        # data_db = submit_to_database(record_id, process_instance['data']['process_id'],request_data)

        # return berupa id, dan statusnya
        return "Submitted", 200

    else:
        return "Token not found", 404

# fungsi untuk submit record
def submit_record(record_id, user_token,request):
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
    submit_to_database(record_id, "null",request)
    return "submitted", 200


    

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
    if result is None:
        task_id = 0
    elif result is not None:
        task_id = result['data'][-1]['id']
    # get manager email dan task id

    result = waitingRespone(user_token,url, task_id)

    hrdDepartment = result['data'][0]['form_data']['pvHrdept']
    hrdCompany = result['data'][0]['form_data']['pvHrcomp']
    task_id = result['data'][-1]['id']

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

def waitingRespone(user_token,url,task_id):
    
    r = requests.get(url , headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
        })

    result = json.loads(r.text)
    # if already got response and task id is different with current one
    if result['data'] != [] and result['data'][-1]['id'] != task_id:
        return result
    return waitingRespone(user_token,url,task_id)

# insert to db

def submit_to_database(record_id, process_id,request_data):

    req_employee_data = request_data.get('employee')
    req_receiver = request_data.get('receiver')
    req_requester = request_data.get('requester')
    req_position_id = int(request_data.get('position'))
    req_behalf_name = request_data.get('behalf-name')
    req_behalf_position = request_data.get('behalf-position')
    req_distribution = request_data.get('distribution')
    req_date = request_data.get('date')
    req_comment = request_data.get('comment')

    req_employee_name = req_employee_data.split(" - ")[1]
 
    req_employee_id = (Employee.query.filter_by(nama = req_employee_name).first()).id
    req_requester_id = (AccessUser.query.filter_by(nama = req_requester).first()).id
    req_receiver_id = (AccessUser.query.filter_by(email = req_receiver).first()).id

    # buat ada template ke dbnya
    data_db = Summary(
        process_id = process_id,
        record_id = record_id,
        distribution_cost_center = req_distribution,
        dates = req_date,
        coment = req_comment,
        behalf_name = req_behalf_name,
        behalf_position = req_behalf_position,
        requester_id = req_requester_id,
        receiver_id = req_receiver_id,
        employee_id = req_employee_id,
        position_id = req_position_id
    )
    
    db.session.add(data_db)
    db.session.commit()
    # db.session.flush()

    if data_db is not None:
        return "str(data_db.id)"
    else:
        return None

@app.route('/GetTask', methods = ['GET', 'POST'])
#### Get access user task ####
def get_task():
    decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])

    userDB = AccessUser.query.filter_by(email = decoded['email']).first()
    
    if userDB is not None:
        user_token = userDB.token
        name = userDB.role
        # print(name)
        query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s" % (name, os.getenv("DEFINITION_ID"))
        
        # https://mosaic-engine.dev.nextflow.tech/makers/api/tasks?folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s
        # https://mosaic-engine.dev.nextflow.tech/makers/api/tasks?folder=app:task:all&filter[name]=%s&filter%5Bstate%5D=active&filter%5Bdefinition_id%5D=definitions%3Abpmn%3Afabf8af1-4516-4876-ba13-a7c9ee118133
        # ngubah url nya
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
        
        # bearer %s user tokennya
        # buat ngambil task ddari si requesternya apa aja
        r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

        result = json.loads(r.text)
        
        return json.dumps(result)

@app.route('/submitTask', methods = ['GET', 'POST','PUT'])
### Submit task by User ###
def submit_task():
    currentToTarget = {
        "HR Department": "Germen_hrd@makersinsitute.id",
        "HR Company": "Germen_hrd@makersinsitute.id",
        "Department Manager": "status_revise",
        "Senior Manager ": "status_revise",
        "Proposed HR Department": "sent_email",
        "Requester": ["Hader_hrd@makersinstitute.id","Haper_hrd@makersinstitute.id"]
    }
    decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
    userDB = AccessUser.query.filter_by(email = decoded['email']).first()
    user_token = userDB.token

    if request.method == "POST":

        if userDB is not None:
            
            request_data = request.get_json()
            task_id = request_data.get('taskid')
            record_id = request_data.get('recordid')
            status = request_data.get('status')
            req_comment = request_data.get('comment')

            r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + record_id + "/stageview", data = request_data, headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
                })

            result = json.loads(r.text)
            
            # get manager email dan task id
            for data in result['data']:
                # not all array have target display_name
                try:
                    if data['target']['id'] == task_id:
                        currentUserTask = data['target']['display_name']
                        break
                except KeyError:
                    continue
            
            nextTarget = currentToTarget[currentUserTask]
            

            if nextTarget == "Germen_hrd@makersinsitute.id":
                # print(nextTarget)
                submit_data = {
                    "data": {
                        "form_data": {
                            # ini ngirim ke siapa aja
                            "pvDeptman": nextTarget
                        },
                        "comment": req_comment
                    }
                }
            elif nextTarget == "status_revise":
                submit_data = {
                    "data": {
                        "form_data": {
                            # ini ngirim ke siapa aja
                            "pvAction": status
                        },
                        "comment": req_comment
                    }
                }
            

            r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
            })

            
            return "Submitted", 200

        else:
            return "Bad request", 400

    elif request.method == "PUT":

        if userDB is not None:
            request_data = request.get_json()
            task_id = request_data.get('taskid')
            record_id = request_data.get('recordid')
            

            r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + record_id + "/stageview", data = request_data, headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
                })

            result = json.loads(r.text)
            
            # get manager email dan task id 
            for data in result['data']:
                # not all array have target display_name
                try:
                    if data['target']['id'] == task_id:
                        currentUserTask = data['target']['display_name']
                        break
                except KeyError:
                    continue
            
            nextTarget = currentToTarget[currentUserTask]

            if nextTarget[0] ==  "Hader_hrd@makersinstitute.id":
                behalf_name = request_data.get('behalf-name')
                behalf_position = request_data.get('behalf-position')
                distribution = request_data.get('distribution')
                date = request_data.get('date')
                comment = request_data.get('comment')

                submit_data = {
                    "data": {
                        "form_data": {
                            # ini ngirim ke siapa aja
                            "pvHrdept": nextTarget[0],
                            "pvHrcomp": nextTarget[1]
                        },
                        "comment": comment
                    }
                }

                r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
                })

                response = json.loads(r.text)
                
                process_id = response['data']['process_id']

                revised = Summary.query.filter_by(record_id = record_id).first()
                revised.process_id = process_id
                revised.behalf_name = behalf_name
                revised.behalf_position = behalf_position
                revised.dates = date
                revised.coment = comment
                revised.distribution_cost_center = distribution
                db.session.commit()

                
            elif nextTarget == "sent_email":
                comment = request_data.get('comment')

                proposed_position = Summary.query.filter_by(record_id = record_id).first()
                current_position = Employee.query.filter_by(id = proposed_position.employee_id).first()
                current_position.position_id = proposed_position.position_id
                db.session.commit()
                
                submit_data = {
                    "data": {
                        "comment": comment
                    }
                }   

                r = requests.post(os.getenv("BASE_URL_TASK") + "/" + task_id + "/submit", data = json.dumps(submit_data), headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % user_token
                })

            return "Submitted", 200
        else:
            return "Bad request", 400
    else:
        return "Methond Not Allowed", 405



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
