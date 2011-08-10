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

function setupEntriesList(pageNumber) {
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
    setNumberOfPages();
}

function setNumberOfPages() {
    var entriesPerPage = $('.entriesPerPageSelect > option:selected').val();
    var numberOfEntries = $('#entryNumber option').length;
    var numberOfPages = Math.ceil(numberOfEntries/entriesPerPage);
    $('.numberOfPages').text(' ' + numberOfPages);
}

function reloadEntriesList(pageNumber, pressedEnter, selectChange) {
    if(!selectChange) {
        if (invalidPageNumber(pageNumber, pressedEnter)) {
            return;
        }
    }
    var entriesPerPage = $('.entriesPerPageSelect > option:selected').val();
    var url = jurl('entry_list', action='limited_list', 'form_id', formId,
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

function invalidPageNumber(pageNumber, pressedEnter) {
    var numberOfPages = parseInt($('.numberOfPages').text());
    if (pageNumber < 1 ) {
        if (pressedEnter) {
            alert(_('Please enter a positive page number.'));
            return true;
        } else {
            alert(_('You are already on the first page.'));
            return true;
        }
    }
    else if (pageNumber > numberOfPages) {
        if (pressedEnter) {
            alert(_('Please enter a page number not greater than ')
                    + numberOfPages+'.');
            return true;
        } else {
            alert(_('You are already on the last page.'));
            return true;
        }
    }
}

function newPageNumber(numberOfEntries, entryIndex, entriesPerPage) {
    console.log(numberOfEntries);
    console.log(entryIndex);
    console.log(entriesPerPage);
    var n = Math.ceil((numberOfEntries - entryIndex) / entriesPerPage);
    if ((numberOfEntries - entryIndex) % entriesPerPage == 0) {
        n++;
    }
    console.log(n);
    return n;
}

function reloadEntriesListOnSelectChange(currentPage, entriesPerPageOld) {
    var numberOfEntries = $('#entryNumber option').length;
    var entryIndexOnTopPosition =
        numberOfEntries - (currentPage*entriesPerPageOld - entriesPerPageOld);
    var $entriesPerPageSelect = $(".entriesPerPageSelect");
    var entriesPerPage = $entriesPerPageSelect.val();
    var newPageNo = newPageNumber(numberOfEntries, entryIndexOnTopPosition, entriesPerPage);
    reloadEntriesList(newPageNo, false, true);
    // update value of entriesPerPageOld
    $entriesPerPageSelect.data('oldValue', entriesPerPage);
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

function enableOrDisablePreviousAndNextButtons() {
    // Obtain the current item in the select
    var currentOption = $('#entryNumber > option:selected');
    $('button.EntryNav').removeClass('disabledButton');
    $('button.EntryNav').removeAttr('disabled');
    if (currentOption.index() == 0) {
      $('#newerButton').addClass('disabledButton');
      $('#newerButton').attr('disabled', 'disabled');
    }
    if (currentOption.index() + 1 == $('#entryNumber option').length) {
      $('#olderButton').addClass('disabledButton');
      $('#olderButton').attr('disabled', 'disabled');
    }
}

//occasionally changes page if user deletes an entry or browses through the
//entries on the view entry dialog with the older/newer buttons or the select.
function changePage(newerButton, olderButton, deletedEntry) {
    console.log('entrei');
    var entryNumber = $('#entryNumber > option:selected').val();
    if (deletedEntry) {entryNumber = undefined;}
    var numberOfEntries = $('#entryNumber > option').length;
    var $entryList = $('.entries');
    console.log($entryList);
    //user deleted the only entry in the list
    if ($entryList.length == 0 && numberOfEntries > 0) {
        console.log('should not be here');
        reloadEntriesList($('.pageNumberInput').val());
        return;
    }
    var firstEntryNumberOfPage = parseInt($entryList.first()[0].cells[0].textContent)
    var lastEntryNumberOfPage = parseInt($entryList.last()[0].cells[0].textContent)
    //go to previous page in case user reached entry at the top of the list.
    if (newerButton && firstEntryNumberOfPage + 1 == entryNumber) {
        $('.previousPageButton').click();
    }
    //go to next page if user reached entry at bottom of the list.
    else if (olderButton && lastEntryNumberOfPage - 1 == entryNumber) {
        $('.nextPageButton').click();
    }
    //user changed entry with select: go to respective page if necessary.
    else if (entryNumber > firstEntryNumberOfPage ||
             entryNumber < lastEntryNumberOfPage) {
        console.log('probably in select change if: ' + entryNumber);
        var currentEntryIndex =
            numberOfEntries - $('#entryNumber > option:selected').index();
        var entriesPerPage = $('.entriesPerPageSelect > option:selected').val();
        var newPageNo = newPageNumber(numberOfEntries, currentEntryIndex,
                                      entriesPerPage);
        reloadEntriesList(newPageNo);
    }
}

$(function () {
    var entryNumberSelect = $('#entryNumber');

    entryNumberSelect.change(function (e) {
        var entryId = getCurrentEntryId();
        get_entry_data(entryId);
        setHrefAttributeForExportButton(entryId);
        changePage();
    });

    $('#newerButton').click(function () {
        var currentOption = $('#entryNumber > option:selected');
        var previousOption = currentOption.prev();
        entryNumberSelect.val(previousOption.val());
        entryNumberSelect.trigger('change');
        changePage(true, false);
    });

    $('#olderButton').click(function () {
        var currentOption = $('#entryNumber > option:selected');
        var nextOption = currentOption.next();
        entryNumberSelect.val(nextOption.val());
        entryNumberSelect.trigger('change');
        changePage(false, true);
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

    $('.entriesPerPageSelect').change(function (e) {
            reloadEntriesListOnSelectChange($('.pageNumberInput').val(),
                                            $(this).data('oldValue') || 10);
    });

    $('.previousPageButton').click(function (e) {
        reloadEntriesList(parseInt($('.pageNumberInput').val()) - 1);
    });

    $('.nextPageButton').click(function (e) {
        reloadEntriesList(parseInt($('.pageNumberInput').val()) + 1);
    });

    // Enable return key for pagenumber input
    $('.pageNumberInput').keydown(function(e) {
        if (e.which == 13) {
            reloadEntriesList($('.pageNumberInput').val(), true, false);
        }
    });
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
                    changePage(false, false, true);
                })
                .error(function () {
                    alert(_("Your entry could not be deleted."));
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

