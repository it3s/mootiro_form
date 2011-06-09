/********** Auxiliar functions **********/
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


/********** Collectors list table **********/
$.get(jurl('static') + '/jquery-templates/collectors_list.tmpl.html',
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
            jurl('static') + '/img/icons-root/editHover.png',
            jurl('static') + '/img/icons-root/edit.png');
        onHoverSwitchImage('.copyIcon', $listTable,
            jurl('static') + '/img/icons-root/copyHover.png',
            jurl('static') + '/img/icons-root/copy.png');
        onHoverSwitchImage('.deleteIcon', $listTable,
            jurl('static') + '/img/icons-root/deleteHover.png',
            jurl('static') + '/img/icons-root/delete.png');
    }
}

$('.editIcon').live('click', function () {
    var arr = $(this).attr('id').split('-');
    var type = arr[1];
    var id = arr[2];

    if (type == 'public_link')
        manager.editPublicLink(id);
    else if (type == 'website_code')
        manager.editWebsiteCode(id);
});
$('.deleteIcon').live('click', function () {
    var arr = $(this).attr('id').split('-');
    var id = arr[2];
    manager.deleteCollector(id);
});


/********** Tabs **********/
function Tabs(tabs, contents) {
    $(contents).hide();
    var instance = this;
    this.to = function (tab) { // Most important method, switches to a tab.
        $(tabs).removeClass("selected");
        $(contents).removeClass("selected").hide();

        var tab_content = $(tab).children().attr("href");
        $(tab).addClass("selected");
        $(tab_content).addClass("selected").show();
    };
    $(tabs).click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
    // first shown tab is the first matched element in DOM tree
    this.to($(tabs)[0]);
}


/********** Dialog windows **********/
$('#btnNewPublicLink').live('click', function (e) {
    manager.editPublicLink('new');
});
$('#btnNewWebsiteCode').live('click', function (e) {
    manager.editWebsiteCode('new');
});

manager = {
    $dialog: $('#CollectorsEditionDialog'),
    currentId: 'new',  // holds the ID of the collector currently being edited
    // formId: this variable is set in the genshi template
    showPublicLinkDialog: function (d) {
        var dialogTitle;
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
        var dialogTitle;
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
        manager.showCollectorDialog(o);

        // Code type Tabs construction
        var where = $('#WebsiteCodeTypes');
        var $tabs = $('li[id^=wc_type_tab]', where);
        var $panels = $('div[id^=wc_type_panel]', where);
        var $actual_tab = $('li[id^=wc_type_tab].selected', where);
        var wc_type_Tabs = new Tabs($tabs, $panels);
        if (manager.currentId == 'new') {
            wc_type_Tabs.to($tabs[0]);
        } else if ($actual_tab[0]) {
            wc_type_Tabs.to($actual_tab);
        }

        $('#embed_frame_height_errors', where).text('');
        $('#invitation_popup_width_errors', where).text('');
        $('#invitation_popup_height_errors', where).text('');
    },
    showCollectorDialog: function (o) { // title, saveAction, closeAction, collectorPrefix
        // TODO: Remove after implementing more restrictions.
        enableOrDisableRestrictionFields();
        validatePublishDates(); // In order to update the error messages.

        manager.$dialog.dialog({
            width: 'auto',
            minHeight:'auto',
            title: o.title,
            modal: true,
            buttons: [
                {text: _('Save'), id: 'saveBtn', click: o.saveAction},
                {text: _('Cancel'), id: 'cancelBtn', click: o.closeAction}
            ]
        });
        $("#cancelBtn").button();
        $("#saveBtn").button({icons: {primary:'ui-icon-custom-check'}});

        // Tabs construction
        var where = manager.$dialog;
        var $tabs = $('li[id^=[0]_tab], li[id^=shared_tab]'.interpol(o.collectorPrefix), where);
        var $panels = $('div[id^=[0]_panel], div[id^=shared_panel]'.interpol(o.collectorPrefix), where);
        $('.panel', where).hide();
        $('.tab', where).hide();
        $($tabs).show();
        tabs = new Tabs($tabs, $panels);

        $('#[0]_name'.interpol(o.collectorPrefix), where).focus();
    },
    setPublicLinkForm: function (d) {
        var where = manager.$dialog;
        $('#pl_name', where).val(d.name);
        // Set the public url and link for saved collectors
        var url, linktext;

        if (manager.currentId == 'new') {
            url = _("Save to create the web link.");
            linktext = _("Save to create the HTML code.");
        } else {
            var text = _("Click to fill out my form.");
            url = schemeDomainPort +
                jurl('entry_form_slug', 'view_form', 'slug', d.slug);
            linktext = '<a href="[0]">[1]</a>'.interpol(url, text);
        }

        $('#pl_url', where).val(url);
        $('#pl_link', where).val(linktext);
        manager.setCollectorForm(d);
    },
    setWebsiteCodeForm: function (d) {
        var where = manager.$dialog;
        var code_invitation, code_survey, code_embed, code_full_page;

        $('#wc_name', where).val(d.name);

        var wi = d.invitation_popup_width || "400";
        $('#invitation_popup_width', where).val(wi);
        var hi = d.invitation_popup_height || "100";
        $('#invitation_popup_height', where).val(hi);

        var he = d.embed_frame_height || "500";
        $('#embed_frame_height', where).val(he);

        var im = d.invitation_message || "We are making a survey. Do you want to answer it now?"; // default message
        $('#invitation_message', where).val(im);

        // Sets website codes
        if (manager.currentId == 'new') {
            code_invitation = code_survey = code_embed = code_full_page =
                _('Save the collector first to get the respective code in here.');
            //$('#wc_hide_survey').attr('checked', false);
        } else {
            var url;
            // TODO: use hide_survey conditionally in the code generation below
            //var hide_survey = $('#wc_hide_survey').attr('checked');
            url = schemeDomainPort + jurl('collector_slug', 'popup_invitation', 'slug', d.slug);
            code_invitation = "<script type='text/javascript' src='[0]'></script>".interpol(url);

            url = schemeDomainPort + jurl('collector_slug', 'popup_survey', 'slug', d.slug);
            code_survey = "<script type='text/javascript' src='[0]'></script>".interpol(url);

            url = schemeDomainPort + jurl('entry_form_slug', 'view_form', 'slug', d.slug);
            code_embed = "<iframe id='MootiroForm-[0]' allowTransparency='true' frameborder='0' style='width:100%; height: [1]px; border:none' src='[2]'><a href='[2]' title='[3]' rel='nofollow'>Fill out my MootiroForm!</a></iframe>".interpol(d.slug, he, url, d.name);
        }

        $('#wc_invitation').text(code_invitation);
        $('#wc_survey').text(code_survey);
        $('#wc_embed').text(code_embed);
        //$('#wc_full_page').text(code_full_page);

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
        var o = {defaultName: _('My public link collector'),
                 showAction: manager.showPublicLinkDialog}
        manager.editCollector(id, o);
    },
    editWebsiteCode: function (id) {
        var o = {defaultName: _('My website code collector'),
                 showAction: manager.showWebsiteCodeDialog}
        manager.editCollector(id, o);
    },
    editCollector: function(id, o) { // showAction, defaultName
        manager.currentId = id;
            var url = jurl('collector', 'as_json',
                'form_id', this.formId, 'id', id);
        if (id == 'new') {
            o.showAction({
                name: o.defaultName,
                on_completion: 'msg',
                limit_by_date: false,
                message_before_start: _('Sorry, you cannot fill in the form, yet. You can fill in the form from the following date on: {start date}'),
                message_after_end: _('Sorry, the period for filling in the form has elapsed on {end date}.'),
                thanks_message: _('Thanks for filling in my form!')
            });
        } else {
            var t = _("Sorry, could not retrieve the data for this collector.");
            $.get(url).success(o.showAction)
            .error(function (d) {
                alert(t + "\nStatus: " + d.status);
            });
        };
    },
    deleteCollector: function (id) {
        this.currentId = id;

        $('#confirm-deletion-' + id).dialog({
            modal: true,
            resizable: false,
            minHeight: 'auto',
            title: _('Delete collector'),
            buttons: [
                {
                text: _("Delete"),
                id: 'deleteBtn' + id,
                click: function() {
                    $(this).dialog("close");
                    var url = jurl('collector', 'delete',
                        'form_id', this.formId, 'id', id);
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
                },
                {
                text: _("Cancel"),
                id: 'canclBtn' + id,
                click: function () {
                    $(this).dialog("close");
                    }
                }
            ],
            open: function() {
                $("#canclBtn" + id).button().focus();
                $("#deleteBtn" + id).button(
                        {icons: {primary:'ui-icon-custom-delete'}});
            }
        });
    },
    closeDialog: function () {
        manager.$dialog.dialog('close');
    },
    savePublicLink: function () {
        $('#name').val($('#pl_name').val());

        var url = jurl('collector', 'save_public_link',
                'id', manager.currentId, 'form_id', manager.formId)
        var o = {saveUrl: url,
                 editAction: manager.editPublicLink,
                 onErrorLastTab: '#pl_tab-PublicLink'};
        manager.saveCollector(o);
    },
    saveWebsiteCode: function () {
        $('#name').val($('#wc_name').val());

        var url = jurl('collector', 'save_website_code',
                'id', manager.currentId, 'form_id', manager.formId)
        var o = {saveUrl: url,
                 editAction: manager.editWebsiteCode,
                 onErrorLastTab: '#wc_tab-WebsiteCode'};
        manager.saveCollector(o);
    },
    saveCollector: function (o) { // saveUrl, editAction, onErrorLastTab
        var tNotSaved = _("Sorry, the collector has NOT been saved.");
        var tCorrect = _("Please correct the errors as proposed in the highlighted text.");

        $.post(o.saveUrl, $('#CollectorsEditionForm').serialize())
        .success(function (d) {
            if (d.id) {  // success, saved
                // Considering a new collector, add it to the list
                if (manager.currentId != 'new') {
                    var $collectorRow = $("#collector-" + manager.currentId);
                    $.tmpl("collectorRow", d).insertAfter($collectorRow);
                    $collectorRow.remove();
                } else {
                    $.tmpl("collectorRow", d).appendTo('#collectorsRows');
                }
                setupCollectorsList();
                o.editAction(d.id);
            } else {  // d contains colander errors
                if (d.start_date || d.end_date || d['']) {
                    tabs.to('#shared_tab-Restrictions');
                    $('#StartDateError').text(d.start_date || '');
                    $('#EndDateError').text(d.end_date || '');
                    $('#IntervalError').text(d[''] || '');
                    alert(tNotSaved + '\n' + tCorrect);
                } else {
                    if (d.thanks_url || d.thanks_message) {
                        tabs.to('#shared_tab-Settings');
                    } else {
                        // TODO: when needed this will be set in a way to treat
                        // collector specific errors
                        tabs.to(o.onErrorLastTab); // last case
                    }
                    alert("[0] [1]\n[2]".interpol(tNotSaved,
                        _("Errors:"), dictToString(d)));
                }
            }
        })
        .error(function (d) {
            alert(tNotSaved + "\nStatus: " + d.status);
        });
    }
};

$('#limit_by_date').live('click', enableOrDisableRestrictionFields);

// TODO: Remove the function after implementing more restrictions. It is no
// longer necessary after more than one restriction is implemented. Then the
// fields will be collapsable and thereby not accessible by the user.
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

// validate the format of a date string as iso and return a date object
function dateValidation(string) { 
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
            $('#EndDateError').text(_('The end date must be in the future.'));
        } else {
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

function validateInvitationPopupWidth () {
    var $e = $('#invitation_popup_width_errors');
    var v = $(this).val();
    var error = integerValidator(v);
    $e.text(error);
    return;
}
function validateInvitationPopupHeight () {
    var $e = $('#invitation_popup_height_errors');
    var v = $(this).val();
    var error = integerValidator(v);
    $e.text(error);
    return;
}

function validateEmbedFrameHeight () {
    var $e = $('#embed_frame_height_errors');
    var h = $(this).val();
    var error = integerValidator(h);
    if (error) {
        $e.text(error);
        return;
    } else {
        $e.text('');
    }
    $e.text(_('You must save to update the generated code'));
    return;
}


// validate publish dates in realtime
$('#start_date, #end_date').live('keyup change', validatePublishDates);
$('#embed_frame_height').live('keyup change', validateEmbedFrameHeight);
$('#invitation_popup_width').live('keyup change', validateInvitationPopupWidth);
$('#invitation_popup_height').live('keyup change', validateInvitationPopupHeight);

$(function () {
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
});

$('#pl_url, #pl_link').click(function() {
    $(this).select();
});

$('#wc_invitation, #wc_survey, #wc_embed').click(function() {
    $(this).select();
});

