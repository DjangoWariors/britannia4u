$(document).ready(function () {

    // prevent cut copy paste in fields
    $('.disable-ccp').bind("cut copy paste", function (e) {
        e.preventDefault();
    });
    $(".number-only").bind('keypress', function (event) {
        var charCode = (event.which) ? event.which : event.keyCode
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    });
    // allow only alphabets in fields
    $(".alpha-space").bind('keypress', function (event) {
        var xp = new RegExp("^[a-zA-Z ]*$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!xp.test(key)) {
            event.preventDefault();
            return false;
        }
    });
    $(".alpha-only").bind('keypress', function (event) {
        var xp = new RegExp("^[a-zA-Z]*$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!xp.test(key)) {
            event.preventDefault();
            return false;
        }
    });
    $(".alpha-numeric").bind('keypress', function (event) {
        var xp = new RegExp("^[0-9a-zA-Z]*$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!xp.test(key)) {
            event.preventDefault();
            return false;
        }
    });
    $(".alpha-numericuser").bind('keypress', function (event) {
        var xp = new RegExp("^[0-9a-zA-Z@_.-/\']*$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!xp.test(key)) {
            event.preventDefault();
            return false;
        }
    });
    $(".alpha-numericspace").bind('keypress', function (event) {
        var xp = new RegExp("^[0-9a-zA-Z_.-/ ]*$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!xp.test(key)) {
            event.preventDefault();
            return false;
        }
    });
    //email key press validation
    $(".email-chars").bind('keypress', function (event) {
        var xp = new RegExp("^[a-zA-Z0-9@\\-\\.]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (event.which === 32) {
            event.preventDefault();
            return false;
        }
        else if (!xp.test(key)) {
            event.preventDefault();
            return false;
        }
    });
});


$(document).ready(function () {
    var showChar = 100; 
    var ellipsestext = "...";
    var moretext = "Show more >";
    var lesstext = "Show less";

    $('.more').each(function () {
        var content = $(this).html();

        if (content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

            $(this).html(html);
        }

    });

    $(".morelink").click(function () {
        if ($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
});