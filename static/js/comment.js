$(document).ready(function() {
    $('#resizer span').click(function() {
        var fontSize = 1.0;
        var name = $(this).attr('id');
        if (name == 'f_s') {
            fontSize -= 0.1;
        } else if (name == 'f_m') {
            fontSize += 0.1;
        } else if (name == 'f_l') {
            fontSize += 0.2;
        }
        $('.entry p').css('font-size', fontSize + 'em');
    });
});

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 为了防止恶刷，也是为了防止重复提交，在返回结果之前是不能点击的
preAllow = true;

$(document.body).on('click', '.do-like', function() {
    var t = $(this),
        action = 'addlike';
    if (t.hasClass('liking')) {
        action = 'dellike';
    }
    var argsxsrf = getCookie("_xsrf");
    var eid = t.attr('eid');
    var etype = t.attr('etype');
    if (!eid) return;
    $.ajax({
        url: '/api/like/' + action,
        type: 'get',
        data: {
            "action": action,
            "entity_id": eid,
            "entity_type": etype,
            "_xsrf": argsxsrf
        },
        success: function(data) {
            if (action === 'addlike') {
                t.addClass('liking');
            } else if (action === 'dellike') {
                t.removeClass('liking');
            }
            t.find('span').text(data['likenum'] + ' ');
        }
    });
});
$(document.body).on('click', '.do-dislike', function() {
    var t = $(this),
        action = 'adddislike';
    if (t.hasClass('disliking')) {
        action = 'deldislike';
    }
    var argsxsrf = getCookie("_xsrf");
    var lid = $('.post_header').attr('data-id');
    if (!lid) {
        return;
    }
    $.ajax({
        url: '/api/like/' + action,
        type: 'get',
        data: {
            "action": action,
            "entity_id": lid,
            "entity_type": "share",
            "_xsrf": argsxsrf
        },
        success: function(data) {
            if (action === 'adddislike') {
                t.addClass('disliking');
            } else if (action === 'deldislike') {
                t.removeClass('disliking');
            }
            t.find('span').text(data['dislikenum'] + ' ');
        }
    });
});




$(function() {
    $("#addCommentForm").submit(function(e) //使用jquery封装js
        {
            e.preventDefault();
            if (preAllow) {
                preAllow = false;
                var flag = 1; //定义一个变量，当下面的一些检查发现问题会置0，这样就不会发送post请求了
                var commentbody = $("#commentbody").val();
                var share_id = encodeURI(encodeURI($("#share_id").val()));
                if (commentbody == "") {
                    $("textarea[name=commentbody]").select();
                    flag = 0;
                }
                var argsxsrf = getCookie("_xsrf");
                if (flag) {
                    $('#submit').val('感谢您的评论，努力提交中..');
                    $.ajax({
                        type: "POST",
                        url: "/sharecomment",
                        data: {
                            "share_id": share_id,
                            "commentbody": commentbody,
                            "_xsrf": argsxsrf
                        },
                        success: function(data) { //回调函数，alert返回结果
                            //alert(decodeURI(data));
                            $(data).hide().insertBefore('#addCommentContainer').slideDown();
                            $('#commentbody').val('');
                            preAllow = true;
                            $('#submit').val('提交');
                        }
                    });
                }
            }
        });
})
$(function() {
    $("#addViewPoint").submit(function(e) {
        e.preventDefault();
        if (preAllow) {
            preAllow = false;
            var flag = 1;
            var aview = $("#aview").val();
            var share_id = encodeURI(encodeURI($("#share_id").val()));
            if (aview == "") {
                $("input[name=aview]").select();
                flag = 0;
            }
            var argsxsrf = getCookie("_xsrf");
            if (flag) {
                $('#submit').val('感谢您的观点，努力提交中..');
                $.ajax({
                    type: "POST",
                    url: "/viewpoint",
                    data: {
                        "share_id": share_id,
                        "aview": aview,
                        "_xsrf": argsxsrf
                    },
                    success: function(data) {
                        //alert(decodeURI(data));
                        data = '<p>'+data+'</p>';
                        $(data).hide().insertBefore('#addViewPoint').slideDown();
                        $('#viewpoint').val('');
                        preAllow = true;
                        $('#submit').val('提交');
                    }
                });
            }
        }
    });
})
