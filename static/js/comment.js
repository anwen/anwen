function getCookie(name) {
	var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
	return r ? r[1] : undefined;
}
preAllow = true; //定义一个变量，主要是为了防止恶刷，也是为了防止重复提交，在返回结果之前是不能点击的
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


	$("#likeit").submit(function(e)
	{
		e.preventDefault();
		if (preAllow) {
			preAllow = false;
			var flag = 1;
			var share_id = encodeURI(encodeURI($("#share_id").val()));
			var likenum = encodeURI(encodeURI($("#likenum").val()));
			var argsxsrf = getCookie("_xsrf");
			if (flag) {
				$('#like').val('感谢您的喜欢，努力提交中..');
				$.ajax({
					type: "POST",
					url: "/sharelike",
					data: {
						"share_id": share_id,
						"likenum": likenum,
						"_xsrf": argsxsrf
					},
					success: function(data) {
						preAllow = true;
						$('#like').val(data);
						$('#like').attr("disabled", "disabled"); 
					}
				});
			}
		}
	});



})