from flask import Flask, request, json, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from requests.utils import quote
import datetime
import os
import jwt
import requests
from sqlalchemy import and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hahaha123@localhost:5432/DatabaseHR'
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

#### Route for log in ###
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        requestData = request.get_json()
        reqEmail = requestData.get('email')
        reqPassword = requestData.get('password')
        userDB = AccessUser.query.filter_by(email=reqEmail, password=reqPassword).first()

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

### Route for get current user data ###
@app.route('/user-profile', methods = ["GET"])
def profile():
    if request.method == 'GET':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email=decoded['email']).first()

        if user is not None:
            position = Position.query.filter_by(id=user.position_id).first()

            user_nama = {
                "nama": user.nama,
                "npk": user.npk,
                "role": position.position,
                "departemen_id": position.departemen_id
            }
            user = json.dumps(user_nama)

            return user, 200
        
        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

### Route for get all employee list for current department ###
@app.route('/employee-list', methods = ["GET"])
def employee():
    if request.method == 'GET':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email=decoded['email']).first()

        if user is not None:
            ### get posiiton for current user ###
            position = Position.query.filter_by(id=user.position_id).first()
            departmentManager = position.departemen_id
            employeeDB = Employee.query.all()

            employeeData = []

            for data in employeeDB:
                ### get department id for employee ###
                departmentEmployee = (Position.query.filter_by(id=data.position_id).first()).departemen_id
                ### take employee data if departmen id managaer is the same with department id employee ###
                if departmentManager == departmentEmployee:
                    employee = {
                        'npk': data.npk,
                        'nama': data.nama,
                        'position_id': data.position_id
                    }
                    employeeData.append(employee)

            employeesData = json.dumps(employeeData)

            return employeesData, 200

        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

### route for get selected employee data ###
@app.route('/current-employee-data', methods = ['POST'])
def currentEmployeeData():
    if request.method == 'POST':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email=decoded['email']).first()

        if user is not None:
            requestData = request.get_json()
            positionId = requestData['id']
            positionData = Position.query.filter_by(id=positionId).first()
            ### Get employee data ###
            employee = {
                'id': positionData.id,
                'position_code': positionData.position_code,
                'position': positionData.position,
                'company': positionData.company,
                'cost_center': positionData.cost_center,
                'cost_center_code': positionData.cost_center_code,
                'personal_area': positionData.personal_area,
                'employee_group': positionData.employee_group,
                'employee_sub_group': positionData.employee_sub_group
            }

            data = json.dumps(employee)
            
            return data, 200

        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

### route for get list of position in proposed department ###
@app.route('/proposed-position-list', methods = ['POST'])
def proposedPositionList():
    if request.method == 'POST':
        requestData = request.get_json()
        positionId = requestData['id']
        positionData = Position.query.filter_by(id = positionId).first()
        ### Get position list that doesnt have the same position and departmen id  with current user
        ### and main company position
        positionList = Position.query.filter(and_(Position.id != positionData.id, Position.departemen_id != positionData.departemen_id, Position.departemen_id != 1)).all()
        positions = []

        for data in positionList:
            position = {
                'id': data.id,
                'position_code': data.position_code,
                'position': data.position
            }
            positions.append(position)

        data = json.dumps(positions)

        return data, 200
    else:
        return "Method not allowed", 405

### Route for get selected proposed position data ###
@app.route('/proposed-position-data', methods = ['POST'])
def proposedPositionData():
    if request.method == 'POST':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email=decoded['email']).first()

        if user is not None:
            requestData = request.get_json()
            positionId = requestData['id']
            positionData = Position.query.filter_by(id = positionId).first()
            
            ### Get receiver data in proposed department ###
            receiver = AccessUser.query.join(Position).filter(Position.departemen_id == positionData.departemen_id).first()
            receiverEmail = receiver.email
            receiverId = receiver.id
            print(receiver)
            employee = {
                'id': positionData.id,
                'position_code': positionData.position_code,
                'position': positionData.position,
                'company': positionData.company,
                'cost_center': positionData.cost_center,
                'cost_center_code': positionData.cost_center_code,
                'personal_area': positionData.personal_area,
                'personal_sub_area': positionData.personal_sub_area,
                'employee_type': positionData.employee_type,
                'receiver': receiverEmail,
                'receier_id': receiverId
            }

            data = json.dumps(employee)
            
            return data, 200
        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

### route for get request summary data and comment history data ###
@app.route('/request-summary-and-comment-history', methods = ["POST"])
def requestSummaryDataAndCommentHistory():
    if request.method == 'POST':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        userDB = AccessUser.query.filter_by(email=decoded['email']).first()

        if userDB is not None:
            requestData = request.get_json()
            recordId = requestData['recordid']
            summaryData = Summary.query.filter_by(record_id = recordId).first()
            
            # GET requester data
            requesterData = AccessUser.query.join(Position).add_columns(AccessUser.nama, AccessUser.npk, Position.position).filter(AccessUser.id == summaryData.requester_id).first()
            # GET receiver data
            receiverData = AccessUser.query.filter_by(id = summaryData.receiver_id).first()
            # GET employee data
            employeeData = Employee.query.join(Position).add_columns(Employee.nama, Employee.npk, Position.position_code, Position.position, Position.company, Position.cost_center, Position.cost_center_code, Position.personal_area, Position.employee_group, Position.employee_sub_group).filter(Employee.id == summaryData.employee_id).first()
            # GET target position
            proposedPosition = Position.query.filter_by(id = summaryData.position_id).first()
            # Summary data and comment history
            summary = {
                'requester': {
                    'name': requesterData[1],
                    'npk': requesterData[2],
                    'position': requesterData[3]
                },
                'behalf': {
                    'behalf_name': summaryData.behalf_name,
                    'behalf_position': summaryData.behalf_position
                },
                'employee': {
                    'employee_name': employeeData[1],
                    'employee_npk': employeeData[2]
                },
                'record_id': summaryData.record_id,
                'current': {
                    'position_code': employeeData[3],
                    'position': employeeData[4],
                    'company': employeeData[5],
                    'cost_center_code': employeeData[7],
                    'cost_center': employeeData[6],
                    'personal_area': employeeData[8],
                    'employee_group': employeeData[9],
                    'employee_sub_group': employeeData[10]
                },
                'proposed': {
                    'position_code': proposedPosition.position_code,
                    'position': proposedPosition.position,
                    'distribution_cost_center': summaryData.distribution_cost_center,
                    'company': proposedPosition.company,
                    'cost_center_code': proposedPosition.cost_center_code,
                    'cost_center': proposedPosition.cost_center,
                    'personal_area': proposedPosition.personal_area,
                    'personal_sub_area': proposedPosition.personal_sub_area,
                    'type': proposedPosition.employee_type
                },
                'receiver': receiverData.nama,
                'date': summaryData.dates,
                'comment': summaryData.coment
            }
        
            userToken = userDB.token
            user = AccessUser.query.join(Position).order_by(AccessUser.id).add_columns(AccessUser.role, AccessUser.nama, Position.position).all()
            
            positions = {}
            activities = ['Prepare Rotation', 'HRCS Verification', 'MAIN HR Verification', 'SM Approval', 'MBD Approval', 'HRBD Verification']
            i = 0
            ### give activites for every access  user ###
            for data in user:
                positions[data[2]] = {
                    'position' : data[3],
                    'activity': activities[i]
                }
                i = i +1

            ### GET comment history from nextflow ###
            r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + requestData['recordid'] + "/stageview", headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
                })

            result = json.loads(r.text)
            
            ### Put form data and comment history in one variable to send to Front End ###
            summarize = {
                'form_data': summary,
                'comment_history': result,
                'comment_history_from_db': positions
            }
            
            summarize = json.dumps(summarize)
            return summarize , 200
        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

@app.route('/SAP-list', methods = ["GET"])
def get_SAP():
    if request.method == 'GET':
        flowBefore = {
            'Department Manager': ['HR Department', 'HR Company'],
            'Senior Manager ': 'Department Manager',
            'Proposed HR Department': 'Senior Manager'
        }
        
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email = decoded['email']).first()

        if user is not None:
            SAP = Summary.query.all()
            userToken = user.token
            allSAP = []

            for data in SAP:
                r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + data.record_id + "/stageview", headers = {
                        "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
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
                        'last_submitted' : flowBefore[result['data'][-1]['target']['display_name']],
                        'record_id' : data.record_id
                    }

                allSAP.append(data)
            SAP = json.dumps(allSAP)

            return SAP, 200
        else:
            return "You have to logged in", 400
    else:
        return "Mehtod not allowed", 405
        
### route for submit new record ###
@app.route('/submit-record', methods = ['GET', 'POST'])
##### initiate nextflow or create record #####
def createRecord():
    if request.method == 'POST':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        requestData = request.get_json()
        reqComment = requestData.get('comment')

        user = AccessUser.query.filter_by(email = decoded['email']).first()

        if user is not None:
            userToken = user.token
            ### template for create recrod ###
            recordInstance = {
                "data": {
                    "definition": {
                        ### mosaic bla bla records ###
                        "id" : os.getenv('DEFINITION_ID')
                    }
                }
            }

            ### create record to get record id ###
            r = requests.post(os.getenv("BASE_URL_RECORD"), data = json.dumps(recordInstance), headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
            })

            ### result from create record ###
            result = json.loads(r.text)
            recordId = result['data']['id']

            ### submit flow using record id and token ###
            submitRecord(recordId, userToken, requestData)

            return "Submitted", 200

        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

### function to submit record ###
def submitRecord(recordId, userToken,request):
    ### template for submit record ###
    recordInstance = {
        "data": {
            "form_data": {
                ### every user in the flow ###
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

    requestData = json.dumps(recordInstance)

    ### Submit record to nexflow ###
    r = requests.post(os.getenv("BASE_URL_RECORD") + "/" + recordId + "/submit", data = requestData, headers = {
            "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
        })

    result = json.loads(r.text)
    ### function to submit to database ###
    submitToDatabase(recordId, "null",request)

    return "submitted", 200

### insert to db funtion ###
def submitToDatabase(recordId, processId, requestData):
    ### get data from front end ###
    employeeData = requestData.get('employee')
    receiver = requestData.get('receiver')
    requester = requestData.get('requester')
    positionId = int(requestData.get('position'))
    behalfName = requestData.get('behalf-name')
    behalfPosition = requestData.get('behalf-position')
    distribution = requestData.get('distribution')
    date = requestData.get('date')
    comment = requestData.get('comment')
    employeeName = employeeData.split(" - ")[1]

    ### get ID for current employee requester and receiver ###
    employeeId = (Employee.query.filter_by(nama = employeeName).first()).id
    requesterId = (AccessUser.query.filter_by(nama = requester).first()).id
    receiverId = (AccessUser.query.filter_by(email = receiver).first()).id

    #### template for submit to database ###
    dataDb = Summary(
        process_id = processId,
        record_id = recordId,
        distribution_cost_center = distribution,
        dates = date,
        coment = comment,
        behalf_name = behalfName,
        behalf_position = behalfPosition,
        requester_id = requesterId,
        receiver_id = receiverId,
        employee_id = employeeId,
        position_id = positionId
    )
    
    db.session.add(dataDb)
    db.session.commit()

    return "Submitted"

### route for get all task list ###
@app.route('/task-list', methods = ['GET', 'POST'])
#### Get access user task ####
def getAllTask():
    if request.method == 'POST':
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email = decoded['email']).first()
        
        if user is not None:
            userToken = user.token
            name = user.role
            query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s" % (name, os.getenv("DEFINITION_ID"))
            print(userToken)
            url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
            
            ### get every task list ###
            r = requests.get(url , headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
            })

            result = json.loads(r.text)
            print(result)

            return json.dumps(result), 200
        else:
            return "You have to logged in", 400
    else:
        return "Method not allowed", 405

### route to submit task by current user ###
@app.route('/submit-task', methods = ['GET', 'POST','PUT'])
### Submit task by User ###
def submitTask():
    currentToTarget = {
        "HR Department": "Germen_hrd@makersinsitute.id",
        "HR Company": "Germen_hrd@makersinsitute.id",
        "Department Manager": "status_revise",
        "Senior Manager ": "status_revise",
        "Proposed HR Department": "sent_email",
        "Requester": ["Hader_hrd@makersinstitute.id","Haper_hrd@makersinstitute.id"]
    }

    if request.method == "POST":
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email = decoded['email']).first()
        userToken = user.token

        if user is not None:
            requestData = request.get_json()
            taskId = requestData.get('taskid')
            recordId = requestData.get('recordid')
            status = requestData.get('status')
            comment = requestData.get('comment')

            r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + recordId + "/stageview", data = requestData, headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
                })

            result = json.loads(r.text)
            
            # get manager email and task id
            for data in result['data']:
                # not all array have target display_name
                try:
                    if data['target']['id'] == taskId:
                        currentUserTask = data['target']['display_name']
                        break
                except KeyError:
                    continue
            
            nextTarget = currentToTarget[currentUserTask]

            if nextTarget == "Germen_hrd@makersinsitute.id":
                submitData = {
                    "data": {
                        "form_data": {
                            # ini ngirim ke siapa aja
                            "pvDeptman": nextTarget
                        },
                        "comment": comment
                    }
                }
            elif nextTarget == "status_revise":
                submitData = {
                    "data": {
                        "form_data": {
                            # ini ngirim ke siapa aja
                            "pvAction": status
                        },
                        "comment": comment
                    }
                }
            

            r = requests.post(os.getenv("BASE_URL_TASK") + "/" + taskId + "/submit", data = json.dumps(submitData), headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
            })
          
            return "Submitted", 200

        else:
            return "Bad request", 400

    elif request.method == "PUT":
        decoded = jwt.decode(request.headers["Authorization"], 'tralala', algorithms=['HS256'])
        user = AccessUser.query.filter_by(email = decoded['email']).first()
        userToken = user.token
        
        if user is not None:
            requestData = request.get_json()
            taskId = requestData.get('taskid')
            recordId = requestData.get('recordid')
            

            r = requests.get(os.getenv("BASE_URL_RECORD") + "/" + recordId + "/stageview", data = requestData, headers = {
                "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
            })

            result = json.loads(r.text)
            
            # get manager email dan task id 
            for data in result['data']:
                # not all array have target display_name
                try:
                    if data['target']['id'] == taskId:
                        currentUserTask = data['target']['display_name']
                        break
                except KeyError:
                    continue
            
            nextTarget = currentToTarget[currentUserTask]

            if nextTarget[0] ==  "Hader_hrd@makersinstitute.id":
                behalfName = requestData.get('behalf-name')
                behalfPosition = requestData.get('behalf-position')
                distribution = requestData.get('distribution')
                date = requestData.get('date')
                comment = requestData.get('comment')

                submitData = {
                    "data": {
                        "form_data": {
                            # ini ngirim ke siapa aja
                            "pvHrdept": nextTarget[0],
                            "pvHrcomp": nextTarget[1]
                        },
                        "comment": comment
                    }
                }

                r = requests.post(os.getenv("BASE_URL_TASK") + "/" + taskId + "/submit", data = json.dumps(submitData), headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
                })

                response = json.loads(r.text)
                
                processId = response['data']['process_id']

                revised = Summary.query.filter_by(record_id = recordId).first()
                revised.process_id = processId
                revised.behalf_name = behalfName
                revised.behalf_position = behalfPosition
                revised.dates = date
                revised.coment = comment
                revised.distribution_cost_center = distribution
                db.session.commit()

                
            elif nextTarget == "sent_email":
                comment = requestData.get('comment')
                ### change the position after all user approve ###
                proposedPosition = Summary.query.filter_by(record_id = recordId).first()
                currentPosition = Employee.query.filter_by(id = proposedPosition.employee_id).first()
                currentPosition.position_id = proposedPosition.position_id
                db.session.commit()
                
                submitData = {
                    "data": {
                        "comment": comment
                    }
                }   

                r = requests.post(os.getenv("BASE_URL_TASK") + "/" + taskId + "/submit", data = json.dumps(submitData), headers = {
                    "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
                })

            return "Submitted", 200
        else:
            return "You have to logged in", 400
    else:
        return "Methond Not Allowed", 405

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT"))
