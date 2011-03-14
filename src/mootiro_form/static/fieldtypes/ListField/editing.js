// Template of a List Option
$.template('optTemplate', "<div id='${$item.idx}'><input name='defOpt' class='multipleChoice' {{if opt_default}}checked='yes'{{/if}} type='checkbox'/><input class='editOptionLabel' type='text' name='optionLabel' value='${label}'/>" +
                          "<img class='moveOpt' alt='Add option' title='Move option' src='/" + route_url('root') + "static/img/icons-edit/moveOpt.png'/>\n" +
                          "<img class='addOpt' alt='Add option' title='Add option' src='/" + route_url('root') + "static/img/icons-edit/addOpt.png'/>\n" +
                          "<img class='deleteOpt' alt='Delete option' title='Delete option' src='/" + route_url('root') + "static/img/icons-edit/deleteOpt.png'/>\n</div>" );

// Template of "Multiple Choices" selector
$.template('multipleChoice', "<div>Multiple choice? <input type='checkbox' class='multipleChoice' {{if checked}}checked{{/if}} name='multipleChoice'/></div>");

// Template of "Sort" selector
$.template('sortChoices', "<div>Sort:<select id='sortChoicesSelect' name='sortChoices'>" +
       "<option {{if sort_choices == 'user_defined'}}selected{{/if}} value='user_defined'>No</option>" + 
       "<option {{if sort_choices == 'alpha_asc'}}selected{{/if}} value='alpha_asc'>Alphabetic Asc</option>" + 
       "<option {{if sort_choices == 'alpha_desc'}}selected{{/if}} value='alpha_desc'>Alphabetic Desc</option>" + 
       "<option {{if sort_choices == 'random'}}selected{{/if}} value='random'>Random</option>" +
       "</select></div>");

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
            multiple_choice: false,
            export_in_columns: false,
            options: {}
        };
        this.props.options['option_' + fieldId.next()] =
            {option_id:'new', label:'option 1', value:'',
             opt_default: true, position: 0};
    }
}

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
    var tplContext = {props: this.props,
        fieldTpl: this.template[this.props.list_type]};
    return $.tmpl('fieldBase', tplContext);
}

ListField.prototype.renderOptions = function () {
    var instance = this;
    domOptions = $.tmpl(this.optionsTemplate, this.props);

    var multipleSelector = $.tmpl('multipleChoice',
        {checked: instance.props.multiple_choice});

    multipleSelector.appendTo($('#multipleChoice', domOptions));

    if (instance.props.list_type != 'select') {
        $('#not_radio_options', domOptions).hide();
    }

    $('input[name=multipleChoice]', domOptions).change(function () {
        if ($(this).attr('checked')) {
            instance.props.multiple_choice = true;
            fields.redrawPreview(instance);
        } else {
            instance.props.multiple_choice = false;
            fields.redrawPreview(instance);
        }
    });

    if (instance.props.new_option) {
       $('#NewOption', domOptions).attr({checked: true});
    }

    $('#NewOption', domOptions).change(function () {
        if ($(this).attr('checked')) {
            instance.props.new_option = true;
            fields.redrawPreview(instance);
        } else {
            instance.props.new_option = false;
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
            if (instance.props.list_type != 'select') { 
                $('#not_radio_options').hide();
                if (instance.props.list_type == 'radio') { 
                    $.each($('input[name=defOpt]:checked', domOptions), function (idx, opt) {
                        if (idx != 0) {
                            $(opt).attr({checked: false});
                        }
                    });
                }
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

ListField.prototype.optionsTemplate = $.template(
  "<div><input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
  "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<textarea id='EditLabel' name='label'>${label}</textarea> \n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
  "<input type='checkbox' id='EditRequired' name='required' />\n" +
  "<label for='EditRequired'>required</label>\n" +
  "<p/><b>List type</b><p/>\n" +
  "<select name='listType' id='listType'>\n" +
  "<option {{if list_type == 'select'}}selected{{/if}} value='select'>select</option>\n" +
  "<option {{if list_type == 'radio'}}selected{{/if}} value='radio'>radio</option>" + 
  "<option {{if list_type == 'checkbox'}}selected{{/if}} value='checkbox'>checkbox</option></select>" + 
  "<div id='not_radio_options'><div id='multipleChoice'/>" +
  "<div id='sizeOptions'>Size:<input type='text' class='size_options' name='size_options' value='${size_options}'/></div>" +
  "</div>" +
  "<div id='sortChoices'>{{tmpl($data) 'sortChoices'}}</div>" +
  "'Other' option?<input type='checkbox' id='NewOption' name='new_option' />\n" +
  "<br/>Export in columns?<input type='checkbox' id='ExportInColumns' name='export_in_columns' />\n" +
  "<p/><b>List options</b><div id='listOptions'>{{tmpl($data) 'options-edit'}}\n" 
  );

ListField.prototype.optionsEditTemplate = $.template("options-edit",
  "{{each options}}{{tmpl($value, {idx: $index}) 'optTemplate'}}" + 
  "{{/each}}\n"
   );

ListField.prototype.option_template = {};
ListField.prototype.option_template['select'] = $.template("option-select",
        "{{each optionsSort(options, sort_choices)}}<option {{if opt_default}}selected='yes'{{/if}} value='${id}'>${label}</option>{{/each}}"
        );

// Checkbox Option Template
ListField.prototype.option_template = {};
ListField.prototype.option_template['checkbox'] = $.template("option-checkbox",
        "{{each optionsSort(options, sort_choices)}}<input disabled type='checkbox' {{if opt_default}}checked='yes'{{/if}} value='${id}'>${label}<br/>{{/each}}"
        );

// Radio Option Template
ListField.prototype.option_template['radio'] = $.template("option-radio",
        "{{each optionsSort(options, sort_choices)}}<input disabled type='radio' name='radio-${$data.id}' {{if opt_default}}checked='yes'{{/if}} value='${option_id}'>${label}</input><br/>{{/each}}"
        );

ListField.prototype.template = {};
ListField.prototype.template['select'] = $.template(
  "<select disabled size=${size_options} {{if multiple_choice}}multiple='multiple'{{/if}} name='select-${id}' id='${id}'>\n" +
  "{{tmpl($data) 'option-select'}}</select>{{if new_option}}<p/>Other: <input type='text' name='other-${id}'/>{{/if}}");

ListField.prototype.template['checkbox'] = $.template(
        "{{each optionsSort(options, sort_choices)}}<input disabled type='checkbox' {{if opt_default}}checked='yes'{{/if}} value='${id}'>${label}<br/>{{/each}}{{if new_option}}<p/>Other: <input type='text' name='other-${id}'/>{{/if}}"
        );

ListField.prototype.template['radio'] = $.template(
        "{{each optionsSort(options, sort_choices)}}<input disabled type='radio' name='radio-${$data.id}' {{if opt_default}}checked='yes'{{/if}} value='${option_id}'>${label}</input><br/>{{/each}}{{if new_option}}<p/>Other: <input type='text' name='other-${id}'/>{{/if}}"
        );


// Methods

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
  this.props.new_option = $('#NewOption').attr('checked');
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

ListField.prototype.addBehaviour = function () {
};

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
