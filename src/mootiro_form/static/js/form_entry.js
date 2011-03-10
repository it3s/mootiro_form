var field_template = $.template('field_template', "<div class='fieldLine'><div class='fieldLabel'>${position}. ${label}</div><div class='fieldData'>${data}</div></div>");

var entry_template = "{{each fields}}{{tmpl($value) 'field_template'}}{{/each}}";

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
    $('#entryBox').html($.tmpl(entry_template, entry));
    $('.fieldLine:odd').toggleClass('fieldLineOdd');
}
