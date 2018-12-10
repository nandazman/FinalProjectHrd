/*
    Nanda


    Fadhiel
    

    Syifa


*/
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


function deleteCookie(){
    document.cookie = ' requester=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'
    document.cookie = ' token=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'
    document.cookie = ' hr=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'
    document.cookie = ' `proposedHr=; expires=Thu, 01 Jan 1970 00:00:00 UTC;'
    window.location = 'login.html'
}

function security(){
    var username = getCookie('token');
    if (username != ""){

    }else {
        alert('Please Login')
        document.cookie = 'requester=${isRequest}; expires=Thu, 01 Jan 1970 00:00:00 UTC;'
        window.location = 'login.html'
    }
}


/******* INTERACTION WITH BACK END ******/


function allTask(){
    
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/GetTask',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token')),
            req.setRequestHeader("Content-Type", "application/json");
        },
        dataType: 'json',
        success: function(res){
            
            var requester = res.data
            if (requester.length == 0){
                $('#alltaskuser').empty()
                $('#alltaskuser').append(`
                    <div class="taskitem")">
                        <h3>There is no task at the moment</h3>
                    </div>`)
            } else {
                $('#alltaskuser').empty()
                requester.forEach(task => {
                    
                    $('#alltaskuser').append(`
                        <div class="taskitem" onclick="commentHistory('${task.id}','${task.record_id}')">
                            <img src="source/man-user.png">
                            <p>Dear ${task.assignee.name}</p>
                            <p>${task.id}</p>
                        </div>`)
                })
            }
        },
        error: function(err){
            alert(err.response)
        }
    })
}

function submitTask(taskid,recordid,status){
    // 'behalf-name': $('#behalf-name').val(),
    // 'behalf-position' : $('#behalf-position').val(),
    // "distribution": $('#distribution-cost').val(),
    // "date": $('#date-start').val(),
    // "comment": $('#comment-requester').val()
    
    if ($('textarea').val() == ""){
        alert("Note must be inputted")
        return
    }

    if (getCookie('requester') == 'true' || getCookie('proposedHr') == 'true'){
        $.ajax({
            method: 'PUT',
            url: 'http://localhost:7000/submitTask',
            beforeSend: function(req) {
                req.setRequestHeader('Authorization', getCookie('token')),
                req.setRequestHeader("Content-Type", "application/json");
            },
            data: JSON.stringify({
                "taskid": taskid,
                "recordid": recordid,
                "status": status,
                'behalf-name': $('#behalf-name-revised').val(),
                'behalf-position' : $('#behalf-position-revised').val(),
                "distribution": $('#distribution-cost-revised').val(),
                "date": $('#date-start-revised').val(),
                "comment": $('textarea').val()
            }),
    
            success: function(res){
                
                $('#alltaskuser .taskitem p:contains("'+taskid+'")').parent().remove()
                $('#modal-form').slideUp()
                $('#revise').remove()
                $('#approve').remove()
                if ($('#alltaskuser').has('.taskitem').length == 0) {
                    $('#alltaskuser').append(`
                    <div class="taskitem")">
                        <h3>There is no task at the moment</h3>
                    </div>`)
                }
            },
            error: function(err){
                alert(err.response)
            }
        })
    } else if (getCookie('requester') !== 'true'){ 
        $.ajax({
            method: 'POST',
            url: 'http://localhost:7000/submitTask',
            beforeSend: function(req) {
                req.setRequestHeader('Authorization', getCookie('token')),
                req.setRequestHeader("Content-Type", "application/json");
            },
            data: JSON.stringify({
                "taskid": taskid,
                "recordid": recordid,
                "status": status,
                "comment": $('textarea').val()
            }),

            success: function(res){
                
                $('#alltaskuser .taskitem p:contains("'+taskid+'")').parent().remove()
                $('#modal-form').slideUp()
                $('#revise').remove()
                $('#approve').remove()
                if ($('#alltaskuser').has('.taskitem').length == 0) {
                    $('#alltaskuser').append(`
                        <div class="taskitem")">
                            <h3>There is no task at the moment</h3>
                        </div>`)
                }
            },
            error: function(err){
                alert(err.response)
            }
        })
    } 


}

function getProfile(){
    $.ajax({
        method: 'GET',
        url: 'http://localhost:7000/getProfile',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
        },
        success: function(res){
            
            data = JSON.parse(res)
            $('#user').append(`
                <div class="greeting">
                    Hello, ${data.nama}!
                    <div class="dropdown"> 
                        <img src="source/down.png">
                        <div class="dropdown-content">
                            <span onclick="deleteCookie()">Sign Out</span>
                        </div>
                    </div>
                </div>
            `)
            $('#new-information').prepend(`
                <div class="listForm">
                    <p>REQUESTER NAME</p>
                    <p id="requester-nama">${data.nama}</p>
                </div>
                <div class="listForm">
                    <p>REQUESTER NPK</p>
                    <p>${data.npk}</p>
                </div>
                <div class="listForm">
                    <p>REQUESTER POSITION</p>
                    <p>${data.role}</p>
                </div>
            `)

        $.ajax({
            method: 'GET',
            url: 'http://localhost:7000/employee',
            beforeSend: function(req) {
                req.setRequestHeader('Authorization', getCookie('token'));
            },
            success: function(res){
                
                data = JSON.parse(res)
                data.forEach(data=> {
                    $('#employee-selection').append(`
                        <option value="${data.position_id}">${data.npk} - ${data.nama}</option>
                    `)

                })
                
            }
        })
        },
        error: function(err){
            console.log(err)
        }
    })
}

function getEmployeeData(){
    // console.log($('#employee-selection').val())
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/current',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
            req.setRequestHeader("Content-Type", "application/json");
        },
        data: JSON.stringify({
            "id": $('#employee-selection').val()
        }),
        success: function(res){
            data = JSON.parse(res)
            $('#current').empty()
            $('#current').append(`
            <div class="listForm">
                <p>POSITION CODE</p>
                <p class="ans">${data.position_code}</p>
            </div>
            <div class="listForm">
                <p>POSITION</p>
                <p class="ans">${data.position}</p>
            </div>
            <div class="listForm">
                <p>COMPANY</p>
                <p class="ans">${data.company}</p>
            </div>
            <div class="listForm">
                <p>COST CENTER</p>
                <div>
                <p class="ans inans">${data.cost_center_code}</p>
                <p class="ans">${data.cost_center}</p>
                </div>
            </div>
            <div class="listForm">
                <p>PERSONAL AREA</p>
                <p class="ans">${data.personal_area}</p>
            </div>
            <div class="listForm">
                <p>EMPLOYEE GROUP</p>
                <p class="ans">${data.employee_group}</p>
            </div>
            <div class="listForm">
                <p>EMPLOYEE SUBGROUP</p>
                <p class="ans">${data.employee_sub_group}</p>
            </div>
            `)
            
            $.ajax({
                method: 'POST',
                url: 'http://localhost:7000/proposed',
                beforeSend: function(req) {
                    req.setRequestHeader("Content-Type", "application/json");
                },
                data: JSON.stringify({
                    "id": data.id
                }),
                success: function(res){
                    data = JSON.parse(res)
                    
                    $('#position-list').empty()
                    $('#position-list').append(`<option disabled selected>--Position--</option>`)
                    data.forEach(data=> {
                        $('#position-list').append(`
                            <option value="${data.id}">${data.position_code} - ${data.position}</option>
                        `)
    
                    })
                },
                error: function(err){
                    console.log(err)
                }
            })
        },
        error: function(err){
            console.log(err)
        }
    })
}

function getPositionData(){

    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/proposeddata',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
            req.setRequestHeader("Content-Type", "application/json");
        },
        data: JSON.stringify({
            "id": $('#position-list').val()
        }),
        success: function(res){
            
            data = JSON.parse(res)
            $('#position-data').empty()
            $('#position-data').append(`
                <div class="listForm">
                    <p>COST CENTER</p>
                    <div>
                        <input type="text" class="doubleinput1" value="${data.cost_center_code}"/><br>
                        <input type="text" class="doubleinput2" value="${data.cost_center}"/>
                    </div>
                </div>
                <div class="listForm">
                    <p>DISTRIBUTION COST CENTER</p>
                    <div>
                        <input type="text" id="distribution-cost" class="database-input" /><br>
                    </div>
                </div>
                <div class="listForm">
                    <p>COMPANY</p>
                    <input type="text" value="${data.company}"/>
                </div>
                <div class="listForm">
                    <p>PERSONNEL AREA</p>
                    <input type="text" value="${data.personal_area}"/>
                </div>
                <div class="listForm">
                    <p>PERSONNEL SUB AREA</p>
                    <input type="text" value="${data.personal_sub_area}"/>
                </div>
                <div class="listForm">
                    <p>EMPLOYEE TYPE</p>
                    <input type="text" value="${data.employee_type}"/>
                </div>
                <div class="listForm">
                    <p>RECEIVER <small id="help">(Position Minimum L4)</small></p>
                    <input type="text" id="receiver" value="${data.receiver}"/>
                </div>
                <div class="listForm">
                    <p>EFFECTIVE DATE START</p>
                    <input type="date" id="date-start" name="trip-start" value="yyyy-mm-dd" min="2018-01-01" max="2018-12-31">
                </div>
                <div class="listForm">
                    <p>COMMENT</p>
                    <input id="comment-requester" type="text" />
                </div>
            `)
          
        },
        error: function(err){
            console.log(err)
        }
    })
}

function submitForm(){
    
    document.getElementById('regForm').style.display = "none";

    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/submitRecord',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
            req.setRequestHeader("Content-Type", "application/json");
        },
        data: JSON.stringify({
            "employee": $('#employee-selection option:selected').text(),
            "receiver": $('#receiver').val(),
            "requester": $('#requester-nama').text(),
            "position": $('#position-list').val(),
            'behalf-name': $('#behalf-name').val(),
            'behalf-position' : $('#behalf-position').val(),
            "distribution": $('#distribution-cost').val(),
            "date": $('#date-start').val(),
            "comment": $('#comment-requester').val()
        }),
        success: function(res){
            console.log(res)
        },
        error: function(err){
            console.log(err)
        }
    })
}

function getSAP(){
    $.ajax({
        method: 'GET',
        url: 'http://localhost:7000/getSAP',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
        },
        success: function(res){
            response = JSON.parse(res)
            var i = 0
            response.forEach( (content) => {
                var data = content.last_submitted
                
                
                $('#comments').append(`
                    <div class="comment" id="commentator">
                        <p></p>
                        <p></p>
                        <p></p>
                        <p></p>
                        <p></p>
                        <p></p>
                    </div>
                `)
                
                $('.comment')[i].children[0].innerHTML = content.record_id.split("-")[2]
                if (data == "Requester"){

                }
                else if (typeof data == "object"){
                
                    // $('.comment')[0].children[1]
                    for(var j = 1; j <= data.length; j++){
                        $('.comment')[i].children[j].innerHTML = '<img src="source/checked.png">'
                    }
                } else if (data == "HR Company"){
                    
                    j = 1
                    k = 1
                    while( $('#histories').children()[k-1].innerHTML != data){
                        k++;
                        
                        if($('#histories').children()[k].innerHTML == data){
                            
                            $('.comment')[i].children[j+1].innerHTML = '<img src="source/checked.png">'
                        }
                        
                        j++;
                    }
                } else if (data != ""){
                   
                    j = 1
                    k = 1
                    
                    while( $('#histories').children()[k-1].innerHTML != data){
                        k++;
                    
                        $('.comment')[i].children[j].innerHTML = '<img src="source/checked.png">'
                        j++;
                    }   
                }
                i++;
            })
        },
        error: function(err){
            console.log(err)
        }
    })
}

function commentHistory(task_id,record_id){
    

    document.getElementById('modal-form').style.display = "block";
    $('#confirmation').append(`<button onclick="submitTask('${task_id}','${record_id}','Approved')" id="approve">Approved</button>`)
    if (getCookie('hr') != 'true' && getCookie('requester') != 'true'){
        $('#confirmation').append(`<button onclick="submitTask('${task_id}','${record_id}','Revised')" id="revise">Revised</button>`)
    }
    
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/tableSummary',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
            req.setRequestHeader("Content-Type", "application/json");
        },
        data: JSON.stringify({
            "taskid": task_id,
            "recordid": record_id 
            }),
        success: function(res){
            comment_histories = (JSON.parse(res)).comment_history
            formData = (JSON.parse(res)).form_data
            data_from_db = (JSON.parse(res)).comment_history_from_db
            console.log(data_from_db)
            $('#modal-requester').empty()
            $("#modal-requester").append(`
                <div class="modal-listForm">
                    <p>REQUESTER NAME</p>
                    <p class="ans">${formData.requester.name}</p>
                </div>
                <div class="modal-listForm">
                    <p>REQUESTER NPK</p>
                    <p class="ans">${formData.requester.npk}</p>
                </div>
                <div class="modal-listForm">
                    <p>REQUESTER POSITION</p>
                    <p class="ans">${formData.requester.position}</p>
                </div>
            `)
        if (getCookie('requester') == 'true'){
            $("#modal-requester").append(`
                <div class="modal-listForm">
                    <p>ON BEHALF NAME</p>
                    <input type="text" class="ans" value="${formData.behalf.behalf_name}" id="behalf-name-revised">
                </div>
                <div class="modal-listForm">
                    <p>ON BEHALF POSITION</p>
                    <input type="text" class="ans" value="${formData.behalf.behalf_position}" id="behalf-position-revised">
                </div>
            `)
        } else if(getCookie('requester') !== 'true'){
            $("#modal-requester").append(`
                <div class="modal-listForm">
                    <p>ON BEHALF NAME</p>
                    <p class="ans">${formData.behalf.behalf_name}</p>
                </div>
                <div class="modal-listForm">
                    <p>ON BEHALF POSITION</p>
                    <p class="ans">${formData.behalf.behalf_position}</p>
                </div>
            `)
        }
        
        $("#modal-requester").append(`
            <div class="modal-listForm">
                <p>EMPLOYEE</p>
                <div>
                    <p class="ans inans">${formData.employee.employee_name}</p>
                    <p class="ans">${formData.employee.employee_npk}</p>
                </div>
            </div>
            <div class="modal-listForm">
                <p>RECORD ID</p>
                <p class="ans">${formData.record_id}</p>
            </div>
        `)

        $('#modal-current').empty()
        $('#modal-current').append(`
            <div class="modal-listForm">
                <p>POSITION CODE</p>
                <p class="ans">${formData.current.position_code}</p>
            </div>
            <div class="modal-listForm">
                <p>POSITION</p>
                <p class="ans">${formData.current.position}</p>
            </div>
            <div class="modal-listForm">
                <p>COMPANY</p>
                <p class="ans">${formData.current.company}</p>
            </div>
            <div class="modal-listForm">
                <p>COST CENTER</p>
                <div>
                    <p class="ans inans">${formData.current.cost_center_code}</p>
                    <p class="ans">${formData.current.cost_center}</p>
                </div>
            </div>
            <div class="modal-listForm">
                <p>PERSONAL AREA</p>
                <p class="ans">${formData.current.personal_area}</p>
            </div>
            <div class="modal-listForm">
                <p>EMPLOYEE GROUP</p>
                <p class="ans">${formData.current.employee_group}</p>
            </div>
            <div class="modal-listForm">
                <p>EMPLOYEE SUBGROUP</p>
                <p class="ans">${formData.current.employee_sub_group}</p>
            </div>
        `)

        $('#modal-proposed').empty()
        $('#modal-proposed').append(`
            <div class="modal-listForm">
                <p>POSITION CODE</p>
                <p class="ans">${formData.proposed.position_code}</p>
            </div>
            <div class="modal-listForm">
                <p>POSITION</p>
                <p class="ans">${formData.proposed.position}</p>
            </div>
            <div class="modal-listForm">
                <p>COST CENTER</p>
                <div>
                    <p class="ans inans">${formData.proposed.cost_center_code}</p>
                    <p class="ans">${formData.proposed.cost_center}</p>
                </div>
            </div>
        `)
        if (getCookie('requester') == 'true'){
            $("#modal-proposed").append(`
                <div class="modal-listForm">
                    <p>DISTRIBUTION COST CENTER</p>
                    <input type="text" value="${formData.proposed.distribution_cost_center}" id="distribution-cost-revised">
                </div>`)
        } else if(getCookie('requester') !== 'true'){
            $("#modal-proposed").append(`
                <div class="modal-listForm">
                    <p>DISTRIBUTION COST CENTER</p>
                    <p class="ans">${formData.proposed.distribution_cost_center}</p>
                </div>`)
        }
        $("#modal-proposed").append(`
            <div class="modal-listForm">
                <p>COMPANY</p>
                <p class="ans">${formData.proposed.company}</p>
            </div>
            <div class="modal-listForm">
                <p>PERSONAL AREA</p>
                <p class="ans">${formData.proposed.personal_area}</p>
            </div>
            <div class="modal-listForm">
                <p>PERSONAL SUB AREA</p> 
                <p class="ans">${formData.proposed.personal_sub_area}</p>
            </div>
            <div class="modal-listForm">
                <p>EMPLOYEE TYPE</p>
                <p class="ans">${formData.proposed.type}</p>
            </div>
            <div class="modal-listForm">
                <p>RECEIVER</p>
                <p class="ans">${formData.receiver}</p>
            </div>`)
        if (getCookie('requester') == 'true'){
            $("#modal-proposed").append(`
                <div class="modal-listForm">
                    <p>EFFECTIVE DATE START</p>
                    <input type="date" value="${formData.date}" id="date-start-revised">
                </div>`)
        } else if(getCookie('requester') !== 'true'){
            $("#modal-proposed").append(`
                <div class="modal-listForm">
                    <p>EFFECTIVE DATE START</p>
                    <p class="ans">${formData.date}</p>
                </div>`)
        }
        $("#modal-proposed").append(`
            <div class="modal-listForm">
                <p>COMMENT</p>
                <p class="ans">${formData.comment}</p>
            </div>
            <div class="modal-listForm">
                <p>NOTE</p>
                <textarea rows="5" cols="30" id="comment"></textarea>
            </div>`)

        
        $('#comment-hismodal').empty()
        $('#comment-hismodal').append(`
            <div class="headercomment">
                <h4>COMMENT-HISTORY</h4>
            </div>
            <div class="his-modal">
                <p>Participant</p>
                <p>Name</p>
                <p>Position</p>
                <p>Activity</p>
                <p>Started</p>
                <p>Completed</p>
                <p>Response</p>
                <p>Comment</p>
            </div>
        `)
        var j = -1
        for(var i = 2; i <= comment_histories.data.length; i+= 2){
            console.log(comment_histories)
            j++;
            console.log(i)
            if (i == comment_histories.data.length){
                i--;
            }
            if (comment_histories.data[i].name == "Task completed"){
                var date_started = new Date(comment_histories.data[i-1].published);
                var date_finished = new Date(comment_histories.data[i].published)
            $('#comment-hismodal').append(`
                <div class="comment-modal">
                    <p>XXX</p>
                    <p>${comment_histories.data[i].actor.display_name}</p>
                    <p>${data_from_db[comment_histories.data[i].actor.display_name].position}</p>
                    <p>${data_from_db[comment_histories.data[i].actor.display_name].activity}</p>
                    <p>${date_started.toLocaleString()}</p>
                    <p>${date_finished.toLocaleString()}</p>
                    <p>Approved</p>
                    <p>${comment_histories.data[i].target.content}</p>
                </div>
            `)
                if (comment_histories.data[i].actor.display_name == "Rudi Sejahtera" ){
                    $('.comment-modal')[j].children[6].innerHTML = "Proposed"
                }
            }
            // If both hr havent approved
            else if (comment_histories.data[i].name == "Task assigned" && comment_histories.data[i-1].name == "Task assigned" && i + 1 == comment_histories.data.length){
                var date_started1 = new Date(comment_histories.data[i-1].published)
                var date_started2 = new Date(comment_histories.data[i].published)
                alert("ini hr belum approve")
               $('#comment-hismodal').append([
                   `<div class="comment-modal">
                        <p>XXX</p>
                        <p>${comment_histories.data[i-1].object.display_name}</p>
                        <p>${data_from_db[comment_histories.data[i-1].object.display_name].position}</p>
                        <p>${data_from_db[comment_histories.data[i-1].object.display_name].activity}</p>
                        <p>${date_started1.toLocaleString()}</p>
                        <p>Waiting</p>
                        <p>Waiting</p>
                        <p>Waiting</p>
                    </div>`,
                    `<div class="comment-modal">
                        <p>XXX</p>
                        <p>${comment_histories.data[i].object.display_name}</p>
                        <p>${data_from_db[comment_histories.data[i].object.display_name].position}</p>
                        <p>${data_from_db[comment_histories.data[i].object.display_name].activity}</p>
                        <p>${date_started2.toLocaleString()}</p>
                        <p>Waiting</p>
                        <p>Waiting</p>
                        <p>Waiting</p>
                    </div>`
                ])
            }
            // if task assigend to anyone but first two hr
            else if (comment_histories.data[i].name == "Task assigned" && i + 1 == comment_histories.data.length){
                var date_started = new Date(comment_histories.data[i].published)
                $('#comment-hismodal').append(
                    `<div class="comment-modal">
                         <p>XXX</p>
                         <p>${comment_histories.data[i].object.display_name}</p>
                         <p>${data_from_db[comment_histories.data[i].object.display_name].position}</p>
                         <p>${data_from_db[comment_histories.data[i].object.display_name].activity}</p>
                         <p>${date_started.toLocaleString()}</p>
                         <p>Waiting</p>
                         <p>Waiting</p>
                         <p>Waiting</p>
                     </div>`)
            }
            // if one hr have approved
            else if (comment_histories.data[i+1].name == "Task completed" && i + 2 == comment_histories.data.length){
                var date_started1 = new Date(comment_histories.data[i-1].published)
                var date_started2 = new Date(comment_histories.data[i].published)
                var completed_name = comment_histories.data[i+1].actor.display_name
                var completed_date = new Date(comment_histories.data[i+1].published)

                $('#comment-hismodal').append([
                    `<div class="comment-modal">
                        <p>XXX</p>
                        <p>${comment_histories.data[i-1].object.display_name}</p>
                        <p>${data_from_db[comment_histories.data[i-1].object.display_name].position}</p>
                        <p>${data_from_db[comment_histories.data[i-1].object.display_name].activity}</p>
                        <p>${date_started1.toLocaleString()}</p>
                        <p>Waiting</p>
                        <p>Waiting</p>
                        <p>Waiting</p>
                    </div>`,
                    `<div class="comment-modal">
                        <p>XXX</p>
                        <p>${comment_histories.data[i].object.display_name}</p>
                        <p>${data_from_db[comment_histories.data[i].object.display_name].position}</p>
                        <p>${data_from_db[comment_histories.data[i].object.display_name].activity}</p>
                        <p>${date_started2.toLocaleString()}</p>
                        <p>${completed_date.toLocaleString()}</p>
                        <p>Approved</p>
                        <p>${comment_histories.data[i+1].target.content}</p>
                    </div>`
                    ])
                break;
            }
            // if both hr approved
            else if (comment_histories.data[i+1].name == "Task completed" && comment_histories.data[i+2].name == "Task completed"){
                var first_hr = comment_histories.data[i-1].object.display_name
                var second_hr = comment_histories.data[i].object.display_name
                var first_complete = comment_histories.data[i+1].actor.display_name
                var second_complete = comment_histories.data[i+2].actor.display_name
                var date_started1 = new Date(comment_histories.data[i-1].published)
                var date_started2 = new Date(comment_histories.data[i].published)
                var date_finished1 = new Date(comment_histories.data[i+1].published)
                var date_finished2 = new Date(comment_histories.data[i+2].published)
                if (first_hr == first_complete){
                    $('#comment-hismodal').append([
                        `<div class="comment-modal">
                            <p>XXX</p>
                            <p>${first_hr}</p>
                            <p>${data_from_db[first_hr].position}</p>
                            <p>${data_from_db[first_hr].activity}</p>
                            <p>${date_started1.toLocaleString()}</p>
                            <p>${date_finished1.toLocaleString()}</p>
                            <p>Approved</p>
                            <p>${comment_histories.data[i+1].target.content}</p>
                        </div>`,
                        `<div class="comment-modal">
                            <p>XXX</p>
                            <p>${second_hr}</p>
                            <p>${data_from_db[second_hr].position}</p>
                            <p>${data_from_db[second_hr].activity}</p>
                            <p>${date_started2.toLocaleString()}</p>
                            <p>${date_finished2.toLocaleString()}</p>
                            <p>Approved</p>
                            <p>${comment_histories.data[i+2].target.content}</p>
                        </div>`
                        ])
                } 
                else if (first_hr == second_complete){
                    $('#comment-hismodal').append([
                        `<div class="comment-modal">
                            <p>XXX</p>
                            <p>${first_hr}</p>
                            <p>${data_from_db[first_hr].position}</p>
                            <p>${data_from_db[first_hr].activity}</p>
                            <p>${date_started1.toLocaleString()}</p>
                            <p>${date_finished2.toLocaleString()}</p>
                            <p>Approved</p>
                            <p>${comment_histories.data[i+2].target.content}</p>
                        </div>`,
                        `<div class="comment-modal">
                            <p>XXX</p>
                            <p>${second_hr}</p>
                            <p>${data_from_db[second_hr].position}</p>
                            <p>${data_from_db[second_hr].activity}</p>
                            <p>${date_started2.toLocaleString()}</p>
                            <p>${date_finished1.toLocaleString()}</p>
                            <p>Approved</p>
                            <p>${comment_histories.data[i+1].target.content}</p>
                        </div>`
                        ])
                }
                i +=2;
                j++;
                
            }
            
        }
        

        },
        error: function(err){
            console.log(err)
        }
    })
}

function getOneRecordId(){
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/',
        beforeSend: function(req) {
            req.setRequestHeader("Content-Type", "application/json");
            req.setRequestHeader('Authorization', getcookie('token'));
        },
        data: JSON.stringify({
            "record_id": document.getElementById('record_id').value
        }),
        success: function(res){
            console.log(res)
        },
        error: function(err){
            console.log(err)
        }
    })
}

function getTableSummary(){
    $.ajax({
        method: 'GET',
        url: 'http://localhost:7000/',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getcookie('token'));
        },
        success: function(res){
            console.log(res)
        },
        error: function(err){
            console.log(err)
        }
    })
}


/****** FOR INTERACRTION IN FRON END ******/
if (getCookie('requester') !== 'true'){
    $("#request-tab").hide()
    $("#commenthis").hide()
    $("#form-input").hide()
    
}


$(document).ready(function () {
    $("#request-tab").click(function () {
        $("#regForm").slideToggle();
        $(".second-box").slideUp();
        
    });
});

$(document).ready(function () {
    $("#commenthis").click(function () {
        $(".second-box").slideToggle();
        $("#regForm").slideUp();
    });
});


document.getElementById("close").onclick = function () {
    document.getElementById('modal-form').style.display = "none";
    document.getElementById('approve').remove()
    if (getCookie('hr') != 'true'){
        document.getElementById('revise').remove()
    }
}

window.onclick = function (event) {
    if (event.target == document.getElementById('modal-form')) {
        document.getElementById('modal-form').style.display = "none";
        document.getElementById('approve').remove()
        if (getCookie('hr') != 'true' && getCookie('requester') !== 'true'){
            document.getElementById('revise').remove()
        }
    }
}

