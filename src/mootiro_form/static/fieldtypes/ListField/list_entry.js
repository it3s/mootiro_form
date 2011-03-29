function limit_choices(id, min, max) {

    var select_list = $('.select-' + id);
    var other_input = $('.other-' + id);

    count_options = function () {
        var min_num = min;
        var max_num =  max;
        var number_choices = $('option:selected', select_list).length;
        var other = other_input.val();
        var other_true = 0;

        if (other) {
            other_true = 1;
        }
    
        if (number_choices + other_true > max_num) {
            $('#select-message-' + id).html('Exceeds maximum number of choices');
        } else {
            $('#select-message-' + id).html('');
        }
    }

    select_list.change(count_options); 
    other_input.change(count_options);
}


function one_choice(id) {

    var other_input = $('.other-' + id);
    var radios = $('.radio-' + id);

    other_input.focus(function () {
        $('.radio-' + id).attr("checked", false);
    });

    radios.change(function () {
        if ($('this:checked')) {
            other_input.val('');
        }
    });
}
