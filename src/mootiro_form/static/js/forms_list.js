function init_forms_list(url) {
    // Global variables
    base_url = url;
    form_delete_url = '';
    form_change_name_url = '';
}

function delete_form(form_name, form_id) {
    return function () {
        $('#confirm-deletion > #form-name').html(form_name);
        $('#confirm-deletion').dialog({
            modal: true,
            buttons: {
                "Cancel": function() {
                    $(this).dialog("close");
                },
                "Delete": function() {
                    $.post( // TODO: Use a function to assemble the URL below
                        'http://' + base_url + 'form/delete/' + form_id,
                        {},
                        function (data) {
                            $('#confirm-deletion').dialog("close");
                            update_forms_list(data.forms);
                        }
                    );
                }
            }
        });
    }
}

function update_forms_list(forms_data) { 

    if (forms_data && forms_data.length > 0) {
        $('#no-form-message').toggle(false);
        $('#forms_list').html($("#form_tr").tmpl(forms_data));

        $(forms_data).each(function (idx, elem) {
            $('#delete-form-' + elem.form_id)
                .click(delete_form(elem.form_name, elem.form_id));

            $('#fname-' + elem.form_id).click(function () {

                function change_name() {
                    $.post('http://' + base_url + 'form/rename/' + elem.form_id,
                        {form_name: $(this).val()}
                    );
                    $(this).hide();
                    $('#fname-' + elem.form_id).html($(this).val()).show();
                }

                        $(this).hide();
                        $('#fname-' + elem.form_id).html($(this).val()).show();

                    $('#fname-input-' + elem.form_id)
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
       $('#forms_list').html('');
       $('#no-form-message').toggle(true);
    }
}
