function init_forms_list(url, all_data, categories_list_slc) {
    // Global variables
    base_url = url;
    categories_list = $(categories_list_slc);
    form_delete_url = '';
    form_change_name_url = '';
    //console.log(all_data);

    categories_list.bind('update_forms_list', update_forms_list);
    $.event.trigger('update_forms_list', [all_data]);

    $('#create_form').hover(
        function () {
           $(this).toggleClass('newFormHover'); 
        }
     ).click(function () {
            location.href = 'http://' + base_url + route_url('form', {action: 'edit', id: 'new'});
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
                "Cancel": function() {
                    $(this).dialog("close");
                },
                "Delete": function() {
               $(this).dialog("close");
                $.post('http://' + base_url + route_url('form', {action: 'delete', id:form_id}))
                   .success(function (data) {
                       if (data.error) {
                            alert(error);
                       } else {
                       console.log(form_id);
                       console.log($('form-'+ form_id));
                       $('#form-'+form_id).html('');
                       }
                   })
                   .error(function (data) {
                       alert("Sorry, error deleting fields on the server.\n" +
                             "Your form has NOT been deleted.\n" +
                             "Status: " + data.status);
                        });
                }
            }
        });
    }
}

function update_forms_list(event, all_data) { 
    if (all_data && all_data.length > 0) {
        $('#no-form-message').toggle(false);
        
        $('#categories').html(''); //Empties the categories screen each pass
        $(all_data).each(function (cat_idx, category) { //This "each" renderizes each category
            
            $('#categories').append($('#category_template').tmpl(category));

                /* Configure the input to change category text */
                $('#cname-' + category.category_id).click(function () {

                    function change_name() {
                        $.post('http://' + base_url + route_url('category', {action: 'rename', id: category.category_id}),
                            {category_name: $(this).val()}
                        );
                        console.log($(this).val());
                        console.log("Agora o valor de $(this)");
                        console.log($(this));

                        $(this).hide();
                        $('#cname-' + category.category_id).html($(this).val()).show();
                    }

                    /* Show and configure the form's name input */
                    var category_name_input = $('#cname-input-' + category.category_id);
                    //console.log("form_name_input AQUI");
                    //console.log(form_name_input);
                    category_name_input
                            .attr({size: category_name_input.val().length})
                            .show()
                            .focus()
                            .focusout(change_name)
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
                    $(this).hide();
                });


            //This function renderizes each form
            $(category.forms).each(function (form_idx, form) {
                $('#categoryForms-' + category.category_id).append($('#form_template').tmpl(form));
                /* Add delete action */ 
                $('#delete-form-' + form.form_id)
                    .click(delete_form(form.form_name, form.form_id))
                    .hover(
                        function () {
                            $(this).attr('src', 'http://' + base_url + 'static/img/icons-root/deleteHover.png');  
                        },
                        function () {
                            $(this).attr('src', 'http://' + base_url + 'static/img/icons-root/delete.png');  
                        });



                /* Configure the input to change form text */
                $('#fname-' + form.form_id).click(function () {

                    function change_name() {
                        $.post('http://' + base_url + route_url('form', {action: 'rename', id: form.form_id}),
                            {form_name: $(this).val()}
                        );
                        $(this).hide();
                        $('#fname-' + form.form_id).html($(this).val()).show();
                    }

                    /* Show and configure the form's name input */
                    var form_name_input = $('#fname-input-' + form.form_id);
                    //console.log("form_name_input AQUI");
                    //console.log(form_name_input);
                    form_name_input
                            .attr({size: form_name_input.val().length})
                            .show()
                            .focus()
                            .focusout(change_name)
                            .keyup(function(){
                                $(this).attr({size: $(this).val().length});
                            })
                            .keydown(function(l) {
                              if (l.keyCode == 13) {
                                $(this).focusout();
                              }
                              $(this).attr({size: $(this).val().length});
                            });

                    /* Remove the form name */
                    $(this).hide();
                });

                /* Configure the edit button */

                $('#edit-form-' + form.form_id).click(function() {
                    location.href = 'http://' + base_url + route_url('form', {action: 'edit', id: form.form_id});
                })
                    .hover(
                        function () {
                            $(this).attr('src', 'http://' + base_url + 'static/img/icons-root/editHover.png');  
                        },
                        function () {
                            $(this).attr('src', 'http://' + base_url + 'static/img/icons-root/edit.png');  
                        });

                /* Configure the view button */

                $('#view-form-' + form.form_id).click(function() {
                    location.href = 'http://' + base_url + route_url('form', {action: 'view', id: form.form_id});
                })
                    .hover(
                        function () {
                            $(this).attr('src', 'http://' + base_url + 'static/img/icons-root/viewHover.png');  
                        },
                        function () {
                            $(this).attr('src', 'http://' + base_url + 'static/img/icons-root/view.png');  
                        });

                if ($("#no-entries-" + form.form_id).html() != '0') { 
                    $("#no-entries-" + form.form_id).attr('href', 'http://' + base_url + route_url('form', {action: 'answers', id: form.form_id}));
                }
            });
         
            $('#formsListTable td:odd').toggleClass('td_even');
        });

    } else {
       $('#no-form-message').toggle(true);
    }
}
