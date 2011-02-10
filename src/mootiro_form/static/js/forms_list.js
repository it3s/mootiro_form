base_url = '';
form_delete_url = '';

function init_forms_list(url) {
    base_url = url;
    form_delete_url = '';

    $.post('http://' + base_url + 'handler_url',
            { handler_name: 'form'
            , action: 'delete' }, 
            function (data) {
                form_delete_url = data.url;
            });

}

function delete_form(form_name, form_id) {

    return function () {
    
        $('#confirm-deletion > #form-name').html(form_name);
        $('#confirm-deletion').dialog({
            modal: true,
            buttons: {
                "Delete": function () {
                        $.post(
                             form_delete_url
                           , { formid: form_id } 
                           , function (data) {
                               $('#confirm-deletion').dialog("close");
                               update_forms_list(data.forms);
                             }
                        );
                },
                "Cancel": function () {
                    $(this).dialog("close");
                }
            }
        });
    }
}

function update_forms_list(forms_data) { 
    var forms_list = $('#forms');

    forms_list.empty();
    
        if (forms_data && forms_data.length > 0) {

        forms_list.append($('<ul/>', {id: 'forms_list'}));
        $(forms_data).each(function (idx, elem) {

            var li_id = 'form-' + elem.form_id;
            var delete_button = $('<span/>', {
                                 id: 'delete-' + li_id,
                                 click: delete_form(elem.form_name, elem.form_id)
                                }).html('Delete');

            $('#forms_list').append('<li id="' + li_id + '">' + elem.form_name + '</li>'); 
            $('#' + li_id).append(delete_button);
        });

    } else {
        var no_form_message = $('<div/>', { id: 'no_forms'})
        .html('You dont have any forms yet.');

        forms_list.append(no_form_message);
    }

}
