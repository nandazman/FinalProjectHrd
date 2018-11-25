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
            console.log(res.data)
            var requester = res.data
            if (requester.length == 0){
                $('#alltaskuser').append(`<div class="taskitem")">
                <h3>There is no task at the moment</h3>
            </div>`)
            } else {
                requester.forEach(task => {
                    
                    $('#alltaskuser').append(`<div class="taskitem" onclick="showModal('${task.id}','${task.record_id}')">
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
            console.log(res)
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

function updateSummary(){
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
        },
        success: function(res){
            console.log(res)
        },
        error: function(err){
            console.log(err)
        }
    })
}

function getProfile(){
    $.ajax({
        method: 'GET',
        url: 'http://localhost:7000/getProfile',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', getCookie('token'));
        },
        success: function(res){
            console.log(JSON.parse(res))
            data = JSON.parse(res)
            $('#user').append(`<h4>Hello, ${data.nama}!</h4>`)
            $('#new-information').prepend(`<div class="listForm">
            <p>REQUESTER NAME</p>
            <p>${data.nama}</p>
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
                console.log(JSON.parse(res))
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
                <input value="${data.position_code}" />
            </div>
            <div class="listForm">
                <p>POSITION</p>
                <input value="${data.position}" />
            </div>
            <div class="listForm">
                <p>COMPANY</p>
                <input value="${data.company}" />
            </div>
            <div class="listForm">
                <p>COST CENTER</p>
                <div>
                <input class="doubleinput1" value="${data.cost_center_code}" />
                <br>
                <input class="doubleinput2" value="${data.cost_center}" />
                </div>
            </div>
            <div class="listForm">
                <p>PERSONAL AREA</p>
                <input value="${data.personal_area}" />
            </div>
            <div class="listForm">
                <p>EMPLOYEE GROUP</p>
                <input value="${data.employee_group}" />
            </div>
            <div class="listForm">
                <p>EMPLOYEE SUBGROUP</p>
                <input value="${data.employee_sub_group}" />
            </div>
            `)
            console.log(data)
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
        $("#new-request").slideToggle();
        $(".second-box").slideUp();
        
    });
});
$(document).ready(function () {
    $("#commenthis").click(function () {
        $(".second-box").slideToggle();
        $("#new-request").slideUp();
    });
});

function showModal(taskid,recordid) {
    document.getElementById('modal-form').style.display = "block";
    $('#confirmation').append(`<button onclick="submitTask('${taskid}','${recordid}','Approved')" id="approve">Approved</button>`)
    if (getCookie('hr') != 'true'){
        $('#confirmation').append(`<button onclick="submitTask('${taskid}','${recordid}','Revised')" id="revise">Revised</button>`)
    }
}
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

