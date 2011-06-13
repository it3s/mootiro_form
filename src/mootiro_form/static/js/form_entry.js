// As the page loads, GET the templates file and compile the templates
$.get(jurl('static') + '/jquery-templates/entries_list.tmpl.html',
    function (fragment) {
        $('body').append(fragment);
        $.template('entriesTable', $('#entriesTable'));
        $.template('entryRow', $('#entryRow'));
        $.tmpl('entriesTable').appendTo('#formAnswers');
        $.tmpl('entryRow', entries_json).appendTo('#entryRows');
        setupEntriesList();
    }
);

function setupEntriesList() {
    $('.ListTable thead th:nth-child(2n)').addClass('darker');
    $('.ListTable tr td:nth-child(2n)').addClass('darker');
    $('.newEntry td:nth-child(2n)').addClass('newEntryDarker');
    // Formatting for the icons on the entries table:
    onHoverSwitchImage('.viewButton', null,
            jurl('static') + '/img/icons-root/viewHover.png',
            jurl('static') + '/img/icons-root/view.png');
    onHoverSwitchImage('.exportSymbol', null,
            jurl('static') + '/img/icons-answers/exportOrange.png',
            jurl('static') + '/img/icons-answers/exportDark.png');
    onHoverSwitchImage('.deleteEntryButton', null,
            jurl('static') + '/img/icons-answers/deleteOrange.png',
            jurl('static') + '/img/icons-answers/delete.png');
    onHoverSwitchImage('.newEntry .viewButton', null,
            jurl('static') + '/img/icons-root/viewHover.png',
            jurl('static') + '/img/icons-answers/viewWhite.png');
    onHoverSwitchImage('.newEntry .exportSymbol', null,
            jurl('static') + '/img/icons-answers/exportOrange.png',
            jurl('static') + '/img/icons-answers/exportWhite.png');
    onHoverSwitchImage('.newEntry .deleteEntryButton', null,
            jurl('static') + '/img/icons-answers/deleteOrange.png',
            jurl('static') + '/img/icons-answers/deleteWhite.png');
    setNumberOfPages(numberOfEntries);
}

setNumberOfPages = function(numberOfEntries) {
    var entriesPerPage = $('#entriesPerPageSelect > option:selected').val();
    var numberOfPages = Math.ceil(numberOfEntries/entriesPerPage);
    $('.numberOfPages').text(' ' + numberOfPages);
}

reloadEntriesList = function(pageNumber) {
    var entriesPerPage = $('#entriesPerPageSelect > option:selected').val();
    var url = jurl('entry_list', action='limited_list', 'id', formId,
                   'page', pageNumber, 'limit', entriesPerPage)
    $.post(url)
        .success(function(entries) {
            entries_json = entries;
            $('.entries').remove();
            $.tmpl('entryRow', entries_json).appendTo('#entryRows');
            setupEntriesList();
            $('.pageNumberInput').val(pageNumber);
        })
        .error(function() {
            alert(_('Sorry, could not reload the entry list.'));
        })
}

reloadEntriesListOnSelectChange = function(currentPageNumber) {
    var entriesPerPage = $('#entriesPerPageSelect > option:selected').val();
    console.log(entriesPerPage);
    //if (currentPageNumber*entriesPerPage > numberOfEntries) {
    console.log('yep');
    var newTotalNumberOfPages = Math.ceil((numberOfEntries/entriesPerPage)); // == 100%
    var currentTotalNumberOfPages = parseInt($('.numberOfPages').text());
    console.log(currentTotalNumberOfPages);
    var newPageNumber = Math.ceil(currentPageNumber / currentTotalNumberOfPages
                        * newTotalNumberOfPages);
    reloadEntriesList(newPageNumber);
    }// else {
       // reloadEntriesList(currentPageNumber);
    //}
//}
enableOrDisableEntryControl = function(pageNumber) {

}

var field_template = $.template('field_template', "<div class='fieldLine'><div class='fieldLabel'>${position}. ${label}</div><div class='fieldData'>${data}</div></div>");

var entry_template = "{{each fields}}{{tmpl($value) 'field_template'}}{{/each}}";

function get_entry_data(id) {
    $.ajax({
        url: jurl('entry', 'data', 'id', id),
        success: show_entry_data
    });
}

function show_entry_data(entry) {
    $('#entryData').html($.tmpl(entry_template, entry));
    $('#entryNumber').val(entry['entry_number']);
    $('#entryBox').dialog({
        width: 'auto',
        open: function() {
            setHrefAttributeForExportButton(getCurrentEntryId);
            }
    });
    $('.fieldLine:odd').toggleClass('fieldLineOdd');
    if ($('#entry_' + entry['entry_id']).hasClass('newEntry')) {
        $('#entry_' + entry['entry_id']).removeClass('newEntry');
        $('#entry_' + entry['entry_id'] + ' td:nth-child(2n)').removeClass(
                'newEntryDarker');
        $('#entry_' + entry['entry_id'] +  ' .viewButton').attr(
                'src', jurl('static') + '/img/icons-root/view.png');
        $('#entry_' + entry['entry_id'] +  ' .exportSymbol').attr(
                'src', jurl('static') + '/img/icons-answers/exportDark.png');
        $('#entry_' + entry['entry_id'] + ' .deleteEntryButton').attr(
                'src', jurl('static') + '/img/icons-answers/delete.png');
    }
    enableOrDisablePreviousAndNextButtons();
}

function enableOrDisablePreviousAndNextButtons () {
    // Obtain the current item in the select
    var currentOption = $('#entryNumber > option:selected');
    $('button.EntryNav').removeClass('disabledButton');
    $('button.EntryNav').removeAttr('disabled');
    if (currentOption.index() == 0) {
      $('#previousButton').addClass('disabledButton');
      $('#previousButton').attr('disabled', 'disabled');
    }
    if (currentOption.index() + 1 == $('#entryNumber option').length) {
      $('#nextButton').addClass('disabledButton');
      $('#nextButton').attr('disabled', 'disabled');
    }
}

$(function () {
    var theSelect = $('#entryNumber');

    theSelect.change(function (e) {
        // When the selected option is changed:
        var currentOption = $('#entryNumber > option:selected');
        // the entry id is in the option id, after "entryNumberOp_"
        var entryId = currentOption.attr('id').substring(14);
        get_entry_data(entryId);
        setHrefAttributeForExportButton(entryId);
    });

    $('#previousButton').click(function () {
        var currentOption = $('#entryNumber > option:selected');
        var previousOption = currentOption.prev();
        theSelect.val(previousOption.val());
        theSelect.trigger('change');
    });

    $('#nextButton').click(function () {
        var currentOption = $('#entryNumber > option:selected');
        var nextOption = currentOption.next();
        theSelect.val(nextOption.val());
        theSelect.trigger('change');
    });

    $('#deleteButtonViewDialog').click(
            function() {deleteEntry(getCurrentEntryId)});
    // Configure mouseover of pagination controls
    onHoverSwitchImage('.firstPageButton', null,
            jurl('static') + '/img/icons-answers/firstPageHover.png',
            jurl('static') + '/img/icons-answers/firstPage.png');
    onHoverSwitchImage('.nextPageButton', null,
            jurl('static') + '/img/icons-answers/nextPageHover.png',
            jurl('static') + '/img/icons-answers/nextPage.png');
    onHoverSwitchImage('.previousPageButton', null,
            jurl('static') + '/img/icons-answers/previousPageHover.png',
            jurl('static') + '/img/icons-answers/previousPage.png');
    onHoverSwitchImage('.lastPageButton', null,
            jurl('static') + '/img/icons-answers/lastPageHover.png',
            jurl('static') + '/img/icons-answers/lastPage.png');
});

function deleteEntry(id) {
    // disable delete button to avoid race conditions
    $("#deleteButtonViewDialog").attr('disabled', 'disabled');
    var url = jurl('entry', 'delete', 'id', id);
    $.post(url)
        .success(function (data) {
            $("#entry_" + data.entry).remove();
            var entryOption = $("#entryNumberOp_" + data.entry);
            if (entryOption.next().length != 0) {
            // if entry is not the last in the list: show the next one
                $('#entryNumber').val(entryOption.next().val());
            } else {
            // else show the first entry of the list
                $('#entryNumber').val($('#entryNumber')[0].childNodes[1].value);
            }
            $('#entryNumber').trigger('change');
            if ($('#entryNumber')[0].length == 1) {
                $('#entryBox').dialog('close');
            }
            entryOption.remove();
            // enable button again
            $("#deleteButtonViewDialog").removeAttr('disabled');
        })
        .error(function () {
            alert(_("Couldn't delete the entry!"));
            $("#deleteButtonViewDialog").removeAttr('disabled');
        });
}

function setHrefAttributeForExportButton(id) {
    $("#exportButtonViewDialog").attr('href',
            jurl('entry', 'export', 'id', id));
}

function getCurrentEntryId() {
    return $('#entryNumber > option:selected').attr('id').substring(14);
}

function deleteEntryDialog(id) {
    $('#deleteEntryBox').dialog({
      resizable: false,
      minHeight: 'auto',
      modal: true,
      buttons: [
        {
        text: _("Delete"),
        id: "deleteBtn" + id,
        click: function() {
            var url = jurl('entry', 'delete', 'id', id);
            $.post(url)
                .success(function (data) {
                    $("#entry_" + data.entry).remove();
                    $("#entryNumberOp_" + data.entry).remove();
                })
                .error(function () {
                    alert(_("Couldn't delete the entry!"));
                });
            $(this).dialog("close");}
        },
        {
        text: _("Cancel"),
        id: "cancelBtn" + id,
        click: function() {$(this).dialog("close");}
        }
      ],
      open: function() {
          $("#cancelBtn" + id).button().focus();
          $("#deleteBtn" + id).button(
                  {icons: {primary:'ui-icon-custom-delete'}});
         }
    });
}

