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


function Tabs(tabs, contents) {
    $(contents).hide();
    $(contents + ":first").show();
    $(tabs + " li:first").addClass("selected");
    var instance = this;
    this.to = function (tab) { // Most important method, switches to a tab.
        $(contents).hide();
        $(tabs + " li").removeClass("selected");
        $(tab).addClass("selected");
        $($(tab).children().attr("href")).show();
    };
    $(tabs + " li").click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
}
tabs = new Tabs('#publicLinkDialog .menu', '#publicLinkDialog .Panel');


function dictToString(d) {
    // Turn something like a colander errors dict into a user-friendly string.
    s = '';
    for (i in d) {
        v = d[i];
        if (typeof(v)==='string' && v)
            s += '[0]: [1]\n'.interpol(i, v);
    }
    return s;
}
function checkRadioButton(name, val, where) {
    $("input[name=[0]][value=[1]]".interpol(name, val), where).click();
}


manager = {
    $publicLinkDialog: $('#publicLinkDialog'),
    currentId: 'new',  // holds the ID of the collector currently being edited
    showPublicLinkDialog: function (d) {
        // Populate textboxes
        var where = manager.$publicLinkDialog;
        $('#pl_name', where).val(d.name);
        // Make the public url and link
        var url;
        var linktext = _("Click to fill out my form.");
        if (manager.currentId != 'new') {
            url = route_url('entry_form_slug',
                {'action': 'view_form', 'slug': d.slug});
            if (url[0] == '/') {
                url = "[0]//[1][2]".interpol(window.location.protocol,
                    window.location.host, url);
            }
            linktext = '<a href="[0]">[1]</a>'.interpol(url, linktext);
        } else {
            url = '';
            linktext = '';
        }
        $('#pl_url', where).val(url);
        $('#pl_link', where).val(linktext);
        $('#pl_thanks_message', where).val(d.thanks_message);
        $('#pl_thanks_url', where).val(d.thanks_url);
        $('#pl_start_date', where).val(d.start_date);
        $('#pl_end_date', where).val(d.end_date);
        $('#pl_message_before_start', where).val(d.message_before_start);
        $('#pl_message_after_end', where).val(d.message_after_end);
        // Populate checkbox
        $('#pl_limit_by_date', where).attr('checked', d.limit_by_date);
        // TODO: Remove after implementing more restrictions.
        enableOrDisableRestrictionFields();
        // Populate radiobuttons, too
        checkRadioButton('on_completion', d.on_completion, where);

        validatePublishDates();
        // In order to update the error messages.

        // Dialog setup
        if (manager.currentId == 'new') {
            dialogTitle = _("New collector: public link");
        } else {
            dialogTitle = _("Public link: [0]").interpol(d.name);
        }
        manager.$publicLinkDialog.dialog({
            width: 'auto',
            minHeight:'300px',
            title: dialogTitle,
            modal: true,
            buttons: [
                {text: _('Save'), click: manager.savePublicLink},
                {text: _('Cancel'), click: manager.closePublicLink}
            ]
        });
        // Dialog default view
        tabs.to('#TabPublicLink');
        $('#pl_name', where).focus();
    },
    editPublicLink: function (id) {
        this.currentId = id;
            var url = route_url('collector',
            {'form_id': this.formId, 'id': id, action: 'as_json'});
        if (id == 'new') {
            this.showPublicLinkDialog({
                name: _('My public link collector'),
                on_completion: 'msg',
                message_before_start: _('Sorry, you cannot fill in the form,'
                                      + ' yet. You can fill in the form from '
                                      + 'the following date on: {start date}'),
                message_after_end: _('Sorry, the period for filling in the form'
                                   + ' has elapsed on {end date}.'),
                thanks_message: _('Thanks for filling in my form!')
            });
        } else {
            var t = _("Sorry, could not retrieve the data for this collector.");
            $.get(url).success(this.showPublicLinkDialog)
            .error(function (d) {
                alert(t + "\nStatus: " + d.status);
            });
        }
    },
    deletePublicLink: function (id) {
        this.currentId = id;

        $('#confirm-deletion-' + id).dialog({
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
                        alert(_("Sorry, could NOT delete this collector.")
                            + "\nStatus: " + d.status);
                    });
                }
            }
        });
    },
    closePublicLink: function (e) {
        manager.$publicLinkDialog.dialog('close');
    },
    tNotSaved: _("Sorry, the collector has NOT been saved."),
    tCorrect: _("Please correct the errors as proposed in the highlighted text."),
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
                    tabs.to('#TabRestrictions');
                    $('#plStartDateError').text(
                        d.start_date || '');
                    $('#plEndDateError').text(
                        d.end_date || '');
                    $('#plIntervalError').text(
                        d[''] || '');
                    alert(manager.tNotSaved + '\n' + manager.tCorrect);
                } else {
                    if (d.thanks_url || d.thanks_message) {
                        tabs.to('#TabSettings');
                    } else {
                        tabs.to('#TabPublicLink');
                    }
                    alert("[0] [1]\n[2]".interpol(manager.tNotSaved,
                        _("Errors:"), dictToString(d)));
                }
            }
        }).error(function (d) {
            alert(tNotSaved + "\nStatus: " + d.status);
        });
    }
};


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


$('#btnNewPublicLink').live('click', function (e) {
    manager.editPublicLink('new');
});
$('.editIcon').live('click', function () {
    var id = $(this).closest('tr').attr('id').split('-')[1];
    manager.editPublicLink(id);
});
$('.deleteIcon').live('click', function () {
    var id = $(this).closest('tr').attr('id').split('-')[1];
    manager.deletePublicLink(id);
});
$('#pl_limit_by_date').live('click', enableOrDisableRestrictionFields);


// TODO: Remove the function after implementing more restrictions. It is no
// longer necessary after more than one restriction is implemented. Then the
// fields will be collapsable and thereby not accessible by the user.
function enableOrDisableRestrictionFields(e) {
    var dates = $('#pl_start_date, #pl_end_date, #pl_message_before_start,'
                  + ' #pl_message_after_end');
    if ($('#pl_limit_by_date').attr('checked')) {
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


function dateValidation(string) { // validate the format of a date as iso
    if (string) {
        var date = Date.parseExact(string, "yyyy-MM-dd HH:mm");
        if (date) {
            return {date:date, valid:true};
        } else {
            return {msg:
                _("Please enter a valid date in the format yyyy-mm-dd hh:mm"),
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
        return _("The start date must be before the end date.");
    } else {
        return "";
    }
}

function validatePublishDates() {
    var start_date = $('#pl_start_date').val();
    var end_date = $('#pl_end_date').val();

    var start_date_dict = dateValidation(start_date);
    var end_date_dict = dateValidation(end_date);
    var valid_start_date = start_date_dict['valid'];
    var valid_end_date = end_date_dict['valid'];
    // validate start date
    if (valid_start_date) {
        $('#plStartDateError').text('');
    } else {
        $('#plStartDateError').text(start_date_dict['msg']);
    }
    // validate end date
    if (valid_end_date) {
        end_date = end_date_dict['date'];
        if (end_date < new Date()) {
           $('#plEndDateError').text(_('The end date must be in the future.'));
        }
        else {
           $('#plEndDateError').text('');
        }
    } else {
        $('#plEndDateError').text(end_date_dict['msg']);
    }
    // validate interval
    if (valid_start_date) {
        start_date = start_date_dict['date'];
        if (valid_end_date) {
          $('#plIntervalError').text(intervalValidation(start_date, end_date));
        }
    } else {
        $('#plIntervalError').text('');
    }
}

// validate publish dates in realtime
$('#pl_start_date, #pl_end_date').live('keyup change', validatePublishDates);

$(function () {
    // The start and end date datetimepicker. First line is
    // necessary to disable automated positioning of the widget.
    $.extend($.datepicker,
        {_checkOffset: function (inst,offset,isFixed) {return offset;}});
    $('#pl_start_date').datetimepicker({
        dateFormat: 'yy-mm-dd',
        timeFormat: 'hh:mm',
        hour: 00,
        minute: 00,
        beforeShow: function(input, inst) {
            inst.dpDiv.addClass('ToTheRight');
        }
    });
    $('#pl_end_date').datetimepicker({
        dateFormat: 'yy-mm-dd',
        timeFormat: 'hh:mm',
        hour: 23,
        minute: 59,
        beforeShow: function(input, inst) {
            inst.dpDiv.addClass('ToTheRight');
        }
    });
});
