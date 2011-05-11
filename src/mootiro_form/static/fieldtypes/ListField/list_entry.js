function limit_choices(id, min, max, list_type) {

    if (!min) {
        min = 0;    
    }  

    if (!max) {
        max = 0;
    }

    if (list_type == 'select') {
        var select_list = $('.select-' + id);
    } else if (list_type == 'checkbox') { 
        var select_list = $('.checkbox-' + id);
    }
    var other_input = $('.other-' + id);

    count_options = function () {
        var min_num = min;
        var max_num =  max;
        if (list_type == 'select') {
            var number_choices = $('option:selected', select_list).length;
        } else if (list_type == 'checkbox'){
            var number_choices = $('.checkbox-' + id + ':checked').length;
        }
        console.log(number_choices);
        var other = other_input.val();
        var other_true = 0;

        if (other) {
            other_true = 1;
        }
    
        if (max_num != 0 && number_choices + other_true > max_num) {
            $('#select-message-' + id).html('Exceeds maximum number of choices');
        } else {
            $('#select-message-' + id).html('');
        }
    }

    select_list.change(count_options); 
    other_input.change(count_options);
}

function one_choice(id) {

    var other_tmp_radio = $('.other-tmp-radio-' + id);
    var other_tmp = $('.other-tmp-' + id);
    var other_input = $('.other-' + id);
    var radios = $('.radio-' + id);

    other_input.focus(function () {
        $('.radio-' + id).attr("checked", false);
        other_tmp_radio.attr("checked", "checked");
    });

    other_click = function () {
        other_tmp.hide();
        other_input.show();
        other_input.val(other_tmp.val());
        other_input.focus();
    };

    other_tmp_radio.click(other_click);
    other_tmp.click(other_click);

    radios.change(function () {
        if ($('this:checked')) {
            if (other_tmp_radio.attr("checked")) {
                other_tmp.val(other_input.val());
                other_tmp.show();
                other_tmp_radio.attr("checked", false);
                other_input.hide();
                other_input.val('');
            }
        }
    });
}
