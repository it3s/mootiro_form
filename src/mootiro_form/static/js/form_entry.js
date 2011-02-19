var field_template = "<span id='fieldLabel'>${label}:</span>${data}<br/>";

function show_entry_data(entry) {
    $('#entryBox').dialog();
    $('#entryBox').html($.tmpl(field_template, entry));
}
