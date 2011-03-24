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
        $.template('options-radio', $('#options-radio'));
        $.template('selectPreview', $('#selectPreview'));
        $.template('checkboxPreview', $('#checkboxPreview'));
        $.template('radioPreview', $('#radioPreview'));
        $.template('sortChoices', $('#sortChoices'));
    });
}

// Constructor
function ListField(props) {
    this.defaultLabel = 'List field';
    if (props) {
        this.props = props;
        this.props.deleteOptions = [];
        this.props.id = fieldId.nextString();
        optionsDict = {};
        $.each(this.props.options, function (idx, opt) {
            optionsDict['option_' + fieldId.next()] = opt;
        });
        this.props.options = optionsDict;
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'ListField',
            label : this.defaultLabel,
            defaul : '',
            description : '',
            required : false,
            list_type : 'select',
            sort_choices : 'user_defined',
            size_options : 1,
            deleteOptions : [],
            new_option: false,
            new_option_label: 'Other',
            min_number: 1,
            max_number: '',
            multiple_choice: false,
            export_in_columns: false,
            options: {}
        };
        this.props.options['option_' + fieldId.next()] =
            {option_id:'new', label:'option 1', value:'',
             opt_default: true, position: 0};
    }
}

ListField.prototype.template = {};
ListField.prototype.template['select'] = 'selectPreview';
ListField.prototype.template['checkbox'] = 'checkboxPreview';
ListField.prototype.template['radio'] = 'radioPreview';

var optionsSort = function (options, sort_choices) {
    var optList = [];
    var listTypeSort = function(sc) {
        switch(sc) {
            case 'alpha_asc':
                return function (a,b) { return a.label > b.label }; 
            case 'alpha_desc':
                return function (a,b) { return a.label < b.label }; 
            case 'random':
                return function (a,b) {
                    var temp = parseInt( Math.random()*10 );
                    var isOddOrEven = temp%2;
                    var isPosOrNeg = temp>5 ? 1 : -1;

                    return isOddOrEven*isPosOrNeg;
                }
            default:
                return function (a,b) { return a.position > b.position }; 
        }
    }

    $.each(options, function (idx, ele) {
        optList.push(ele);
    });

    return optList.sort(listTypeSort(sort_choices));
}

ListField.prototype.renderPreview = function () {
    var instance = this;
    var tplContext = {props: instance.props, 
        fieldTpl: instance.template[instance.props.list_type]};
    return $.tmpl('fieldBase', tplContext);
}

ListField.prototype.renderOptions = function () {
    var instance = this;
    domOptions = $.tmpl('optionsTemplate', this.props);

    var multipleSelector = $.tmpl('multipleChoice',
        {checked: instance.props.multiple_choice});

    if (instance.props.multiple_choice) {
        $('#multipleChoiceOptions', domOptions).show();
    } else {
        $('#multipleChoiceOptions', domOptions).hide();
    }

    multipleSelector.appendTo($('#multipleChoice', domOptions));

    if (instance.props.list_type == 'radio') {
        $('#not_radio_options', domOptions).hide();
    }

    $('input[name=multipleChoice]', domOptions).change(function () {
        if ($(this).attr('checked')) {
            instance.props.multiple_choice = true;
            $('#multipleChoiceOptions', domOptions).show();
            fields.redrawPreview(instance);
        } else {
            instance.props.multiple_choice = false;
            $('#multipleChoiceOptions', domOptions).hide();
            fields.redrawPreview(instance);
        }
    });

    if (instance.props.new_option) {
       $('#NewOption', domOptions).attr({checked: true});
       $('#otherOpt', domOptions).show();
    } else {
       $('#otherOpt', domOptions).hide();
    }

    $('#NewOptionLabel', domOptions).keyup(function() {
      instance.props.new_option_label = $(this).val();
      fields.redrawPreview(instance); 
    });

    $('#NewOption', domOptions).change(function () {
        if ($(this).attr('checked')) {
            instance.props.new_option = true;
            $('#otherOpt', domOptions).show();
            fields.redrawPreview(instance);
        } else {
            instance.props.new_option = false;
            $('#otherOpt', domOptions).hide();
            fields.redrawPreview(instance);
        }
    });

    if (instance.props.export_in_columns == 'true') {
       $('#ExportInColumns', domOptions).attr({checked: true});
    }

    var inputOptions = $('input[name="optionLabel"]', domOptions);
    var i = 0;
    $.each(instance.props.options, function (idx, opt) {
        inputOptions[i].option = opt;
        inputOptions[i].opt_idx = idx;
        ++i;
    });
    
    $('#sortChoicesSelect', domOptions).change(function () {
       fields.saveCurrent();
       fields.redrawPreview(instance);
    });

    var buttonsBehaviour = function (dom) {

        $('.size_options', dom).keyup(function () {
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });

        $('.deleteOpt', dom).click(function () {
            var delOptId = $(this).siblings('input[type=text]')[0].option.option_id;
            var delOptIdx = $(this).siblings('input[type=text]')[0].opt_idx;
            if (delOptId != 'new') {
                instance.props.deleteOptions.push(delOptId);
            }
            delete(instance.props.options[delOptIdx]);
            $(this).parent().remove();
            fields.saveCurrent();
            fields.redrawPreview(instance);
        });

        $('.addOpt', dom).click(function () {
           var opt_idx = 'option_' + fieldId.next();
           var newOptionDom = $.tmpl('optTemplate');
           $(newOptionDom).attr({id: opt_idx});
           var newOption = {id: opt_idx, option_id:'new', label:'', value:'', opt_default: false, position: 0};
           instance.props.options[opt_idx] = newOption;
           $('input[type=text]', newOptionDom)[0].opt_idx = opt_idx;
           $('input[type=text]', newOptionDom)[0].option = newOption;
           $(this).parent().after(newOptionDom[0]);  
           fields.redrawPreview(instance);
           buttonsBehaviour(newOptionDom);
        });

        $('input[name=defOpt]', dom).change(function () {
            $(this).next()[0].option.opt_default = $(this).attr('checked');
            var opt_idx = $(this).next()[0].opt_idx;
            if (instance.props.list_type == 'radio') {
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
                var newOption = {id: opt_idx, option_id:'new', label:'', value:'', opt_default: false, position: 0};
                instance.props.options[opt_idx] = newOption;
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
                instance.props.options[opt].position = idx;
            });
            
            fields.redrawPreview(instance);
        };


        /* Redraw field when changing list type */
        $('#listType', dom).change(function () {
            instance.props.list_type = $('option:selected', this).val();
            if (instance.props.list_type == 'radio') { 
                $('#not_radio_options').hide();
                    $.each($('input[name=defOpt]:checked', domOptions), function (idx, opt) {
                        if (idx != 0) {
                            $(opt).attr({checked: false});
                        }
                    });
            } else {
                $('#not_radio_options').show();
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

// Fields

ListField.prototype.update = function (data) {
    var instance = this;
    $.each(data.insertedOptions, function (o_idx, o_id) {
        instance.props.options[o_idx].option_id = o_id;
    }); 
}

ListField.prototype.save = function() {
  var instance = this;
  // Copies to props the information in the left form
  this.props.label = $('#EditLabel').val();
  this.props.defaul = '';
  this.props.list_type = $('#listType option:selected').val();
  this.props.required = $('#EditRequired').attr('checked');
  this.props.description = $('#EditDescription').val();
  this.props.sort_choices = $('#sortChoicesSelect option:selected').val();
  this.props.size_options = $('input.size_options').val();
  this.props.min_num = $('input[name=min_num]').val();
  this.props.max_num = $('input[name=max_num]').val();
  this.props.new_option = $('#NewOption').attr('checked');
  this.props.new_option_label = $('#NewOptionLabel').val();
  this.props.export_in_columns = $('#ExportInColumns').attr('checked');
  $('input[name=defOpt]').each(function (idx, ele) {
    $(this).next()[0].option.opt_default = $(this).attr('checked');
  });
  $('input[name="optionLabel"]').each(function (idx, ele) {
    $(this)[0].option.label = $(this).val();
  });
  var order = $('#listOptions').sortable('toArray');

  $.each(order, function (idx, opt) {
      instance.props.options[opt].position = idx;
  });
 
}

// Register it
fields.types['ListField'] = ListField;

$('img.ListFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/ListField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/ListField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/ListField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/ListField/iconHover.png'});
});
