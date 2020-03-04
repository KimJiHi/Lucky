$(document).ready(function () {
    var button = document.getElementById("submit")

    $.post("/checkPrize/", function(data) {
            if (data.status == "error"){
                button.style.pointerEvents = "none"
                button.value = "已参与"
            }
        })
})