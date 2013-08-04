$.fn.toggleClick = function(){

    var functions = arguments ;

    return this.click(function(){
            var iteration = $(this).data('iteration') || 0;
            functions[iteration].apply(this, arguments);
            iteration = (iteration + 1) % functions.length ;
            $(this).data('iteration', iteration);
    });
};
//---------------------------------
//-----------图片上传-----
//---------------------------------
$('#switchImgWrap').toggleClick(

    function () {
        $(this).html('取消上传');
        if ($('.post_image_upload_wrap').css('display') == 'none') {
            $('.post_image_upload_wrap').show();
        }
    },

    function () {
        $(this).html('上传图片');
        if ($('.post_image_upload_wrap').css('display') == 'block') {
            $('.post_image_upload_wrap').hide();
        }
    }
);

//---------------------------------
//-----------拖拽上传图片-----------
//---------------------------------
var dropbox = $('.post_image_upload'),
    message = $('.message', dropbox),
    template = '<div class="preview">' +
        '<span class="imageHolder">' +
        '<span class="uploaded"></span>' +
        '</span>' +
        '<div class="progressHolder">' +
        '<div class="progress"></div>' +
        '</div>' +
        '</div>';

dropbox.filedrop({
    // The name of the $_FILES entry:
    paramname: 'uploadImg',
    allowedfiletypes: ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'],
    maxfiles: 1,
    maxfilesize: 2, //最大2M
    url: '/share/image_upload',
    uploadFinished: function (i, file, response) {
        if (response.status == 's') {
            alert(response.info);
            $(".preview").remove();
            $('.post_image_upload').css({
                'background': '#EAF5FA'
            });
        } else if (response.status == 'o') {
            alert(response.info);
            $(".preview").remove();
            $('.post_image_upload').css({
                'background': '#EAF5FA'
            });
        } else if (response.status == 'y') {
            $('#post_Img_1').val(response.pic_1200);
            $(".imageHolder").css({
                "background": 'url(" ' + "static/upload/img/" + response.pic_1200 + ' ") center center no-repeat',
                'background-size': 'cover'
            });

            $('.post_image_upload').css({
                'background-size': 'cover',
                'background-image': 'url(" ' + "static/upload/img/" + response.pic_1200 + ' ")'
            });

            $.data(file).addClass('done');
            uploaded = $('.uploaded', dropbox);
            $(uploaded).fadeIn(300);

            $('.upload_btn').hide();

            $('.del_post_img, .save_post_img_btn').show();
            setTimeout(function () {
                $('.uploaded, .progressHolder').fadeOut(250);
            }, 1000);


        }

    },

    error: function (err, file) {
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

    beforeEach: function (file) {
        if (!file.type.match(/^image\//)) {
            alert('Only images are allowed!');
            return false;
        }
    },

    uploadStarted: function (i, file, len) {
        createImage(file);
        $(".post_image_upload_1").css({
            'background': 'none'
        });
    },

    progressUpdated: function (i, file, progress) {
        $.data(file).find('.progress').width(progress);
    }

});

function createImage(file) {

    var preview = $(template),
        image = $('.imageHolder', preview);

    var reader = new FileReader();

    reader.onload = function (e) {

    };

    // Reading the file as a DataURL. When finished,
    // this will trigger the onload function above:
    reader.readAsDataURL(file);

    message.hide();
    preview.appendTo(dropbox);

    // Associating a preview container
    // with the file, using $'s $.data():

    $.data(file, preview);
}

function showMessage(msg) {
    message.html(msg);
}

//---------------------------------
//-----------点击上传图片-----------
//---------------------------------
$("#upload_file_hide").change(function () {
    //创建FormData对象
    var data = new FormData();
    //为FormData对象添加数据
    $.each($('#upload_file_hide')[0].files, function (i, file) {
        data.append('uploadImg', file);
    });
    $(".post_image_upload").css({
        'background': 'url(/static/img/onLoad.gif) center center no-repeat'
    }).find('.message').hide();
    $.ajax({
        url: '/share/image_upload',
        type: 'POST',
        data: data,
        cache: false,
        contentType: false, //不可缺
        processData: false, //不可缺
        dataType: "json",
        success: function (response) {

            if (response.status == 's') {
                alert(response.info);
                $(".preview").remove();
                $('.post_image_upload').css({
                    'background': '#EAF5FA'
                });
            } else if (response.status == 'o') {
                alert(response.info);
                $(".preview").remove();
                $('.post_image_upload').css({
                    'background': '#EAF5FA'
                });
            } else if (response.status == 'y') {
                $('#post_Img_1').val('' + response.pic_1200);
                $(".post_image_upload").css({
                    "background": 'url(" ' + "static/upload/img/" + response.pic_1200 + ' ") center center no-repeat',
                    'background-size': 'cover'
                });
                $('.message, .upload_btn').hide();
                $('.del_post_img').show();
            }
        },
        error: function () {
            alert("请检查文件格式或者文件大小，目前只支持jpg/gif/jpeg/png/bmp格式的图片。不能超过2M");
            $('.message').show();
            $('.post_image_upload').css({
                'background': '#EAF5FA'
            });
        }
    });
});


//删除post图片

function DeletePostImg() {
    // 需要判断是拖拽上传还是点击上传的
    var path = '';
    if ($('.imageHolder').size() > 0) {
        path = $(".imageHolder").css("background-image");
    } else {
        path = $(".post_image_upload").css("background-image");
    }

    path = path.replace(/"/g, "").replace(/url\(|\)$/ig, "");
    h = path.split("/", 6).join("/");
    // http://0.0.0.0:8888
    d = path.replace(h, "").replace('/', "");
    d = d.split('_')[0] + "_" + d.split('_')[1] + "_" + d.split('_')[2];

    $.ajax({
        url: '/share/image_upload',
        type: 'DELETE',
        data: {
            img_name: d
        },
        dataType: "text",
        success: function (mes) {
            if (mes == 's') {
                //恢复上传容器的原始大小
                $('.post_image_upload_wrap').attr('style', '');
                $('.input-mlarge').addClass('input-xxlarge').removeClass('input-mlarge');
                if ($('.imageHolder').size() > 0) {
                    $(".preview").remove();
                }
                $('.post_image_upload').css({
                    'background': '#eaf5fa'
                });
                $('.upload_btn, .message').show();
                $('.del_post_img, .save_post_img_btn').hide();
                $('.change_post_image_btn').css({
                    'background-color': '#58AD69',
                    'color': '#fff'
                }).html('<i class="icon-pencil icon-white"></i> 更换图片');

            }
        },
        error: function () {
            alert('出错，可能是服务器那边出问题了，请联系管理员');
        }
    });

    $('#post_Img_1').val('');
}

//删除更改图片是上传的图片
$(".del_post_img").click(DeletePostImg);


$(document).ready(function () {
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
        $('.post_image_upload').css({
            'background-size': 'cover',
            'background-image': 'url(" ' + post_img_path + ' ")'
        });

        $('#post_Img_1').val('' + post_img);
        $(".imageHolder").css({
            "background": 'url("' + post_img_path + ' ") center center no-repeat',
            'background-size': 'cover'
        });
        $('.message, .upload_btn').hide();
        $('.del_post_img, .save_post_img_btn').show();

    }
}