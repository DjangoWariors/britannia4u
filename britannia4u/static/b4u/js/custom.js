$(function () {

    $(document).on("submit", "[czb-form='true']", function (e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        console.log(url);
        var method = form.attr('method');
        var name = form.attr('name');
        $("[data-message]").removeClass().html("");
        $(".form-error").removeClass().html("");

        var buttontxt = $("button[type=submit]", form).text();
        $("button[type=submit]", form).attr('disabled', true).html('Uploading...');

        $("span.error-message", form).replaceWith("");
        var formData = new FormData(this);

		var file= '';

		//formdata.append("image", file);

        $.ajax({
            url: url,
            method: method,
            data: formData,
            contentType: false,
            cache: false,
            processData: false,

            success: function (resp) {

                $("button[type=submit]", form).attr('disabled', false).html(buttontxt);

                if (resp.StatusCode == 1) {
                    $.each(resp.ErrorMessage, function (key, val) {

                        $('[name="' + key + '"],[textarea="' + key + '"]', form).after('<span class="invalid-feedback form-error" style="display: unset;">' + val + '</span>');

                    });
                } else if (resp.StatusCode == 2) {

                    alert(resp.ErrorMessage.mobile);
                } else if (resp.StatusCode == 5) {
                    $('#sign-in').hide();
                    $("#otp-send-message").html(resp.ErrorMessage)
                    $('#verify-otp').show();
                } else if (resp.StatusCode == 9) {
                    Swal.fire(resp.ErrorMessage);
                } else if (resp.StatusCode == 0) {

                    if (resp.Reload && resp.Reload == 'false') {

                    } else {
                        setTimeout(function () {
                            window.location.reload();
                        }, 10);
                    }
                    if (resp.FormBlank) {
                        if (resp.FormBlank == 'false') {

                        } else {
                            form[0].reset();
                        }
                    }
                    $("[data-message]").addClass(resp.Class).attr('onClick', "this.classList.add('hide')").html(resp.Message);

                } else if (resp.StatusCode == 3) {
                    window.location.replace(resp.RedirectUrl);
                } else {
                    $("[data-message]").addClass(resp.Class).attr('onClick', "this.classList.add('hide')").html(resp.Message);
                }

            },
            error: function (res) {
                alert("Slow network please try again !");
                // location.reload();
            }
        });
    });


    $("[czb-link]").on("click", function (e) {
        e.preventDefault();

        var url = $(this).attr('data-href');
        var id = '';
        $.ajax({
            url: url,
            type: "post",
            data: {id: id,},
            success: function (resp) {
                if (resp) {
                    if (resp.StatusCode == 0) {
                        //Swal.fire(resp.ErrorMessage)
                        Swal.fire({
                            title: resp.ErrorMessage,
                            didOpen: function () {
                                Swal.showLoading()
                                setTimeout(function () {
                                    Swal.close()
                                }, 2000)
                            }
                        })
                    } else if (resp.StatusCode == 3) {
                        window.location.replace(resp.RedirectUrl);
                    }
                }
            },
            error: function (res) {
                location.reload();
            }
        });
    });

    $("[czb-like-counter]").on("click", function (e) {
        e.preventDefault();

        var url = $(this).attr('data-href-like');
        var id = $(this).attr('image-id');

        $.ajax({
            url: url,
            type: "post",
            data: {id: id,},
            success: function (resp) {
                if (resp) {
                    if (resp.StatusCode == 0) {

                        $("[ajax-count]").html(resp.TotalLikes)

                        Swal.fire(resp.ErrorMessage)
                        Swal.fire({
                            title: resp.ErrorMessage,
                            didOpen: function () {
                                setTimeout(function () {
                                    Swal.close()
                                }, 2000)
                            }
                        })
                    } else if (resp.StatusCode == 1) {
                        Swal.fire({
                            title: resp.ErrorMessage,
                            didOpen: function () {
                                //Swal.showLoading()
                                setTimeout(function () {
                                    Swal.close()
                                }, 2000)
                            }
                        })
                    } else if (resp.StatusCode == 3) {
                        //window.location.replace(resp.RedirectUrl);
                    }
                }
            },
            error: function (res) {
                //location.reload();
            }
        });
    });

});
