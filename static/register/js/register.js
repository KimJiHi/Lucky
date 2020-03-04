function registerCheck() {
    var name = document.forms['registerform']['name'].value
    var email = document.forms['registerform']['email'].value
    var phoneNumber = document.forms['registerform']['phoneNumber'].value
    var pwd = document.forms['registerform']['pwd'].value
    var pwd2 = document.forms['registerform']['pwd2'].value
    apos=email.indexOf("@")
    dotpos=email.lastIndexOf(".")

    if (name==''){
        alert('账号不能为空')
        return false
    }
    else if (apos<1||dotpos-apos<2){
        alert('邮箱格式有误')
        return false
    }
    else if (phoneNumber.toString().length!==11){
        alert('手机长度有误')
        return false
    }
    else if (pwd==''){
        alert('密码不能为空')
        return false
    }
    else if (pwd!=pwd2){
        alert('两次密码不相同')
        return false
    }
    else{
        return true
    }
}


$(document).ready(function(){

    var account = document.getElementById("account")
    var accounter1 = document.getElementById("accounter1")
    var accounter2 = document.getElementById("accounter2")
    var name = document.getElementById("name")
    var email = document.getElementById("email")
    var phoneNumber = document.getElementById("phoneNumber")
    var pwd = document.getElementById("pwd")
    var pwd2 = document.getElementById("pwd2")
    var pwdd = document.getElementById("pwdd")

    account.addEventListener("focus", function(){
        accounter1.style.display = "none"
        accounter2.style.display = "none"
    },false)
    account.addEventListener("blur", function(){
        instr = this.value
        if (instr.length < 6 || instr.length > 12){
            accounter1.style.display = "block"
            return
        }
        $.post("/checkuserid/", {"account":instr}, function(data) {
            if (data.status == "error"){
                accounter2.style.display = "block"
                return
            }
        })
    },false)

    pwd2.addEventListener("focus", function(){
        pwdd.style.display = "none"
    },false)
    pwd2.addEventListener("blur", function(){
        instr = this.value
        if (instr != pwd.value){
            pwdd.style.display = "block"
        }
    },false)

})