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
            if (document.getElementById('email').value[0] == 'h' || document.getElementById('email').value[0] == 'H' ){
                
                var isHr = true;
            } else {
                var isHr = false;
            }
            document.cookie = `token=${res}`;
            document.cookie = `requester=${isRequest}`;
            document.cookie = `hr=${isHr}`
            window.location = "/requester.html";
        },
        error: function(err){
            console.log(err)
        }
    })
}

