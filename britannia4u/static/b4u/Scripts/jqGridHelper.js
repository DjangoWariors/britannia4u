var Editable;
var lastSel;
var ddd;
var url = '';
var araID;
var regID;

function decodeErrorMessage(jqXHR, textStatus, errorThrown) {
    return $.parseJSON(jqXHR.responseText);
};

function afterSaveFuncAfterEdit(rowId, response) {
    var data = $.parseJSON(response.responseText);
    if (data.error == true) {
        jQuery("#list").jqGrid().editRow(rowId);
    }
    else {
        alert(data.message);
        jQuery("#list").jqGrid().trigger("reloadGrid");
        return false;
    }
};

function AfterErrorFunc(rowId, response) {
    $('#notification').delay(0).fadeIn('fast');
    $('#notification').html('');
    $('#notification').html('<div class="ui-widget"><div class="ui-state-error ui-corner-all" style="padding: 0 .7em;"><p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span><strong>Alert: </strong>' +
                        $.parseJSON(response.responseText) + '</p></div></div>');
    //$('#notification').delay(5000).fadeOut('slow');
    return true;
};

function PopulateDDList(itemName, data) {
    if (data.length > 0) {
        var listItems = [];
        for (var key in data) {
            if (data[key].Selected) {
                listItems.push('<option selected=selected value="' +
                                data[key].Value + '">' + data[key].Text
                                + '</option>');
            } else {
                listItems.push('<option value="' +
                                data[key].Value + '">' + data[key].Text
                                + '</option>');
            }
        }
        $('#' + itemName).empty();
        $('#' + itemName).append(listItems.join(''));
        return true;
    }
    else {
        $('#' + itemName).empty();
        return false;
    }
}

function PopulateSelectWithData(itemName, data) {
    if (data.length > 0) {
        var listItems = [];
        for (var key in data) {
            if (data[key].Selected) {
                listItems.push('<option selected=selected value="' +
                                data[key].Value + '">' + data[key].Text
                                + '</option>');
            } else {
                listItems.push('<option value="' +
                                data[key].Value + '">' + data[key].Text
                                + '</option>');
            }
        }
        $('#' + itemName).empty();
        $('#' + itemName).append(listItems.join(''));
        return true;
    }
    else {
        $('#' + itemName).empty();
        return false;
    }
}

function PopulateSelectWithURL(itemName, url) {
    var jqxhr = jQuery.ajax({ url: url, async: false, type: 'POST' });
    var data = jQuery.parseJSON(jqxhr.responseText);
    PopulateSelectWithData(itemName, data);
}
function BS(data) {
    var response = jQuery.parseJSON(data);
    var s = '<select width="100%">';
    if (response && response.length) {
        for (var i = 0, l = response.length; i < l; i++) {
            var ri = response[i];
            s += '<option value="' + ri.Value + '">' + ri.Text + '</option>';
        }
    }
    return s + "</select>";
}

function OSR(id) {
    lastSel = id;
}

function GC() {
    var top_rowid = jQuery('#list tbody:first-child tr').eq(1).attr('id'); //jQuery('#list tbody:first-child tr:first').attr('amx_id');
    //jQuery("#list").jqGrid('setSelection', top_rowid, false);
    lastSel = top_rowid;
}

function LE(jqXHR, textStatus, errorThrown) {
    $('#notification').delay(0).fadeIn('fast');
    $('#notification').html('');
    $('#notification').html('<div class="ui-widget"><div class="ui-state-error ui-corner-all" style="padding: 0 .7em;"><p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span><strong>Alert: </strong>' +
                                        decodeErrorMessage(jqXHR, textStatus, errorThrown) + '</p></div></div>');
    //$('#notification').delay(5000).fadeOut('slow');
}

function LC(data) {
    $('#notification').html('');
}

function resize_grid() {
    $("#list").fluidGrid({ base: '#grid_wrapper', offset: -5 });
}

function CustomOnLoad() {
    jQuery("#list").navGrid("#pager", { edit: false, add: false, del: false, deltext: '', refresh: true, refreshtext: '', search: true, searchtext: '' }, {}, {}, {}, { multipleSearch: true });
    jQuery("#list").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, defaultSearch: 'cn' });
    jQuery("#list").inlineNav("#pager", { add: true, addtext: '', edit: true, edittext: '', editicon: "ui-icon-pencil",
        editParams: {
            keys: false,
            aftersavefunc: afterSaveFuncAfterEdit,
            restoreAfterError: false,
            errorfunc: AfterErrorFunc,
            afterrestorefunc: function () { $('#notification').fadeOut('fast') }
        }
    });
    resize_grid();
    $(window).resize(resize_grid);
    jQuery("#list").navGrid("#pager").navButtonAdd('#pager', { caption: "Filter", title: "Toggle Searching Toolbar",
        buttonicon: 'ui-icon-pin-s',
        onClickButton: function () { jQuery("#list")[0].toggleToolbar(); }
    });
    jQuery("#list")[0].toggleToolbar();
}

function CustomOnLoad(Nav, Filter, Inline) {
    if (Nav)
        jQuery("#list").navGrid("#pager", { edit: false, add: false, del: false, deltext: '', refresh: true, refreshtext: '', search: true, searchtext: '' }, {}, {}, {}, { multipleSearch: true });
    if (Filter) {
        jQuery("#list").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, defaultSearch: 'cn' });
        jQuery("#list").navGrid("#pager").navButtonAdd('#pager', { caption: "Filter", title: "Toggle Searching Toolbar",
            buttonicon: 'ui-icon-pin-s',
            onClickButton: function () { jQuery("#list")[0].toggleToolbar(); }
        });
        jQuery("#list")[0].toggleToolbar();
    }
    if (Inline)
        jQuery("#list").inlineNav("#pager", { add: true, addtext: '', edit: true, edittext: '', editicon: "ui-icon-pencil",
            editParams: {
                keys: false,
                aftersavefunc: afterSaveFuncAfterEdit,
                restoreAfterError: false,
                errorfunc: AfterErrorFunc,
                afterrestorefunc: function () { $('#notification').fadeOut('fast') }
            }
        });
    resize_grid();
    $(window).resize(resize_grid);
}

function CustomOnLoad(Nav, Filter, Inline, InlineEdit) {
    if (Nav)
        jQuery("#list").navGrid("#pager", { edit: false, add: false, del: false, deltext: '', refresh: true, refreshtext: '', search: true, searchtext: '' }, {}, {}, {}, { multipleSearch: true });
    if (Inline)
        jQuery("#list").inlineNav("#pager", { add: true, addtext: '', edit: InlineEdit, edittext: '', editicon: "ui-icon-pencil",
            editParams: {
                keys: false,
                aftersavefunc: afterSaveFuncAfterEdit,
                restoreAfterError: false,
                errorfunc: AfterErrorFunc,
                afterrestorefunc: function () { $('#notification').fadeOut('fast') }
            }
        });
    if (Filter) {
        jQuery("#list").jqGrid('filterToolbar', { stringResult: true, searchOnEnter: false, defaultSearch: 'cn' });
        jQuery("#list").navGrid("#pager").navButtonAdd('#pager', { caption: "Filter", title: "Toggle Searching Toolbar",
            buttonicon: 'ui-icon-pin-s',
            onClickButton: function () { jQuery("#list")[0].toggleToolbar(); }
        });
        jQuery("#list")[0].toggleToolbar();
    }
    resize_grid();
    $(window).resize(resize_grid);
}

function Notify(message, error) {
    if (error) {
        $('#notification').delay(0).fadeIn('fast');
        $('#notification').html('');
        $('#notification').html('<div class="ui-widget"><div class="ui-state-error ui-corner-all" style="padding: 0 .7em;"><p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span><strong>Alert: </strong>' +
                                        message + '</p></div></div>');
        //$('#notification').delay(5000).fadeOut('slow');
    }
    else {
        $('#notification').delay(0).fadeIn('fast');
        $('#notification').html('');
        $('#notification').html('<div class="ui-widget"><div class="ui-state-highlight ui-corner-all" style="padding: 0 .7em;"><p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span><strong>Alert: </strong>' +
                                        message + '</p></div></div>');
        $('#notification').delay(5000).fadeOut('slow');
    }
}

jQuery.fn.center = function () {
    this.css("position", "absolute");
    this.css("top", Math.max(0, (($(window).height() - this.outerHeight()) / 2) +
                                                $(window).scrollTop()) + "px");
    this.css("left", Math.max(0, (($(window).width() - this.outerWidth()) / 2) +
                                                $(window).scrollLeft()) + "px");
    return this;
}

function PopulateSelectWithDataName(itemName, data) {
    if (data.length > 0) {
        var listItems = [];
        for (var key in data) {
            if (data[key].Selected) {
                listItems.push('<option selected=selected value="' +
                                data[key].Value + '">' + data[key].Text
                                + '</option>');
            } else {
                listItems.push('<option value="' +
                                data[key].Value + '">' + data[key].Text
                                + '</option>');
            }
        }
        $(itemName).empty();
        $(itemName).append(listItems.join(''));
        return true;
    }
    else {
        $(itemName).empty();
        return false;
    }
}


function PopulateSelectWithName(itemName, data) {
    if (data.length > 0) {
        var listItems = [];
        for (var key in data) {
            if (data[key].Selected) {
                listItems.push('<option selected=selected value="' +
                    data[key].Value + '">' + data[key].Text
                    + '</option>');
            } else {
                listItems.push('<option value="' +
                    data[key].Value + '">' + data[key].Text
                    + '</option>');
            }
        }

        $(itemName).empty();
        $(itemName).append(listItems.join(''));
        return true;
    }
    else {
        $(itemName).empty();
        return false;
    }
}

function NumbersOnly(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode
    if (charCode > 31 && (charCode < 48 || charCode > 57))
        return false;

    return true;
}

function DecimalOnly(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    else {
        var dp = 0;
        var CHAR_AFTER_DP = 2;

        if (evt.target) {
            if ((dp = evt.target.value.indexOf(".")) > -1) {
                if (charCode == 46)
                    return false;
                else {
                    if (evt.target.value.length - dp <= CHAR_AFTER_DP)
                        return true;
                    else
                        return false;
                }
            }
        }
        else {
            if ((dp = evt.srcElement.value.indexOf(".")) > -1) {
                if (charCode == 46)
                    return false;
                else {
                    if (evt.srcElement.value.length - dp <= CHAR_AFTER_DP)
                        return true;
                    else
                        return false;
                }
            }
        }
    }
    return true;
}

jQuery.fn.center = function () {
    this.css("position", "absolute");
    this.css("top", Math.max(0, (($(window).height() - $(this).outerHeight()) / 2) +
                                                $(window).scrollTop()) + "px");
    this.css("left", Math.max(0, (($(window).width() - $(this).outerWidth()) / 2) +
                                                $(window).scrollLeft()) + "px");
    return this;
}

function myFunction() {
    var element = document.getElementById("myDIV");
    element.classList.toggle("mob-profile-1");
}

  function ContinueShopping() {
      window.location = BaseURL + 'ProductCatalogue';
}


