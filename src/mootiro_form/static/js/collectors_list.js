/********** Auxiliar functions **********/
// TODO: Remove this function when JS translation is merged
String.prototype.interpol = function () {
    // String interpolation for format strings like "Item {0} of {1}".
    // May receive strings or numbers as arguments.
    // For usage, see the test function below.
    var args = arguments;
    try {
        return this.replace(/\{(\d+)\}/g, function () {
            //
            // The replaceme
            // nt string is given by the nth element in the list,
            // where n is the second group of the regular expression:
            return args[arguments[1]];
        });
    } catch (e) {
        if (window.console) console.log(['Exception on interpol() called on',
            this, 'with arguments', arguments]);
        throw(e);
    }
}

function dictToString(d) {
    // Turn something like a colander errors dict into a user-friendly string.
    s = '';
    for (i in d) {
        v = d[i];
        if (typeof(v)==='string' && v)
            s += '{0}: {1}\n'.interpol(i, v);
    }
    return s;
}

function checkRadioButton(name, val, where) {
    $("input[name={0}][value={1}]".interpol(name, val), where).click();
}

// TODO: Move this function to a new global.js lib
function onHoverSwitchImage(selector, where, hoverImage, normalImage) {
    $(selector, where).live('mouseover mouseout', function(event) {
        if (event.type == 'mouseover') {
            $(this).attr({src: hoverImage});
        } else {
            $(this).attr({src: normalImage});
        }
    });
}


/********** Collectors list table **********/
$.get(route_url('root') + 'static/jquery-templates/collectors_list.tmpl.html',
    function (fragment) {
        $('body').append(fragment);
        $.template("collectorsTable", $('#collectorsTable'));
        $.template("collectorRow", $('#collectorRow'));
        $.tmpl("collectorsTable").appendTo('#middle');
        $.tmpl("collectorRow", collectors_json).appendTo('#collectorsRows');
        setupCollectorsList();
    }
);

function setupCollectorsList () {
    var $listTable = $('#CollectorsListTable');
    var $EmptyListMessage = $('#EmptyListMessage');
    var c_num = $listTable.find("tbody tr").length;

    if (c_num == 0) {
        $listTable.hide();
        $EmptyListMessage.show();
    } else {
        $listTable.show();
        $EmptyListMessage.hide();

        $listTable.find('tr td:nth-child(2n)').addClass('darker');
        $listTable.find('thead th:nth-child(2n)').addClass('darker');
        onHoverSwitchImage('.editIcon', $listTable,
            route_url('root') + 'static/img/icons-root/editHover.png',
            route_url('root') + 'static/img/icons-root/edit.png');
        onHoverSwitchImage('.copyIcon', $listTable,
            route_url('root') + 'static/img/icons-root/copyHover.png',
            route_url('root') + 'static/img/icons-root/copy.png');
        onHoverSwitchImage('.deleteIcon', $listTable,
            route_url('root') + 'static/img/icons-root/deleteHover.png',
            route_url('root') + 'static/img/icons-root/delete.png');
    }
}

$('.editIcon').live('click', function () {
    var id = $(this).closest('tr').attr('id').split('-')[1];
    manager.editPublicLink(id);
});
$('.deleteIcon').live('click', function () {
    var id = $(this).closest('tr').attr('id').split('-')[1];
    manager.deleteCollector(id);
});


/********** Tabs **********/
function Tabs(tabs, contents) {
    $(contents).hide();
    var instance = this;
    this.to = function (tab) { // Most important method, switches to a tab.
        $(contents).hide();
        $(tabs).removeClass("selected");
        $(tab).addClass("selected");
        $($(tab).children().attr("href")).show();
    };
    $(tabs).click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
    // first shown tab is the first matched element in DOM tree
    this.to($(tabs)[0]);
}


/********** Dialog windows **********/
$('#btnNewPublicLink').click(function (e) {
    manager.editPublicLink('new');
});
$('#btnNewWebsiteCode').click(function (e) {
    manager.editWebsiteCode('new');
});

manager = {
    $dialog: $('#CollectorsEditionDialog'),
    currentId: 'new',  // holds the ID of the collector currently being edited
    showPublicLinkDialog: function (d) {
        manager.setPublicLinkForm(d);
        if (manager.currentId == 'new') {
            dialogTitle = "New collector: public link";
        } else {
            dialogTitle = "Public link: " + d.name;
        }
        var o = {title: dialogTitle,
                 saveAction: manager.savePublicLink,
                 closeAction: manager.closeDialog,
                 collectorPrefix: "pl"};
        manager.showCollectorDialog(o);
    },
    showWebsiteCodeDialog: function (d) {
        manager.setWebsiteCodeForm(d);
        if (manager.currentId == 'new') {
            dialogTitle = "New collector: website code";
        } else {
            dialogTitle = "Website code: " + d.name;
        }
        var o = {title: dialogTitle,
                 saveAction: manager.saveWebsiteCode,
                 closeAction: manager.closeDialog,
                 collectorPrefix: "wc"};
        
        // Code type Tabs construction
        var where = $('#WebsiteCodeTypes');
        var $tabs = $('li[id^=wc_type_tab]', where);
        var $panels = $('div[id^=wc_type_panel]', where);
        tabs = new Tabs($tabs, $panels);

        manager.showCollectorDialog(o);
    },
    showCollectorDialog: function (o) { // title, saveAction, closeAction, collectorPrefix
        // TODO: Remove after implementing more restrictions.
        enableOrDisableRestrictionFields();
        validatePublishDates(); // In order to update the error messages.

        manager.$dialog.dialog({
            width: 'auto',
            minHeight:'300px',
            title: o.title,
            modal: true,
            buttons: [
                {text: 'Save', click: o.saveAction},
                {text: 'Cancel', click: o.closeAction}
            ]
        });

        // Tabs construction
        var where = manager.$dialog;
        var $tabs = $('li[id^={0}_tab], li[id^=shared_tab]'.interpol(o.collectorPrefix), where);
        var $panels = $('div[id^={0}_panel], div[id^=shared_panel]'.interpol(o.collectorPrefix), where);
        $('.panel', where).hide();
        $('.tab', where).hide();
        $($tabs).show();
        tabs = new Tabs($tabs, $panels);

        $('#name', where).focus();
    },
    setPublicLinkForm: function (d) {
        // Set the public url and link for saved collectors
        if (manager.currentId != 'new') {
            var where = manager.$dialog;
            var url;
            url = route_url('entry_form_slug',
                {'action': 'view_form', 'slug': d.slug});
            if (url[0] == '/') {
                url = "{0}//{1}{2}".interpol(window.location.protocol,
                    window.location.host, url);
            }
            link='<a href="{0}">Click to fill out my form.</a>'.interpol(url);
            $('#pl_url', where).val(url);
            $('#pl_link', where).val(link);
        }

        manager.setCollectorForm(d);
    },
    setWebsiteCodeForm: function (d) {
        var where = manager.$dialog;
        var code_invitation, code_survey, code_embed, code_full_page;
        
        // Sets website codes
        if (manager.currentId == 'new') {
            code_invitation = code_survey = code_embed = code_full_page =
                'Save the collector first to get the respective code in here.';
            $('#wc_hide_survey').attr('checked', false);
        } else {
            var hide_survey = $('#wc_hide_survey').attr('checked');
            // TODO: create conditional html codes
        }
        
        $('#wc_invitation').text(code_invitation);
        $('#wc_survey').text(code_survey);
        $('#wc_embed').text(code_embed);
        $('#wc_full_page').text(code_full_page);

        manager.setCollectorForm(d);
    },
    setCollectorForm: function (d) {
        var where = manager.$dialog;
        
        $('#name', where).val(d.name);
        $('#thanks_message', where).val(d.thanks_message);
        $('#thanks_url', where).val(d.thanks_url);
        $('#start_date', where).val(d.start_date);
        $('#end_date', where).val(d.end_date);
        $('#message_before_start', where).val(d.message_before_start);
        $('#message_after_end', where).val(d.message_after_end);
        checkRadioButton('on_completion', d.on_completion, where);
        $('#limit_by_date', where).attr('checked', (d.limit_by_date));
    },
    editPublicLink: function (id) {
        var o = {defaultName: 'My public link collector',
                 showAction: this.showPublicLinkDialog}
        manager.editCollector(id, o);
    },
    editWebsiteCode: function (id) {
        var o = {defaultName: 'My website code collector',
                 showAction: this.showWebsiteCodeDialog}
        manager.editCollector(id, o);
    },
    editCollector: function(id, o) { //
        this.currentId = id;
        var url = route_url('collector',
            {'form_id': this.formId, 'id': id, action: 'as_json'});
        if (id == 'new') {
            o.showAction({
                name: o.defaultName,
                on_completion: 'msg',
                thanks_message: 'Thanks for filling in my form!'
            });
        } else {
            $.get(url).success(o.showAction)
            .error(function (d) {
                alert("Sorry, could not retrieve the data for this collector."
                    + "\nStatus: " + d.status);
            });
        }
    },
    deleteCollector: function (id) {
        this.currentId = id;

        $('#confirm-deletion-'+id).dialog({
            modal: true,
            buttons: {
                "Cancel": function () {
                    $(this).dialog("close");
                },
                "Delete": function() {
                    $(this).dialog("close");
                    var url = route_url('collector',
                        {'form_id': this.formId, 'id': id, action: 'delete'});
                    $.post(url)
                    .success(function (data) {
                        if (data.error) {
                            alert(error);
                        } else {
                            $('#collector-' + manager.currentId).remove();
                            setupCollectorsList();
                            manager.currentId = 'new';
                        }
                    })
                    .error(function (data) {
                        alert("Sorry, could NOT delete this collector."
                            + "\nStatus: " + d.status);
                    });
                }
            }
        });
    },
    closeDialog: function (e) {
        manager.$dialog.dialog('close');
    },
    savePublicLink: function (e) {
        $.post(route_url('collector', {action: 'save_public_link',
            id: manager.currentId, form_id: manager.formId}),
            $('#publicLinkForm').serialize()
        ).success(function (d) {
            if (d.id) {  // success, saved
                // Considering a new public link, add it to the list
                if (manager.currentId != 'new') {
                    var $collectorRow = $("#collector-" + manager.currentId);
                    $.tmpl("collectorRow", d).insertAfter($collectorRow);
                    $collectorRow.remove();
                } else {
                    $.tmpl("collectorRow", d).appendTo('#collectorsRows');
                }
                setupCollectorsList();
                manager.editPublicLink(d.id);
            } else {  // d contains colander errors
                if (d.start_date || d.end_date || d['']) {
                    tabs.to('#shared_tab-Restrictions');
                    $('#StartDateError').text(
                        d.start_date || '');
                    $('#EndDateError').text(
                        d.end_date || '');
                    $('#IntervalError').text(
                        d[''] || '');
                    alert("Sorry, your alterations have NOT been saved."
                          + "\n Please corect the errors as proposed in the"
                          + " highlighted text.");
                } else {
                    if (d.thanks_url || d.thanks_message) {
                        tabs.to('#shared_tab-Settings');
                    }
                    else {
                        tabs.to('#pl_tab-PublicLink');
                    }
                    alert("Sorry, the collector was not saved. Errors:\n" +
                    dictToString(d));}
            }
        }).error(function (d) {
            alert("Sorry, the collector was not saved. Status: " + d.status);
        });
    },
    saveWebsiteCode: function (e) {
        alert("saveWebsiteCode");
    },
    saveCollector: function (e) {
        alert("saveCollector");
    }
};

$('#limit_by_date').click(enableOrDisableRestrictionFields);

// TODO: Remove the function after implementing more restrictions. It is no 
// longer necessary after more than one restriction is implemented. Then the 
// fields will be collapsable and thereby not accessable by the user.
function enableOrDisableRestrictionFields(e) {
    var dates = $('#start_date, #end_date, #message_before_start,'
                  + ' #message_after_end');
    if ($('#limit_by_date').attr('checked')) {
        $.datepicker._enableDatepicker(dates[0])
        $.datepicker._enableDatepicker(dates[1])
        dates.attr('readonly', false);
    }
    else {
        $.datepicker._disableDatepicker(dates[0])
        $.datepicker._disableDatepicker(dates[1])
        dates.attr('readonly', true);
        dates.attr('disabled', false);
    }
}

// The start and end date datetimepicker. First line is
// necessary to disable automated positioning of the widget.
$.extend($.datepicker,
    {_checkOffset: function (inst,offset,isFixed) {return offset;}});
$('#start_date').datetimepicker({
    dateFormat: 'yy-mm-dd',
    timeFormat: 'hh:mm',
    hour: 00,
    minute: 00,
    beforeShow: function(input, inst) {
        inst.dpDiv.addClass('ToTheRight');
    }
});
$('#end_date').datetimepicker({
    dateFormat: 'yy-mm-dd',
    timeFormat: 'hh:mm',
    hour: 23,
    minute: 59,
    beforeShow: function(input, inst) {
        inst.dpDiv.addClass('ToTheRight');
    }
});

// validate the format of a datestring as isoformat.
function dateValidation(string) {
    if (string) {
        var date = Date.parseExact(string, "yyyy-MM-dd HH:mm");
        if (date) {
            return {date:date, valid:true};
        } else {
            return {msg:
                "Please enter a valid date of the format yyyy-mm-dd hh:mm",
                valid: false};
        }
    } else {
        return {valid: true};
    }
}

// validate whether start date is before end date
function intervalValidation(start_date, end_date) {
    if (start_date < end_date) {
        return "";
    }
    else if (start_date > end_date) {
        return "The start date must be before the end date";
    } else {
        return "";
    }
}

function validatePublishDates() {
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();

    var start_date_dict = dateValidation(start_date);
    var end_date_dict = dateValidation(end_date);
    var valid_start_date = start_date_dict['valid'];
    var valid_end_date = end_date_dict['valid'];
    // validate start date
    if (valid_start_date) {
        $('#StartDateError').text('');
    } else {
        $('#StartDateError').text(start_date_dict['msg']);
    }
    // validate end date
    if (valid_end_date) {
        end_date = end_date_dict['date'];
        if (end_date < new Date()) {
            $('#EndDateError').text('The end date must be in the future');
        }
        else {
            $('#EndDateError').text('');
        }
    } else {
        $('#EndDateError').text(end_date_dict['msg']);
    }
    // validate interval
    if (valid_start_date) {
        start_date = start_date_dict['date'];
        if (valid_end_date) {
          $('#IntervalError').text(intervalValidation(start_date, end_date));
        }
    } else {
        $('#IntervalError').text('');
    }
}

// validate publish dates in realtime
$('#start_date, #end_date').keyup(validatePublishDates).change(validatePublishDates);
