function logged_root_init() {
    $.get(jurl('static') + '/jquery-templates/forms_list.tmpl.html',
        function (fragment) {
            $('body').append(fragment);
            $.template('categoryTemplate', $('#categoryTemplate'));
            $.template('formTemplate', $('#formTemplate'));
            if (all_data) {
                init_forms_list(url_root, all_data, '#categories');
            } else {
                init_forms_list(url_root, '', '#categories');
            }
        }
    );
}

function init_forms_list(url, all_data, categories_list_slc) {
    // Global variables
    base_url = url;
    categories_list = $(categories_list_slc);
    form_delete_url = '';
    form_change_name_url = '';

    categories_list.bind('update_forms_list', update_forms_list);
    $.event.trigger('update_forms_list', [all_data]);

    /* This function defines the action for the create_category dialog */
    var newCategory = function() {
        $.post('/category/edit/new',
            $('#newcategoryform').serialize(),
            function (response) {
                if (response.changed) {
                    $.event.trigger('update_forms_list', [response.all_data]);
                    $('#newCategory').dialog('close');
                } else {
                    $('#newCategory').html(response);
                }
        });
    }

    /* This function defines the create_category dialog */
    $('#create_category').click(function () {
        $('#newCategory').load('/category/edit/new', function() {
            $('#newCategory').dialog({
                width: 'auto',
                minHeight:'400px',
                modal: true,
                buttons:
                    [{text: _('Create new category'),
                      click: newCategory}]
            })
        });
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

function copy_form(form_id) {
    return function () {
        $.post(jurl('form', 'copy', 'id', form_id))
            .success(function (data) {
                if (data.errors) {
                    alert(error);
                } else {
                    $.event.trigger('update_forms_list', [data.all_data]);
                    $("#fname-" + data.form_copy_id).click();
                }
            })
            .error(function (data) {
                alert(_("Sorry, error on the server -- your form has NOT been copied.\nStatus: [0]").interpol(data.status));
            });
    }
}

function delete_form(form_name, form_id) {
    return function () {
        var dialog_title = _('Delete form')
        $('#confirm-deletion').attr('title',
                                    dialog_title + ' ' + form_name + '?');
        $('#confirm-deletion').dialog({
            modal: true,
            resizable: false,
            minHeight: 'auto',
            buttons: [
                {
                text: _("Delete"),
                id: "deleteBtn" + form_id,
                click: function() {
                    $(this).dialog("close");
                    $.post(jurl('form', 'delete', 'id', form_id))
                        .success(function (data) {
                            if (data.error) {
                                alert(error);
                            } else {
                                $.event.trigger('update_forms_list',
                                                [data.all_data]);
                            }
                        })
                        .error(function (data) {
                            alert(_("Sorry, error on the server.\nYour form has"
                                    + "NOT been deleted.\nStatus: [0]")
                                    .interpol(data.status));
                        });
                    }
                },
                {
                text: _("Cancel"),
                id: "cancelBtn" + form_id,
                click: function () {$(this).dialog("close");}
                }
            ],
            open: function() {
                $("#cancelBtn" + form_id).button().focus();
                $("#deleteBtn" + form_id).button(
                        {icons: {primary:'ui-icon-custom-delete'}});
            }
        });
    }
}

function update_forms_list(event, all_data) {
    if (all_data.categories && all_data.categories.length > 0) {
        $('#NoFormMessage').toggle(false);
       // $('#no-form-in-category-message').tmpl('');//These two are initializations of alert messages. If there aren't any categories, their status will be toggled below
        $('#uncategorized').empty();
        $('#categories').empty(); //Empties the screen each pass
            $(all_data.categories).each(function (cat_idx, category) { //This "each" renderizes each category
            var rendered = $.tmpl('categoryTemplate', category);
            if (category.category_name == "uncategorized") {
                //$('#uncategorized') is renderized each time, so we need to
                //empty it each pass
                $('#uncategorized').append(rendered);
            } else {
                $('#categories').append(rendered);
            }
                /* Configure the input to change category text */
                /*$('#cname-' + category.category_id).click(function () {

                    function change_name() {
                        $.post('http://' + base_url + jurl('category', 'rename', 'id', category.category_id),
                            {category_name: $(this).val()}
                        );
                        //console.log($(this).val());
                        //console.log("Agora o valor de $(this)");
                        //console.log($(this));

                        $(this).hide();//Hides the name
                        $('#cname-' + category.category_id).html($(this).val()).show(); //Shows the dialog to input name
                    }

                    /* Show and configure the form's name input */
                  /*  var category_name_input = $('#cname-input-' + category.category_id);
                    category_name_input
                            .attr({size: category_name_input.val().length})
                            .show()
                            .focus()
                            .focusout(change_name)//HERE the name is changed!
                            .keyup(function(){
                                $(this).attr({size: $(this).val().length});
                            })
                            .keydown(function(l) {
                              if (l.keyCode == 13) {
                                $(this).focusout();
                              }
                              $(this).attr({size: $(this).val().length});
                            });

                    /* Remove the category name */
                    //$(this).hide();
                //});


            // This function renders each form
            $(category.forms).each(function (form_idx, form) {
                $('#categoryForms-' + category.category_id)
                    .append($.tmpl('formTemplate', form));

                var editDiv = "#fname-edit-" + form.form_id;
                var errorPara = $(editDiv + ' p');
                var inputName = $('#fname-input-' + form.form_id);
                var spanName = $('#fname-' + form.form_id);

                $(editDiv).hide();

                /* Configure the copy button */
                $('#copy-form-' + form.form_id)
                    .click(copy_form(form.form_id))
                    .hover(
                        function () {
                            $(this).attr('src', jurl('static') +
                                '/img/icons-root/copyHover.png');
                        },
                        function () {
                            $(this).attr('src', jurl('static') +
                                '/img/icons-root/copy.png');
                        });

                /* Add delete action */
                $('#delete-form-' + form.form_id)
                    .click(delete_form(form.form_name, form.form_id))
                    .hover(
                        function () {
                            $(this).attr('src', jurl('static') +
                                '/img/icons-root/deleteHover.png');
                        },
                        function () {
                            $(this).attr('src', jurl('static') +
                                '/img/icons-root/delete.png');
                        }
                    );
                /* Configure the form name to be modifiable */
                spanName.die().live('click', function () {
                    function change_name() {
                        $.post(jurl('form', 'rename', 'id', form.form_id),
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
                            alert(_("Sorry, error on the server.\nYour changes have NOT been saved.\nStatus: [0]").interpol(data.status));
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
                }
            );
            /* Configure the edit button */
            $('#edit-form-' + form.form_id).hover(
                function () {
                    $(this).attr('src', jurl('static') +
                        '/img/icons-root/editHover.png');
                },
                function () {
                    $(this).attr('src', jurl('static') +
                        '/img/icons-root/edit.png');
                }
            );
            /* Configure the view button */
            $('#view-form-' + form.form_id).hover(
                function () {
                    $(this).attr('src', jurl('static') +
                        '/img/icons-root/viewHover.png');
                },
                function () {
                    $(this).attr('src', jurl('static') +
                        '/img/icons-root/view.png');
                }
            );
            /* Configure the collect button */
            $('#collect-form-' + form.form_id).hover(
                function () {
                    $(this).attr('src', jurl('static') +
                        '/img/icons-root/collectHover.png');
                },
                function () {
                    $(this).attr('src', jurl('static') +
                        '/img/icons-root/collect.png');
                }
            );
            if (form.form_entries != 0) {
                $("#no-entries-" + form.form_id).attr('href',
                    jurl('entry', 'list', 'id', form.form_id));
            }
        $('.ListTable tr td:nth-child(2n+1)').addClass('darker');
        $('.ListTable tr td:nth-child(1)').removeClass('darker');
        $('.ListTable thead th:nth-child(2n)').addClass('darker');
        });
      });
    }
    if (all_data.forms_existence===false) {
        //If there isn't any data, there aren't any forms or categories, so
        //let's show the message indicating there are no forms and hide all
        //other things
        $('#uncategorized').empty();
        //$('#categories').empty();
        $('#NoFormMessage').toggle(true);
    }
    // After redrawing all the stuff, create the accordion
    $("#categories").accordion("destroy");
    $("#categories").accordion();
}
