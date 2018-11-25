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

function logIn(){
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/login',
        beforeSend: function(req) {
            req.setRequestHeader("Content-Type", "application/json");
        },
        data: JSON.stringify({
            "email": document.getElementById('email').value,
            "password":  document.getElementById('password').value
        }),
        success: function(res){
            if (document.getElementById('email').value == "rudi_hrd@makersinstitute.id"){
                var isRequest = true;
            } else {
                var isRequest = false;
            }
            document.cookie = `token=${res}`;
            document.cookie = `requester=${isRequest}`
            window.location = "/requester.html";
            
        },
        error: function(err){
            console.log(err)
        }
    })
}

function allTask(){
    $.ajax({
        method: 'POST',
        url: 'http://localhost:7000/GetTask',
        beforeSend: function(req) {
            req.setRequestHeader('Authorization', 'Haper_hrd@makersinstitute.id'),
            req.setRequestHeader("Content-Type", "application/json");
        },
        data: JSON.stringify({
            "email": "Haper_hrd@makersinstitute.id"
        }),
        dataType: 'json',
        success: function(res){
            
            var requester = res.data
            requester.forEach(task => {
                $('#alltaskuser').append(`<div class="taskitem" onclick="showModal('${task.record_id}')">
                <img src="image1.jpg">
                <p>Dear ${task.assignee.name}</p>
                <p>${task.id}</p>
            </div>`)
            
            })
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
        },
        error: function(err){
            console.log(err)
        }
    })
}

function getListEmployee(){
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