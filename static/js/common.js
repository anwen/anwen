jQuery(function(){
    //goTop
    jQuery(window).scroll(function() {
        var t = jQuery(window).scrollTop();
        if(t >= 1024){
            jQuery('#goTop').removeClass('invisible')
        }
        if (t < 1024){
            jQuery('#goTop').addClass('invisible')
        }
    })
    
    // 回顶端 
    jQuery('#goTop').click(function(){
        jQuery(document).stop().scrollTo(0, 400);
    })

    // 弹出overlay层
    function OpenOverlay(){
        var douban_id = jQuery(this).attr('href').split('/')[2],
            douban_uid = jQuery(this).attr('title')
        jQuery('body').addClass('home-overlay-enabled');
        jQuery('.overlay_username').html(douban_uid);
        jQuery('#overlay_douban_link').attr('href', 'http://www.douban.com/people/' + douban_id)
        return false;
    }

    // 关闭overlay层
    jQuery('.home-overlay-close ').click(function(){
        jQuery('body').removeClass('feedback-overlay-enabled').removeClass('home-overlay-enabled');
    })

    //打开feedback层
    jQuery('#feedbackBtn').tooltip({
        placement : 'left'
    }).click(openFeedback)

    function openFeedback(){
        jQuery('#feedback_wrap h3').remove();
        jQuery('body').addClass('feedback-overlay-enabled');
        jQuery('#feedbackForm input:submit').removeClass('disabled').removeAttr('disabled');
        jQuery('#feedbackForm').fadeIn();
    }

    function closeFeedback(){
        jQuery('#feedbackForm').hide().after('<h3>提交成功，感谢你的反馈,我们会尽快处理 :) <span class="show" style="font-size:12px;font-weight:normal">本窗口会自动关闭</span></h3>');
        jQuery('#feedbackForm textarea').val('');
        jQuery('#feedbackForm input:submit').addClass('disabled').attr('disabled','disabled');
        setTimeout(function(){
            jQuery('body').removeClass('feedback-overlay-enabled');
        },3000)
    }

    //feedback 表单验证
    jQuery('#feedbackForm').Validform({
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
