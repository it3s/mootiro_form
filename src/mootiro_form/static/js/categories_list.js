function init_categories_list(url) {
    // Global variables
    base_url = url;
    category_delete_url = '';
    category_change_name_url = '';
}

function delete_category(category_name, category_id) {
    return function () {
        $('#confirm-category-deletion > #category-name').html(category_name); //WTF happens on this line??
        $('#confirm-category-deletion').dialog({
            modal: true,
            buttons: {
                "Cancel": function() {
                    $(this).dialog("close");
                },
                "Delete": function() {
                    $.post( // TODO: Use a function to assemble the URL below
                        'http://' + base_url + 'category/delete/' + category_id,
                        {},
                        function (data) {
                            $('#confirm-category-deletion').dialog("close");
                            update_forms_list(data.categories);
                        }
                    );
                }
            }
        });
    }
}

function update_categories_list(categories_data) {

    alert("Entrou no update_categories_list");
        alert("categories_data = " + categories_data + "categories_data.length = " + categories_data.length);
    if (categories_data && categories_data.length > 0) {
        alert("categories_data = " + categories_data + "categories_data.length = " + categories_data.length);
        $('#no-category-message').toggle(false);
        $('#categories_list').html($("#category_tr").tmpl(categories_data));

        $(categories_data).each(function (idx, elem) {

            /* Add delete action */ 
            $('#delete-category-' + elem.category_id)
                .click(delete_category(elem.category_name, elem.category_id));

            /* Configure the input to change form text */
            $('#cname-' + elem.category_id).click(function () {

                function change_name() {
                    $.post('http://' + base_url + 'category/rename/' + elem.form_id,
                        {form_name: $(this).val()}
                    );
                    $(this).hide();
                    $('#cname-' + elem.form_id).html($(this).val()).show();
                }

                /* Show and configure the form's name input */
                var category_name_input = $('#cname-input-' + elem.category_id);

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

                /* Remove the form name */
                $(this).hide();
            });

            /* Configure the edit button */

            $('#edit-category-' + elem.category_id).click(function() {
               alert("ID da categoria: "+ elem.category_id);
               location.href = 'http://' + base_url + 'category/edit/' + elem.category_id;
            });

        });
    } else {
       $('#categories_list').html('');
       $('#no-category-message').toggle(true);
    }
}
