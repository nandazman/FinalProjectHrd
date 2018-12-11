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
            if (document.getElementById('email').value[0] == 'h') {
                var isHr = true;
                var isProposed = true;
            } else if (document.getElementById('email').value[0] == 'H') {
                var isHr = true;
                var isProposed = false;
            } else {
                var isHr = false;
                var isProposed = false;
            }
            document.cookie = `token=${res}`;
            document.cookie = `requester=${isRequest}`;
            document.cookie = `hr=${isHr}`;
            document.cookie = `proposedHr=${isProposed}`
            window.location = "/home.html";
        },
        error: function(err){
            console.log(err)
        }
    })
}

