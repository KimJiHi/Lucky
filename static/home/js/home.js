$(document).ready(function(){
    var list = document.getElementById('list')
    var all = document.getElementById('all')
    var bdianzi = document.getElementById('dianzi')
    var bjiating = document.getElementById('jiating')
    var bfushi = document.getElementById('fushi')
    var bjiushui = document.getElementById('jiushui')
    var bdajiang = document.getElementById('dajiang')
    $("#showrelease").click(function(){
        $("#release").slideDown();
        });
    $("#cancel").click(function () {
        $("#release").slideUp();
    });
    // 全部奖品
    $('#all').click(function () {
        list.innerHTML = null
        all.style.background = "#95a5a6"
        bdianzi.style.background = "#5a6268"
        bjiating.style.background = "#5a6268"
        bfushi.style.background = "#5a6268"
        bjiushui.style.background = "#5a6268"
        bdajiang.style.background = "#5a6268"
        $.ajax({
            type: "GET",
            url: "/homelist/",
            dataType: "json",
            success:function (arg) {
                if (arg.status) {
                    var plist = JSON.parse(arg.data)
                    for(i=0;i<=plist.length;i++){
                        list.innerHTML = list.innerHTML+"<a href=/prize/"+plist[i]["pk"]+">"+plist[i]["fields"]["name"]+plist[i]["fields"]["content"]+""
                    }
                }
            }
        })
    })
    //电子数码
    $('#dianzi').click(function () {
        list.innerHTML = null
        bdianzi.style.background = "#95a5a6"
        all.style.background = "#2c3e50"
        bjiating.style.background = "#5a6268"
        bfushi.style.background = "#5a6268"
        bjiushui.style.background = "#5a6268"
        bdajiang.style.background = "#5a6268"
        $.ajax({
            type: "GET",
            url: "/dslist/",
            dataType: "json",
            success:function (arg) {
                if (arg.status) {
                    var plist = JSON.parse(arg.data)
                    for(i=0;i<=plist.length;i++){
                        list.innerHTML = list.innerHTML+"<a href=/prize/"+plist[i]["pk"]+">"+plist[i]["fields"]["name"]+plist[i]["fields"]["content"]+""
                    }
                }
            }
        })
    })
    //家庭日用
    $('#jiating').click(function () {
        list.innerHTML = null
        bjiating.style.background = "#95a5a6"
        all.style.background = "#2c3e50"
        bdianzi.style.background = "#5a6268"
        bfushi.style.background = "#5a6268"
        bjiushui.style.background = "#5a6268"
        bdajiang.style.background = "#5a6268"
        $.ajax({
            type: "GET",
            url: "/jrlist/",
            dataType: "json",
            success:function (arg) {
                if (arg.status) {
                    var plist = JSON.parse(arg.data)
                    for(i=0;i<=plist.length;i++){
                        list.innerHTML = list.innerHTML+"<a href=/prize/"+plist[i]["pk"]+">"+plist[i]["fields"]["name"]+plist[i]["fields"]["content"]+""
                    }
                }
            }
        })
    })
    //服饰护理
    $('#fushi').click(function () {
        list.innerHTML = null
        bfushi.style.background = "#95a5a6"
        all.style.background = "#2c3e50"
        bdianzi.style.background = "#5a6268"
        bjiating.style.background = "#5a6268"
        bjiushui.style.background = "#5a6268"
        bdajiang.style.background = "#5a6268"
        $.ajax({
            type: "GET",
            url: "/fhlist/",
            dataType: "json",
            success:function (arg) {
                if (arg.status) {
                    var plist = JSON.parse(arg.data)
                    for(i=0;i<=plist.length;i++){
                        list.innerHTML = list.innerHTML+"<a href=/prize/"+plist[i]["pk"]+">"+plist[i]["fields"]["name"]+plist[i]["fields"]["content"]+""
                    }
                }
            }
        })
    })
    //酒水食品
    $('#jiushui').click(function () {
        list.innerHTML = null
        bjiushui.style.background = "#95a5a6"
        all.style.background = "#2c3e50"
        bdianzi.style.background = "#5a6268"
        bjiating.style.background = "#5a6268"
        bfushi.style.background = "#5a6268"
        bdajiang.style.background = "#5a6268"
        $.ajax({
            type: "GET",
            url: "/sjlist/",
            dataType: "json",
            success:function (arg) {
                if (arg.status) {
                    var plist = JSON.parse(arg.data)
                    for(i=0;i<=plist.length;i++){
                        list.innerHTML = list.innerHTML+"<a href=/prize/"+plist[i]["pk"]+">"+plist[i]["fields"]["name"]+plist[i]["fields"]["content"]+""
                    }
                }
            }
        })
    })
    //大奖
    $('#dajiang').click(function () {
        list.innerHTML = null
        bdajiang.style.background = "#95a5a6"
        all.style.background = "#2c3e50"
        bdianzi.style.background = "#5a6268"
        bjiating.style.background = "#5a6268"
        bfushi.style.background = "#5a6268"
        bjiushui.style.background = "#5a6268"
        $.ajax({
            type: "GET",
            url: "/djlist/",
            dataType: "json",
            success:function (arg) {
                if (arg.status) {
                    var plist = JSON.parse(arg.data)
                    for(i=0;i<=plist.length;i++){
                        list.innerHTML = list.innerHTML+"<a href=/prize/"+plist[i]["pk"]+">"+plist[i]["fields"]["name"]+plist[i]["fields"]["content"]+""
                    }
                }
            }
        })
    })

    //启动时点击按钮
    $('#all').trigger("click");
});
// function release() {
//     var div = document.getElementById("release")
//     div.style.display="block"
// }
// function closerelease() {
//     var div = document.getElementById("release")
//     div.style.display='none'
// }