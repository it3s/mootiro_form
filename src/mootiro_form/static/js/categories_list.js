function init_categories_list(url, categories_data, categories_list_slc) {
    // Global variables
    base_url = url;
    categories_list = $(categories_list_slc);
    category_delete_url = '';
    category_change_name_url = '';

    categories_list.bind('update_categories_list', update_categories_list);
    $.event.trigger('update_categories_list', [categories_data]);
}

/*
function delete_category(category_name, category_id) {
    return function () {
        $('#confirm-deletion > #category-name').html(category_name);
        $('#confirm-deletion').dialog({
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
                            $('#confirm-deletion').dialog("close");
                            $.event.trigger('update_categories_list', [data.categories])
                        }
                    );
                }
            }
        });
    }
}
*/


function update_categories_list(event, categories_data) { 
    alert("Essa porra tá rodando de novo");

    if (categories_data && categories_data.length > 0) {
        $('#no-category-message').toggle(false);
        categories_list.html($("#category_tr").tmpl(categories_data));

        $(categories_data).each(function (idx, elem) {

            /* Add delete action */ 
            $('#delete-category-' + elem.category_id)
                .click(delete_category(elem.category_name, elem.category_id));

            /* Configure the input to change category text */
            $('#fname-' + elem.category_id).click(function () {

                function change_name() {
                    $.post('http://' + base_url + 'category/rename/' + elem.category_id,
                        {category_name: $(this).val()}
                    );
                    $(this).hide();
                    $('#fname-' + elem.category_id).html($(this).val()).show();
                }

                /* Show and configure the category's name input */
                var category_name_input = $('#fname-input-' + elem.category_id);

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

            /* Configure the edit button */

            $('#edit-category-' + elem.category_id).click(function() {
                location.href = 'http://' + base_url + 'category/edit/' + elem.category_id;
            });

        });
    } else {
       categories_list.html('');
       $('#no-category-message').toggle(true);
    }
}

