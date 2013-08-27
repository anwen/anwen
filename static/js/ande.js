function getCookie(name) {
  var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
  return r ? r[1] : undefined;
}

$(document).ready(function() {
  $('#usersayform').submit(function(e) {
    e.preventDefault();
    get_andesay();
  });
});

function get_andesay() {
  $("#andesay").hide();
  var usersay = $("#usersay").val();
  var xsrf = getCookie("_xsrf");
  // $("#usersay").val("");
  $.ajax({
    type: "POST",
    url: "/ande",
    data: {
      "usersay": usersay,
      "_xsrf": xsrf
    },
    dataType: "json",
    success: function(data) {
      if (data.andesay.length > 0) {
        $("#andesay_box").html(data.andesay);
        $("#andethink").html(data.andethink);
        $("#usersay").val('');
      }
    }
  });
}