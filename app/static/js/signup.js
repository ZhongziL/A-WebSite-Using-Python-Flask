$(function () {
    $("#byPhone").on("click", function () {
        $('#byEmail').attr('checked', false);
        $('#phoneMethod').css("display", "block");
        $('#emailMethod').css("display", "none");
    });

    $("#byEmail").on("click", function () {
        $('#byPhone').attr('checked', false);
        $('#phoneMethod').css("display", "none");
        $('#emailMethod').css("display", "block");
    });

    $("#submitBtn").on("click", function () {
        alert('adsa');
        return false;
    });
});

window.onload = function() {
    var isPhoneChecked = $("input[name='byPhone']:checked").val();
    alert(isPhoneChecked);
    if (isPhoneChecked == "") {
        //$('#byEmail').attr('checked', false);
        $('#phoneMethod').css("display", "block");
        $('#emailMethod').css("display", "none");
    } else {
        //$('#byPhone').attr('checked', false);
        $('#phoneMethod').css("display", "none");
        $('#emailMethod').css("display", "block");
    }
}