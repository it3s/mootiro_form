function init_forms_list(url) {
    // Global variables
    base_url = url;
    form_delete_url = '';
    form_change_name_url = '';

    $.post('http://' + base_url + 'handler_url',
    {
        handler_name: 'form',
        action: 'delete'
    },
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
                "Delete": function() {
                    $.post( // TODO: Use a function to assemble the URL below
                        'http://' + base_url + 'form/delete/' + form_id,
                        {},
                        function (data) {
                            $('#confirm-deletion').dialog("close");
                            update_forms_list(data.forms);
                        }
                    );
                },
                "Cancel": function() {
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

        forms_list.append($('<ul/>', {
            id: 'forms_list'
        }));
        $(forms_data).each(function (idx, elem) {

            var li_id = 'form-' + elem.form_id;
            var delete_button = $('<span/>', {
                id: 'delete-' + li_id,
                click: delete_form(elem.form_name, elem.form_id)
            }).html('Delete');

            $('#forms_list').append('<li id="' + li_id + '">\
                                <input class="fname" style="display: none;" name="form_name" value="' 
                + elem.form_name +
                '"/><span class="form_name">' + elem.form_name + '</span></li>');

            li_form = $('#' + li_id);
            li_form.append(delete_button)

            $('.form_name', li_form).click(function () {

                function change_name() {
                    $.post('http://' + base_url + 'form/rename/' + elem.form_id,
                        {form_name: $(this).val()}
                    );
                    $(this).hide();
                    $('#' + li_id + ' > .form_name').html($(this).val()).show();
                }

                $('#' + li_id + ' > .fname')
                .show()
                .focus()
                .focusout(change_name)
                .keydown(function(l) {
                    if (l.keyCode == 13) {
                        $(this).focusout();
                    }
                });
                $(this).hide();
            });
        });
    } else {
        var no_form_message = $('<div/>', {
            id: 'no_forms'
        })
        .html("You don't have any forms yet.");

        forms_list.append(no_form_message);
    }
}
