var field_template = "<div class='fieldLine'><span class='fieldLabel'>${label}:</span>${data}</div>";

function get_entry_data(id) {
    return function () {
        entry_data_url = 'http://' + url_root + route_url('entry', {action: 'data', id: id});
        $.ajax({
            url: entry_data_url, 
            success: show_entry_data
        }); 
    }
}

function show_entry_data(entry) {
    $('#entryBox').dialog({dialogClass: 'dialog'});
    $('#entryBox').html($.tmpl(field_template, entry));
    $('.fieldLine:even').toggleClass('fieldLineEven');
}
