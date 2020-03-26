$(document).ready(function(){
    $("#showrelease").click(function(){
        $("#release").slideDown();
        });
    $("#cancel").click(function () {
        $("#release").slideUp();
    });
    $("#control").click(function () {
        if ($(this).text()=='展开导航'){
            $(this).text('关闭导航');
        }
        else {
            $(this).text('展开导航');
        }
        $("#sidebars").toggle();
    });

    $("#allList").click(function () {
        $(this).css('color','#9F79EE')
        $("#dianzi").css('color','black')
        $("#jiating").css('color','black')
        $("#fushi").css('color','black')
        $("#jiushui").css('color','black')
        $("#dajiang").css('color','black')
        $.ajax({
            url:'/homelist/',
            dataType:'html',
            success:function (data) {
                $("#litem").html(data)
            }
        })
        location.hash = 'all'
        return false
    })

    $("#dianzi").click(function () {
        $(this).css('color','#9F79EE')
        $("#allList").css('color','black')
        $("#jiating").css('color','black')
        $("#fushi").css('color','black')
        $("#jiushui").css('color','black')
        $("#dajiang").css('color','black')
        $.ajax({
            url:'/dslist/',
            dataType:'html',
            success:function (data) {
                $("#litem").html(data)
            }
        })
        location.hash = '电子&数码'
        return false
    })

    $("#jiating").click(function () {
        $(this).css('color','#9F79EE')
        $("#dianzi").css('color','black')
        $("#allList").css('color','black')
        $("#fushi").css('color','black')
        $("#jiushui").css('color','black')
        $("#dajiang").css('color','black')
        $.ajax({
            url:'/jrlist/',
            dataType:'html',
            success:function (data) {
                $("#litem").html(data)
            }
        })
        location.hash = '家庭&日用'
        return false
    })

    $("#fushi").click(function () {
        $(this).css('color','#9F79EE')
        $("#dianzi").css('color','black')
        $("#jiating").css('color','black')
        $("#allList").css('color','black')
        $("#jiushui").css('color','black')
        $("#dajiang").css('color','black')
        $.ajax({
            url:'/fhlist/',
            dataType:'html',
            success:function (data) {
                $("#litem").html(data)
            }
        })
        location.hash = '服饰&护理'
        return false
    })

    $("#jiushui").click(function () {
        $(this).css('color','#9F79EE')
        $("#dianzi").css('color','black')
        $("#jiating").css('color','black')
        $("#fushi").css('color','black')
        $("#allList").css('color','black')
        $("#dajiang").css('color','black')
        $.ajax({
            url:'/sjlist/',
            dataType:'html',
            success:function (data) {
                $("#litem").html(data)
            }
        })
        location.hash = '食品&酒水'
        return false
    })

    $("#dajiang").click(function () {
        $(this).css('color','#9F79EE')
        $("#dianzi").css('color','black')
        $("#jiating").css('color','black')
        $("#fushi").css('color','black')
        $("#jiushui").css('color','black')
        $("#allList").css('color','black')
        $.ajax({
            url:'/djlist/',
            dataType:'html',
            success:function (data) {
                $("#litem").html(data)
            }
        })
        location.hash = '超级大奖'
        return false
    })

    $("#search").submit(function () {
        event.preventDefault()||(event.returnValue=false);
        var str = $("#str").val()
        $.post("/search/",{'str':str},function (data) {
            $("#litem").html(data)
        })
        location.hash = 'search='+ str
    })

$("#allList").trigger('click')
});
