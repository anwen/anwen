$(document).tooltip({
    selector: "a[rel=tooltip]"
});


$(function(){
    //goTop
    $(window).scroll(function() {
        var t = $(window).scrollTop();
        if(t >= 1024){
            $('#goTop').removeClass('invisible')
        }
        if (t < 1024){
            $('#goTop').addClass('invisible')
        }
    })
    
    // 回顶端 
    $('#goTop').click(function(){
        $(document).stop().scrollTo(0, 400);
    })

    //打开feedback层
    $('#feedbackBtn').tooltip({
        placement : 'left'
    }).click(openFeedback)

    function openFeedback(){
        $('#feedback_wrap h3').remove();
        $('body').addClass('feedback-overlay-enabled');
        $('#feedbackForm input:submit').removeClass('disabled').removeAttr('disabled');
        $('#feedbackForm').fadeIn();
    }

    function closeFeedback(){
        $('#feedbackForm').hide().after('<h3>提交成功，感谢你的反馈,我们会尽快处理 :) <span class="show" style="font-size:12px;font-weight:normal">本窗口会自动关闭</span></h3>');
        $('#feedbackForm textarea').val('');
        $('#feedbackForm input:submit').addClass('disabled').attr('disabled','disabled');
        setTimeout(function(){
            $('body').removeClass('feedback-overlay-enabled');
        },3000)
    }

    //feedback 表单验证
    $('#feedbackForm').Validform({
        tipSweep : true,
        ajaxPost:true,
        datatype : {
            "feedback_content": /^[\w\W]{1,500}$$/
        },
        tiptype:function(msg,o,cssctl){
            var objtip=o.obj.siblings(".Validform_checktip");
            cssctl(objtip,o.type);
            objtip.text(msg);
        },
        callback:function(data){
            if(data.status=="y"){
                closeFeedback();
            }
        }
    })

})
