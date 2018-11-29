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
                $('#alltaskuser').append(`<div class="taskitem")">
                <h3>There is no task at the moment</h3>
            </div>`)
            } else {
                requester.forEach(task => {
                    
                    $('#alltaskuser').append(`<div class="taskitem" onclick="commentHistory('${task.id}','${task.record_id}')">
                    <img src="image1.jpg">
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
            "comment": "mantap approve"
        }),

        success: function(res){
            
            $('#alltaskuser .taskitem p:contains("'+taskid+'")').parent().remove()
            $('#modal-form').slideUp()
            $('#revise').remove()
            $('#approve').remove()
            // var requester = res.data
            // requester.forEach(task => {
            //     $('#alltaskuser').append(`<div class="taskitem" onclick="showModal('${task.id}')">
            //     <img src="image1.jpg">
            //     <p>Dear ${task.assignee.name}</p>
            //     <p>${task.id}</p>
            // </div>`)
            
            // })
        },
        error: function(err){
            alert(err.response)
        }
    })
}

// Menangkal Asyncrhonousnya AJAX
// $.when(
//     $.ajax({

//     }),
//     $.ajax({

//     })
// ).done(function(hasilAjax1, hasilAjax2){
    
// })



function getProfile(){
    $.ajax({
        method: 'GET',
        url: 'http://localhost:7000/getProfile',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
        },
        success: function(res){
            
            data = JSON.parse(res)
            $('#user').append(`<div class="greeting">Hello,<div class="dropdown"> 
            <span>${data.nama}</span>
            <div class="dropdown-content">
            <span onclick="deleteCookie()">Sign Out</span>
            </div>
            </div>!
            </div>`)
            $('#new-information').prepend(`<div class="listForm">
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
        </div>`)
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
            alert(data.id)
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
           
            $('#proposed').append(`<div class="listForm">
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
        </div>`)
          
        },
        error: function(err){
            console.log(err)
        }
    })
}


function submitForm(){
    
    document.getElementById('regForm').style.display = "none";
    employee = $('#employee-selection option:selected').text()
    receiver = $('#receiver').val()
    requester = $('#requester-nama').text()
    position = $('#position-list').val()
    behalf = $('#behalf-position').val()
   

    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/submitToHRD',
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
            response.forEach( (data) => {

                
                $('#comments').append(`<div class="comment" id="commentator">
                <p>Record ID</p>
                <p></p>
                <p></p>
                <p></p>
                <p></p>
                <p></p>
            </div>`)
                if (data == "Requester"){

                }
                else if (typeof data == "object"){
                
                    // $('.comment')[0].children[1]
                    for(var j = 1; j <= data.length; j++){
                        $('.comment')[i].children[j].innerHTML = '<img src="checked.png">'
                    }
                } else if (data == "HR Company"){
                    
                    j = 1
                    k = 1
                    while( $('#histories').children()[k-1].innerHTML != data){
                        k++;
                        
                        if($('#histories').children()[k].innerHTML == data){
                            
                            $('.comment')[i].children[j+1].innerHTML = '<img src="checked.png">'
                        }
                        
                        j++;
                    }
                } else {
                   
                    j = 1
                    k = 1
                    console.log("BATAS")
                    while( $('#histories').children()[k-1].innerHTML != data){
                        k++;
                        console.log($('#histories').children()[k-1].innerHTML)
                        console.log(data)
                        $('.comment')[i].children[j].innerHTML = '<img src="checked.png">'
                        j++;
                    }
                    
                    
                }
                i++;
            })
            // GET header table
            // $('#histories').children()[1].innerHTML

            // $('#comments').children()[1].innerHTML

        },
        error: function(err){
            console.log(err)
        }
    })
}


function commentHistory(task_id,record_id){
    alert("summary")

    document.getElementById('modal-form').style.display = "block";
    $('#confirmation').append(`<button onclick="submitTask('${task_id}','${record_id}','Approved')" id="approve">Approved</button>`)
    if (getCookie('hr') != 'true'){
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
            console.log(comment_histories)
            
            console.log("AAAAAAAAAAA")
            console.log(formData)

            $("#modal-requester").append(`<div class="modal-listForm">
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
        <div class="modal-listForm">
            <p>ON BEHALF NAME</p>
            <p class="ans">${formData.behalf.behalf_name}</p>
        </div>
        <div class="modal-listForm">
            <p>ON BEHALF POSITION</p>
            <p class="ans">${formData.behalf.behalf_position}</p>
        </div>
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
        </div>`)

        $('#modal-current').append(`<div class="modal-listForm">
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
        </div>`)

        $('#modal-proposed').append(`<div class="modal-listForm">
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
        <div class="modal-listForm">
            <p>DISTRIBUTION COST CENTER</p>
            <p class="ans">${formData.proposed.distribution_cost_center}</p>
        </div>
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
            <p class="ans">${formData.proposed_personal_sub_area}</p>
        </div>
        <div class="modal-listForm">
            <p>EMPLOYEE TYPE</p>
            <p class="ans">${formData.proposed.type}</p>
        </div>
        <div class="modal-listForm">
            <p>RECEIVER</p>
            <p class="ans">${formData.receiver}</p>
        </div>
        <div class="modal-listForm">
            <p>EFFECTIVE DATE START</p>
            <p class="ans">${formData.date}</p>
        </div>
        <div class="modal-listForm">
            <p>COMMENT</p>
            <p class="ans">${formData.comment}</p>
        </div>
        <div class="modal-listForm">
            <p>NOTE</p>
            <textarea rows="5" cols="30"></textarea>
        </div>`)

        var i;
        for(i = 1; i < comment_histories.data.length; i+=2 ){
            $('.comment-hismodal').append(`
            <div class="comment-modal">
                <p>XXX</p>
                <p>${comment_histories.data[i].object.display_name}</p>
                <p>XXX</p>
                <p>XXX</p>
                <p>${comment_histories.data[i].published}</p>
                <p>${comment_histories.data[i+1].published}</p>
                <p>XXX</p>
                <p>XXX</p>
            </div>`)
            if (i == 3){
                i ++;
                $('.comment-hismodal').append(`
            <div class="comment-modal">
                <p>XXX</p>
                <p>${comment_histories.data[i].object.display_name}</p>
                <p>XXX</p>
                <p>XXX</p>
                <p>${comment_histories.data[i].published}</p>
                <p>XXX</p>
                <p>XXX</p>
                <p>XXX</p>
            </div>`)
            }
            console.log(comment_histories.data[i].object.display_name)
        }
        
        // comment_histories.data.forEach( (history, index) => {
        //     console.log(history, index)
        //     console.log("aing maung", comment_histories.data[index])
        //     $('.comment-modal').append(`
        //     <div class="comment-modal">
        //             <p>XXX</p>
        //             <p>${comment_histories.data[index].actor.display_name}</p>
        //             <p>XXX</p>
        //             <p>XXX</p>
        //             <p>XXX</p>
        //             <p>XXX</p>
        //             <p>XXX</p>
        //             <p>XXX</p>
        //         </div>
        //     `)
        // }
        // )
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
    $("#request-tab").remove()
    $("#commenthis").remove()
    $("#form-input").remove()
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
        if (getCookie('hr') != 'true'){
            document.getElementById('revise').remove()
        }
    }
}

