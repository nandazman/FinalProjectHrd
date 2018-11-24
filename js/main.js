$(document).ready(function(){
    $("#request-tab").click(function(){
        $("#new-request").slideToggle();
        $(".second-box").slideUp();
    });
});
$(document).ready(function(){
    $("#commenthis").click(function(){
        $(".second-box").slideToggle();
        $("#new-request").slideUp();
    });
});

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
            window.location = "/index.html";
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
            console.log(res)
            var requester = res.data
            requester.forEach(task => {
                $('#new-request').append(`<div class="itemrequest" onclick="showModal('${task.record_id}')">
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
$.when(
    $.ajax({

    }),
    $.ajax({

    })
).done(function(hasilAjax1, hasilAjax2){
    
})