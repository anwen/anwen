//---------------------------------
//-----------图片上传-----
//---------------------------------
jQuery('#switchImgWrap').toggle(

function() {
    jQuery(this).html('取消上传');
    if (jQuery('.post_image_upload_wrap').css('display') == 'none') {
        jQuery('.post_image_upload_wrap').show();
    }
},

function() {
    jQuery(this).html('上传图片');
    if (jQuery('.post_image_upload_wrap').css('display') == 'block') {
        jQuery('.post_image_upload_wrap').hide();
    }
});

//---------------------------------
//-----------拖拽上传图片-----------
//---------------------------------
var dropbox = jQuery('.post_image_upload'),
    message = jQuery('.message', dropbox),
    template = '<div class="preview">' +
        '<span class="imageHolder">' +
        '<span class="uploaded"></span>' +
        '</span>' +
        '<div class="progressHolder">' +
        '<div class="progress"></div>' +
        '</div>' +
        '</div>';

dropbox.filedrop({
    // The name of the jQuery_FILES entry:
    paramname: 'uploadImg',
    allowedfiletypes: ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'],
    maxfiles: 1,
    maxfilesize: 2, //最大2M
    url: '/share/image_upload',
    uploadFinished: function(i, file, response) {
        if (response.status == 's') {
            alert(response.info);
            jQuery(".preview").remove();
            jQuery('.post_image_upload').css({
                'background': '#EAF5FA'
            });
        } else if (response.status == 'o') {
            alert(response.info);
            jQuery(".preview").remove();
            jQuery('.post_image_upload').css({
                'background': '#EAF5FA'
            });
        } else if (response.status == 'y') {
            jQuery('#post_Img_1').val(response.pic_1200);
            jQuery(".imageHolder").css({
                "background": 'url(" ' + "static/upload/img/" + response.pic_1200 + ' ") center center no-repeat',
                'background-size': 'cover'
            });

            jQuery('.post_image_upload').css({
                'background-size': 'cover',
                'background-image': 'url(" ' + "static/upload/img/" + response.pic_1200 + ' ")'
            });

            jQuery.data(file).addClass('done');
            uploaded = jQuery('.uploaded', dropbox);
            jQuery(uploaded).fadeIn(300);

            jQuery('.upload_btn').hide();

            jQuery('.del_post_img, .save_post_img_btn').show();
            setTimeout(function() {
                jQuery('.uploaded, .progressHolder').fadeOut(250);
            }, 1000);


        }

    },

    error: function(err, file) {
        switch (err) {
            case 'BrowserNotSupported':
                showMessage('你的浏览器不支持HTML5上传');
                break;
            case 'TooManyFiles':
                alert('添加一张就可以了');
                break;
            case 'FileTooLarge':
                alert(file.name + ' 太大了，请上传不超过2M的');
                break;
            default:
                break;
        }
    },

    beforeEach: function(file) {
        if (!file.type.match(/^image\//)) {
            alert('Only images are allowed!');
            return false;
        }
    },

    uploadStarted: function(i, file, len) {
        createImage(file);
        jQuery(".post_image_upload_1").css({
            'background': 'none'
        });
    },

    progressUpdated: function(i, file, progress) {
        jQuery.data(file).find('.progress').width(progress);
    }

});

function createImage(file) {

    var preview = jQuery(template),
        image = jQuery('.imageHolder', preview);

    var reader = new FileReader();

    reader.onload = function(e) {

    };

    // Reading the file as a DataURL. When finished,
    // this will trigger the onload function above:
    reader.readAsDataURL(file);

    message.hide();
    preview.appendTo(dropbox);

    // Associating a preview container
    // with the file, using jQuery's jQuery.data():

    jQuery.data(file, preview);
}

function showMessage(msg) {
    message.html(msg);
}

//---------------------------------
//-----------点击上传图片-----------
//---------------------------------
jQuery("#upload_file_hide").change(function() {
    //创建FormData对象
    var data = new FormData();
    //为FormData对象添加数据
    jQuery.each(jQuery('#upload_file_hide')[0].files, function(i, file) {
        data.append('uploadImg', file);
    });
    jQuery(".post_image_upload").css({
        'background': 'url(/static/img/onLoad.gif) center center no-repeat'
    }).find('.message').hide();
    jQuery.ajax({
        url: '/share/image_upload',
        type: 'POST',
        data: data,
        cache: false,
        contentType: false, //不可缺
        processData: false, //不可缺
        dataType: "json",
        success: function(response) {

            if (response.status == 's') {
                alert(response.info);
                jQuery(".preview").remove();
                jQuery('.post_image_upload').css({
                    'background': '#EAF5FA'
                });
            } else if (response.status == 'o') {
                alert(response.info);
                jQuery(".preview").remove();
                jQuery('.post_image_upload').css({
                    'background': '#EAF5FA'
                });
            } else if (response.status == 'y') {
                jQuery('#post_Img_1').val('' + response.pic_1200);
                jQuery(".post_image_upload").css({
                    "background": 'url(" ' + "static/upload/img/" + response.pic_1200 + ' ") center center no-repeat',
                    'background-size': 'cover'
                });
                jQuery('.message, .upload_btn').hide();
                jQuery('.del_post_img').show();
            }
        },
        error: function() {
            alert("请检查文件格式或者文件大小，目前只支持jpg/gif/jpeg/png/bmp格式的图片。不能超过2M");
            jQuery('.message').show();
            jQuery('.post_image_upload').css({
                'background': '#EAF5FA'
            });
        }
    });
});


//删除post图片

function DeletePostImg() {
    // 需要判断是拖拽上传还是点击上传的
    var path = '';
    if (jQuery('.imageHolder').size() > 0) {
        path = jQuery(".imageHolder").css("background-image");
    } else {
        path = jQuery(".post_image_upload").css("background-image");
    }

    path = path.replace(/"/g, "").replace(/url\(|\)$/ig, "");
    h = path.split("/", 6).join("/");
    // http://0.0.0.0:8888
    d = path.replace(h, "").replace('/', "");
    d = d.split('_')[0] + "_" + d.split('_')[1] + "_" + d.split('_')[2];

    jQuery.ajax({
        url: '/share/image_upload',
        type: 'DELETE',
        data: {
            img_name: d
        },
        dataType: "text",
        success: function(mes) {
            if (mes == 's') {
                //恢复上传容器的原始大小
                jQuery('.post_image_upload_wrap').attr('style', '');
                jQuery('.input-mlarge').addClass('input-xxlarge').removeClass('input-mlarge');
                if (jQuery('.imageHolder').size() > 0) {
                    jQuery(".preview").remove();
                }
                jQuery('.post_image_upload').css({
                    'background': '#eaf5fa'
                });
                jQuery('.upload_btn, .message').show();
                jQuery('.del_post_img, .save_post_img_btn').hide();
                jQuery('.change_post_image_btn').css({
                    'background-color': '#58AD69',
                    'color': '#fff'
                }).html('<i class="icon-pencil icon-white"></i> 更换图片');

            }
        },
        error: function() {
            alert('出错，可能是服务器那边出问题了，请联系管理员');
        }
    });

    jQuery('#post_Img_1').val('');
}

//删除更改图片是上传的图片
jQuery(".del_post_img").click(DeletePostImg);


$(document).ready(function() {
    JudgeCheck();
    CheckImg();
});

function JudgeCheck() {
    var sharetype = $("input[name=sharetype]")[0].value;
    $("input[name=type][value=" + sharetype + "]").attr("checked", true);
}


function CheckImg() {
    var post_img = $("input[name=post_img]")[0].value;
    if (post_img) {
        var post_img_path = '/static/upload/img/' + post_img;
        jQuery('.post_image_upload').css({
            'background-size': 'cover',
            'background-image': 'url(" ' + post_img_path + ' ")'
        });

        jQuery('#post_Img_1').val('' + post_img);
        jQuery(".imageHolder").css({
            "background": 'url("' + post_img_path + ' ") center center no-repeat',
            'background-size': 'cover'
        });
        jQuery('.message, .upload_btn').hide();
        jQuery('.del_post_img, .save_post_img_btn').show();

    }
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


jQuery('#wysiwyg_post_form').Validform({
    tipSweep : true,
    ajaxPost:true,
    ignoreHidden:true,
    
    datatype : {
        "title": /^[\w\W]{1,2}$$/,
        "content": /^[\w\W]{5,65535}$/
    },
    tiptype:function(msg,o,cssctl){
        var objtip=o.obj.siblings(".Validform_checktip");
        cssctl(objtip,o.type);
        objtip.text(msg);
    },
    beforeCheck:function(curform){
        var content = jQuery('#editor').html();
        alert(content);
        $('#hidden-content').html(content);
        //在表单提交执行验证之前执行的函数，curform参数是当前表单对象。
        //这里明确return false的话将不会继续执行验证操作;    
    },
    beforeSubmit:function(curform){
        curform.find('button#save').html('发布中...').removeClass('btn-info');
    },
    callback:function(data){
        if(data.status=="y"){
            window.location.href = "/share/" + data.post_id;
        }
    }
});
