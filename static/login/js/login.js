function checklogin() {
    var account = document.getElementById("account")
    var password = document.getElementById("pwd")
    var pwdd = document.getElementById("pwdd")
    var form = document.getElementById("login")
    var acc,pwd
    acc = account.value
    pwd = password.value
    console.log("aaa")
    $.post("/checklogin/", {"account":acc,"pwd":pwd}, function(data) {
        if (data.status == "error"){
            alert('密码错误')
            return
        }
        else {
            form.method="POST"
            form.action="/login/"
            form.submit()
        }
    })

}