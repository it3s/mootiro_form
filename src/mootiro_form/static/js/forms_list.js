function init_forms_list(url, forms_data, forms_list_slc) {
    // Global variables
    base_url = url;
    forms_list = $(forms_list_slc);
    form_delete_url = '';
    form_change_name_url = '';

    forms_list.bind('update_forms_list', update_forms_list);
    $.event.trigger('update_forms_list', [forms_data]);

    $('#create_form').hover(
        function () {
           $(this).toggleClass('newFormHover'); 
        }
     ).click(function () {
            location.href = 'http://' + base_url +
                route_url('form', {action: 'edit', id: 'new'});
    });


    function select_all_forms () {
        if ($('#selectAll-input').is(':checked')) {
            $('#selectAll-input').attr('checked', false);
            $('.formSelect').attr('checked', false);
        } else {
            $('#selectAll-input').attr('checked', true);
            $('.formSelect').attr('checked', true);
        }
    }

    /* Configure select_all checkbox */

    $('#selectAll-input').change(function () {
        if ($('#selectAll-input').is(':checked')) {
            $('.formSelect').attr('checked', true);
        } else {
            $('.formSelect').attr('checked', false);
        }
    });
    $('.selectAll > span').click(select_all_forms);
}

function delete_form(form_name, form_id) {
    return function () {
        $('#confirm-deletion > #form-name').html(form_name);
        $('#confirm-deletion').dialog({
            modal: true,
            buttons: {
                "Cancel": function () {
                    $(this).dialog("close");
                },
                "Delete": function () {
                    $.post(
                        'http://' + base_url +
                            route_url('form', {action: 'delete', id:form_id}),
                        {},
                        function (data) {
                            $('#confirm-deletion').dialog("close");
                            $.event.trigger('update_forms_list',
                                [$.parseJSON(data.forms)])
                        }
                    );
                }
            }
        });
    }
}

function update_forms_list(event, forms_data) { 

    if (forms_data && forms_data.length > 0) {
        $('#no-form-message').toggle(false);
        forms_list.html($("#form_tr").tmpl(forms_data));

        $(forms_data).each(function (idx, props) {
            var editDiv = "#fname-edit-" + props.form_id;
            var errorPara = $(editDiv + ' p');
            var inputName = $('#fname-input-' + props.form_id);
            var spanName = $('#fname-' + props.form_id);

            $(editDiv).hide();
            
            /* Add delete action */ 
            $('#delete-form-' + props.form_id)
                .click(delete_form(props.form_name, props.form_id))
                .hover(
                    function () {
                        $(this).attr('src', 'http://' + base_url +
                            'static/img/icons-root/deleteHover.png');
                    },
                    function () {
                        $(this).attr('src', 'http://' + base_url +
                            'static/img/icons-root/delete.png');
                    });

            /* Configure the form name to be modifiable */
            spanName.die().live('click', function () {

                function change_name() {
                    $.post('http://' + base_url + route_url('form',
                        {action: 'rename', id: props.form_id}),
                        {form_name: $(this).val()})
                    .success(function (data) {
                        errorPara.text(data.name);
                        if (data.name) {
                            $(editDiv).show();
                            errorPara.show();
                        } else { // saved OK
                            inputName.die(); // prevent POSTing more than once
                            $(editDiv).hide();
                            errorPara.hide();
                            var text = inputName.val().slice(0, 25);
                            if (inputName.val().length > 24)  text += '...';
                            if (!text) text = 'Untitled form';
                            spanName.text(text).show();
                        }
                    })
                    .error(function (data) {
                        alert("Sorry, error on the web server.\n" +
                            "Your changes have NOT been saved.\n" +
                            "Status: " + data.status);
                    });
                }

                spanName.hide();
                errorPara.hide();
                $(editDiv).show();
                /* Show and configure the form's name input */
                inputName.attr({size: inputName.val().length})
                         .die()
                         .live('focusout', change_name)
                         .live('keyup', function () {
                             $(this).attr({size: $(this).val().length});
                         })
                         .live('keydown', function (l) {
                           if (l.keyCode == 13) {
                             $(this).focusout();
                           }
                           $(this).attr({size: $(this).val().length});
                         })
                         .show()
                         .focus();
            // end spanName.click()
            });

            /* Configure the edit button */

            $('#edit-form-' + props.form_id).hover(
                    function () {
                        $(this).attr('src', 'http://' + base_url +
                            'static/img/icons-root/editHover.png');
                    },
                    function () {
                        $(this).attr('src', 'http://' + base_url +
                            'static/img/icons-root/edit.png');
                    });

            /* Configure the view button */

            $('#view-form-' + props.form_id).hover(
                    function () {
                        $(this).attr('src', 'http://' + base_url +
                            'static/img/icons-root/viewHover.png');
                    },
                    function () {
                        $(this).attr('src', 'http://' + base_url +
                            'static/img/icons-root/view.png');
                    });

            if ($("#no-entries-" + props.form_id).html() != '0') {
                $("#no-entries-" + props.form_id).attr('href', 'http://' +
                  base_url + route_url('form',
                  {action: 'answers', id: props.form_id}));
            }
        });
    
        $('#formsListTable tr td:nth-child(2n)').toggleClass('even');

    } else {
       forms_list.html('');
       $('#no-form-message').toggle(true);
    }
}
