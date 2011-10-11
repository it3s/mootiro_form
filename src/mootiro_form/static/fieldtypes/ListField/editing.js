// Constructor
function ListField(props) {
    this.defaultLabel = _('List of options');
    if (props) {
        this.props = props;
        this.props.deleteOptions = [];
        this.props.id = fieldId.nextString();
        var optionsDict = {};
        $.each(this.props.options, function (idx, opt) {
            optionsDict['option_' + fieldId.next()] = opt;
        });
        this.props.options = optionsDict;
    } else {
        this.props = mergeNewFieldProps({
            type: 'ListField',
            label: this.defaultLabel,
            defaul: '',
            list_type : 'select',
            sort_choices : 'user_defined',
            size_options : 1,
            deleteOptions : [],
            new_option: false,
            new_option_label: _('Other'),
            min_num: 1,
            max_num: '',
            case_sensitive: true,
            moderated: true,
            multiple_choice: false,
            opt_restrictions: false,
            //export_in_columns: false,
            options: {}
        });
        this.props.options['option_' + fieldId.next()] =
            {option_id:'new', label:_('option 1'), value:'',
             opt_default: true, position: 0};
    }
}

ListField.prototype.load = function () {
    if (!$('#optionsTemplate').data('tmpl')) {
        $.get('/static/fieldtypes/ListField/_list.tmpl.html',
          function (template) {
            $('body').append(template);
            $.template('optTemplate', $('#optTemplate'));
            $.template('multipleChoice', $('#multiplechoice'));
            $.template('optionsTemplate', $('#optionsTemplate'));
            $.template('options-edit', $('#options-edit'));
            $.template('options-select', $('#options-select'));
            $.template('options-checkbox', $('#options-checkbox'));
            $.template('options-moderation', $('#options-moderation'));
            $.template('options-radio', $('#options-radio'));
            $.template('selectPreview', $('#selectPreview'));
            $.template('checkboxPreview', $('#checkboxPreview'));
            $.template('radioPreview', $('#radioPreview'));
            $.template('sortChoices', $('#sortChoices'));
        });
    }
}

ListField.prototype.template = {'select': 'selectPreview',
    'checkbox': 'checkboxPreview',
    'radio': 'radioPreview'
};

function optionsSort(options, sort_choices) {
    var optList = [];
    var listTypeSort = function(sc) {
        switch(sc) {
            case 'alpha_asc':
                return function (a,b) { return a.label > b.label };
            case 'alpha_desc':
                return function (a,b) { return a.label < b.label };
            default:
                return function (a,b) { return a.position > b.position };
        }
    }

    $.each(options, function (idx, ele) {
        optList.push(ele);
    });

    if (sort_choices != 'random') {
        return optList.sort(listTypeSort(sort_choices));
    } else {
        var list_length = optList.length;

        while (--list_length) {
            var j = Math.floor(Math.random() * (list_length + 1));
            var temp = optList[list_length];
            optList[list_length] = optList[j];
            optList[j] = temp;
        }

        return optList;
    }
}

ListField.prototype.renderPreview = function () {
    var tplContext = {props: this.props,
        fieldTpl: this.template[this.props.list_type]};
    return $.tmpl('FieldBase', tplContext);
}

ListField.prototype.renderOptions = function () {
    var instance = this;
    var props = this.props;
    var tplContext = {props: props,
        BottomBasicOptionsTpl: this.bottomBasicOptionsTemplate,
        AdvancedOptionsTpl: 'optionsTemplate'};
    domOptions = $.tmpl('optionsBase', tplContext);

    /* Multiple Choice Parameters */

    /* Multiple choice parameters template */
    var multipleSelector = $.tmpl('multipleChoice',
        {checked: props.multiple_choice});

    /* If has multiple options parameters, show it */
    if (props.multiple_choice || props.list_type == 'checkbox') {
        $('#multipleChoiceOptions', domOptions).show();
        /* Size exists only in select lists */
        if (props.list_type != 'select') {
            $('#sizeOptions', domOptions).hide();
        }
    } else {
        $('#list_size', domOptions).attr('disabled', 'disabled');
        $('#multipleChoiceOptions', domOptions).hide();
    }

    multipleSelector.appendTo($('#multipleChoice', domOptions));

    if (props.list_type != 'select') {
        $('#allow_multiple', domOptions).hide();
    }

    if (props.list_type == 'radio') {
        $('#not_radio_options', domOptions).hide();
    }

    if (props.opt_restrictions) {
        $("#opt_rest_checkbox", domOptions).attr("checked", true);
        $('#opt_restrictions', domOptions).show();
    } else {
        $('#opt_restrictions', domOptions).hide();
    }

    $("#opt_rest_checkbox", domOptions).change(function () {
        if ($(this).attr('checked')) {
            props.opt_restrictions = true;
            $('#opt_restrictions', domOptions).show();
        } else {
            props.opt_restrictions = false;
            $('#opt_restrictions', domOptions).hide();
        }
    });

    /* Automatic preview after changes in multiple choices parameters */
    $('input[name=multipleChoice]', domOptions).change(function () {
        if ($(this).attr('checked')) {
            props.multiple_choice = true;
            $('#multipleChoiceOptions', domOptions).show();

            if (props.list_type != 'select') {
                $('#sizeOptions', domOptions).hide();
            } else {
                $('#list_size', domOptions).attr('disabled', '');
            }
        } else {
            props.multiple_choice = false;
            $('#list_size', domOptions).attr('disabled', 'disabled');
            if (instance.props.list_type != 'checkbox') {
                $('#multipleChoiceOptions', domOptions).hide();
            }
        }
        fields.redrawPreview(instance);
    });

    if (props.required) {
        $('#EditRequired', domOptions).attr({checked: true});
    }

    /* Moderation of new alternatives */

    /* Show new option parameter if configured */
    if (props.new_option) {
       $('#NewOption', domOptions).attr({checked: true});
       $('#otherOpt', domOptions).show();
    } else {
       $('#otherOpt', domOptions).hide();
    }
    $('#NewOption', domOptions).change(function () {
        if ($(this).attr('checked')) {
            props.new_option = true;
            $('#otherOpt', domOptions).show();
        } else {
            props.new_option = false;
            $('#otherOpt', domOptions).hide();
        }
        fields.redrawPreview(instance);
    });

    /* Configure new option label */
    $('#NewOptionLabel', domOptions).keyup(function() {
        props.new_option_label = $(this).val();
        fields.redrawPreview(instance);
    });

    /* Configure if moderated */
    if (props.moderated) {
        $('#manual_approval', domOptions).attr('checked', 'checked');
    } else {
        $('#automatic_approval', domOptions).attr('checked', 'checked');
    }

    /* Case sensitive options */
    if (props.case_sensitive) {
        $('#CaseSensitive', domOptions).attr({checked: true});
    } else {
        $('#CaseSensitive', domOptions).attr({checked: false});
    }

    /* Configure buttons to moderate */
    $('#aprove_options', domOptions).click(function () {
       $('#moderate_options_list option:selected').each(function () {
           var value = $(this).val();
           var new_options_moderation = $.grep(props.options_moderation, function (e,i) {
               return e.option_id.toString() !== value;
           });
           props.options_moderation = new_options_moderation;
           var opt_idx = 'option_' + fieldId.next();
           $(newOptionDom).attr({id: opt_idx});
           var newOption = {
               id: opt_idx,
               option_id: $(this).val(),
               label: $(this).text(),
               value: $(this).val(),
               opt_default: false,
               status: 'Approved',
               position: $('input[type=text]', '#listOptions').length
           };
           var newOptionDom = $.tmpl('optTemplate', newOption);
           props.options[opt_idx] = newOption;
           $('input[type=text]', newOptionDom)[0].opt_idx = opt_idx;
           $('input[type=text]', newOptionDom)[0].option = newOption;
           $('#listOptions').after(newOptionDom[0]);
           fields.redrawPreview(instance);
           buttonsBehaviour(newOptionDom);
           $(this).remove();
       });
    }).button();

    $('#exclude_options', domOptions).click(function () {
        $('#moderate_options_list option:selected').each(function () {
            var value = $(this).val();
            var new_options_moderation = $.grep(instance.props.options_moderation, function (e,i) {
                return e.option_id.toString() !== value;
            });
            props.options_moderation = new_options_moderation;
            props.deleteOptions.push($(this).val());
            $(this).remove();
        });
    }).button();

    var inputOptions = $('input[name="optionLabel"]', domOptions);
    var i = 0;
    $.each(props.options, function (idx, opt) {
        inputOptions[i].option = opt;
        inputOptions[i].opt_idx = idx;
        ++i;
    });

    $('#sortChoicesSelect', domOptions).change(function () {
       fields.saveCurrent();
       fields.redrawPreview(instance);
    });

    var buttonsBehaviour = function (dom) {
        $('#list_size', dom).change(function () {
            props.list_size = $('option:selected', this).val();
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });

        $('.deleteOpt', dom).click(function () {
            var delOptId = $(this).siblings('input[type=text]')[0].option.option_id;
            var delOptIdx = $(this).siblings('input[type=text]')[0].opt_idx;
            if (delOptId != 'new') {
                props.deleteOptions.push(delOptId);
            }
            delete(props.options[delOptIdx]);
            $(this).parent().remove();
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });

        $('.addOpt', dom).click(function () {
           var opt_idx = 'option_' + fieldId.next();
           var newOptionDom = $.tmpl('optTemplate');
           $(newOptionDom).attr({id: opt_idx});
           var newOption = {id: opt_idx, option_id:'new', label:'', value:'',
                      opt_default: false, position: 0, status: 'Form owner'};
           props.options[opt_idx] = newOption;
           $('input[type=text]', newOptionDom)[0].opt_idx = opt_idx;
           $('input[type=text]', newOptionDom)[0].option = newOption;
           $(this).parent().after(newOptionDom[0]);
           fields.redrawPreview(instance);
           buttonsBehaviour(newOptionDom);
        });

        $('#EditRequired', domOptions).change(function () {
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });

        $('input[name=defOpt]', dom).change(function () {
            $(this).next()[0].option.opt_default = $(this).attr('checked');
            var opt_idx = $(this).next()[0].opt_idx;
            if (props.list_type == 'radio') {
                $.each($('input[name=defOpt]', dom), function (idx, opt) {
                    if ($(opt).next()[0].opt_idx != opt_idx) {
                        $(opt).attr({checked: false});
                    }
                });
            }
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });

        /* Redraw field when changing option label */
        $('.editOptionLabel', dom).keyup(function (event) {
            fields.saveCurrent();
            fields.redrawPreview(instance);
            if (event.keyCode == '13') {
                var opt_idx = 'option_' + fieldId.next();
                var newOptionDom = $.tmpl('optTemplate');
                $(newOptionDom).attr({id: opt_idx});
                var newOption = {id: opt_idx, option_id:'new', label:'',
                    value:'', status: 'Form owner', opt_default: false,
                    position: 0};
                props.options[opt_idx] = newOption;
                $('input[type=text]', newOptionDom)[0].opt_idx = opt_idx;
                $('input[type=text]', newOptionDom)[0].option = newOption;
                $(this).parent().after(newOptionDom[0]);
                fields.redrawPreview(instance);
                $('input[type=text]', newOptionDom).focus();
                buttonsBehaviour(newOptionDom);
            }
        });

        var updateOptionsOrder = function (event, ui) {
            var order = $('#listOptions', dom).sortable('toArray');
            $.each(order, function (idx, opt) {
                props.options[opt].position = idx;
            });
            fields.redrawPreview(instance);
        };

        /* Redraw field when changing list type */
        $('#listType', dom).change(function () {
            props.list_type = $('option:selected', this).val();
            if (props.list_type == 'select') {
                $('#not_radio_options').show();
                $('#allow_multiple', domOptions).show();
                $('#sizeOptions', domOptions).show();
            } else if (props.list_type == 'checkbox') {
                $('#multipleChoiceOptions').show();
                $('#not_radio_options').show();
                $('#allow_multiple', domOptions).hide();
                $('#sizeOptions', domOptions).hide();
            } else {
                $('#allow_multiple', domOptions).hide();
                $('#sizeOptions', domOptions).hide();
                $('#not_radio_options').hide();
                $.each($('input[name=defOpt]:checked', domOptions),
                  function (idx, opt) {
                    if (idx != 0) {
                        $(opt).attr({checked: false});
                    }
                  }
                );
            }
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });
        $('#listOptions', dom).sortable({handle: '.moveOpt',
                                         update: updateOptionsOrder});
    };
    buttonsBehaviour(domOptions);
    return domOptions;
}

ListField.prototype.update = function (data) {
    var instance = this;
    $.each(data.insertedOptions, function (o_idx, o_id) {
        instance.props.options[o_idx].option_id = o_id;
    });
}

ListField.prototype.save = function() {
    // Copies to props the information in the left form
    var p = this.props;
    p.label = $('#EditLabel').val();
    p.defaul = '';
    p.required = $('#EditRequired').attr('checked');
    p.list_type = $('#listType option:selected').val();
    p.description = $('#EditDescription').val();
    p.sort_choices = $('#sortChoicesSelect option:selected').val();
    p.size_options = $('#list_size option:selected').val();
    p.multiple_choice = $('input[name=multipleChoice]').attr('checked');
    p.min_num = $('input[name=min_num]').val();
    p.max_num = $('input[name=max_num]').val();
    p.new_option = $('#NewOption').attr('checked');
    p.new_option_label = $('#NewOptionLabel').val();
    p.moderated = $('#manual_approval').is(':checked');
    p.case_sensitive = $('#CaseSensitive').attr('checked');
    $('input[name=defOpt]').each(function (idx, ele) {
        $(this).next()[0].option.opt_default = $(this).attr('checked');
    });
    $('input[name="optionLabel"]').each(function (idx, ele) {
        $(this)[0].option.label = $(this).val();
    });
    var order = $('#listOptions').sortable('toArray');
    $.each(order, function (idx, opt) {
        p.options[opt].position = idx;
    });
}

ListField.prototype.clone = function (original) {
    // This is called when a field has just been cloned.
    // `original` is the first field, from which this was cloned.
    // The options are new objects already, but their IDs must change:
    var newOptions = {};
    $.each(this.props.options, function (idx, opt) {
        var id = fieldId.next();
        opt.option_id = 'new';
        newOptions['option_' + id] = opt;
    });
    this.props.options = newOptions;
    // Discard any "other" options pending approval
    this.props.options_moderation = [];
}


$('img.ListFieldIcon').hover(function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ListField/iconHover.png'});
}, function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ListField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ListField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ListField/iconHover.png'});
});
