base_url = '';
form_delete_url = '';

function init_forms_list(url) {
    base_url = url;
    form_delete_url = '';
    form_change_name_url = '';

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

    if (forms_data && forms_data.length > 0) {
        $('#no-form-message').toggle(false);
        $('#forms_list').html($("#form_tr").tmpl(forms_data));

        $(forms_data).each(function (idx, elem) {
            $('#delete-form-' + elem.form_id)
                .click(delete_form(elem.form_name, elem.form_id));

            $('#fname-' + elem.form_id).click(function () {

                    function change_name () {
                         $.post('http://localhost:6543/form/change_name'
                               , { form_name: $(this).val() ,
                                   form_id: elem.form_id });

                        $(this).hide();
                        $('#fname-' + elem.form_id).html($(this).val()).show();
                    }

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
