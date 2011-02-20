var field_template = "<span id='fieldLabel'>${label}:</span>${data}<br/>";

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
    $('#entryBox').dialog();
    $('#entryBox').html($.tmpl(field_template, entry));
}
