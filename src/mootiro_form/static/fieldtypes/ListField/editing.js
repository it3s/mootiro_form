
// Template of a List Option
$.template('optTemplate', "<div id='${$item.idx}'><input name='defOpt' class='multipleChoice' {{if opt_default}}checked='yes'{{/if}} type='checkbox'/><input class='editOptionLabel' type='text' name='optionLabel' value='${label}'/>" +
                          "<img class='moveOpt' alt='Add option' title='Move option' src='" + route_url('root') + "static/img/icons-edit/moveOpt.png'/>\n" +
                          "<img class='addOpt' alt='Add option' title='Add option' src='" + route_url('root') + "static/img/icons-edit/addOpt.png'/>\n" +
                          "<img class='deleteOpt' alt='Delete option' title='Delete option' src='" + route_url('root') + "static/img/icons-edit/deleteOpt.png'/>\n</div>" );

// Template of "Multiple Choices" selector
$.template('multipleChoice', "<div>Multiple choice? <input type='checkbox' class='multipleChoice' {{if checked}}checked{{/if}} name='multipleChoice'/></div>");


// Template of "Sort" selector
$.template('sortChoices', "<div>Sort:<select id='sortChoicesSelect' name='sortChoices'>" +
       "<option value='alpha_asc'>Alphabetic Asc</option>"+ 
       "<option value='alpha_desc'>Alphabetic Desc</option>"+ 
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
            deleteOptions : [],
            multiple_choice: false,
            options: {}
        };
        this.props.options['option_' + fieldId.next()] = {option_id:'new', label:'option 1', value:'', opt_default: true, position: 0};
    }
}

ListField.prototype.render = function () {
    return $.tmpl(this.template[this.props.list_type], this.props);
}

ListField.prototype.renderOptions = function () {
    var instance = this;
    domOptions = $.tmpl(this.optionsTemplate, this.props);

    var multipleSelector = $.tmpl('multipleChoice', {checked: instance.props.multiple_choice});

    multipleSelector.appendTo($('#multipleChoice', domOptions));

    $('input[name=multipleChoice]', domOptions).change(function () {
        if ($(this).attr('checked')) {
            instance.props.multiple_choice = true;
            instance.redraw();
        } else {
            instance.props.multiple_choice = false;
            instance.redraw();
        }
    });
 
    var inputOptions = $('input[name="optionLabel"]', domOptions);
    var i = 0;
    $.each(instance.props.options, function (idx, opt) {
        inputOptions[i].option = opt;
        inputOptions[i].opt_idx = idx;
        ++i;
    });
    
    $('#sortChoicesSelect', domOptions).change(function () {
 //       $('#listOptions').qsort();
    });

    var buttonsBehaviour = function (dom) {

        $('.deleteOpt', dom).click(function () {
            var delOptId = $(this).siblings('input[type=text]')[0].option.option_id;
            var delOptIdx = $(this).siblings('input[type=text]')[0].opt_idx;
            if (delOptId != 'new') {
                instance.props.deleteOptions.push(delOptId);
            }
            delete(instance.props.options[delOptIdx]);
            $(this).parent().remove();
            instance.save();
            instance.redraw();
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
           instance.redraw();
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
            instance.save();
            instance.redraw();
        });

       /* Redraw field when changing option label */
       $('.editOptionLabel', dom).keyup(function () {
           instance.save();
           instance.redraw();
       });

       var updateOptionsOrder = function (event, ui) {
           var order = $('#listOptions', dom).sortable('toArray');

           $.each(order, function (idx, opt) {
               instance.props.options[opt].position = idx;
           });
           
           instance.redraw();
       };
   
       $('#listOptions', dom).sortable({handle: '.moveOpt',
                                        update: updateOptionsOrder});

    };

    buttonsBehaviour(domOptions);

    /* Redraw field when changing list type */
    $('#listType', domOptions).change(function () {
        instance.props.list_type = $('option:selected', this).val();
        if (instance.props.list_type == 'radio') { 
            $.each($('input[name=defOpt]:checked', domOptions), function (idx, opt) {
                if (idx != 0) {
                    $(opt).attr({checked: false});
                }
            });
        } 
        instance.save();
        instance.redraw();
    });

    return domOptions;
}

// Fields

ListField.prototype.optionsTemplate = $.template(
  "<div><input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
  "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
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
  "<div id='multipleChoice'/>" +
  "<div id='sortChoices'>{{tmpl($data) 'sortChoices'}}</div>" +
  "<p/><b>List options</b><div id='listOptions'>{{tmpl($data) 'options-edit'}}\n" 
  );

ListField.prototype.optionsEditTemplate = $.template("options-edit",
  "{{each options}}{{tmpl($value, {idx: $index}) 'optTemplate'}}" + 
  "{{/each}}\n"
   );

ListField.prototype.option_template = {};
ListField.prototype.option_template['select'] = $.template("option-select",
        "{{each options}}<option {{if opt_default}}selected='yes'{{/if}} value='${id}'>${label}</option>{{/each}}"
        );

// Checkbox Option Template
ListField.prototype.option_template = {};
ListField.prototype.option_template['checkbox'] = $.template("option-checkbox",
        "{{each options}}<input type='checkbox' {{if opt_default}}checked='yes'{{/if}} value='${id}'>${label}<br/>{{/each}}"
        );

// Radio Option Template
ListField.prototype.option_template['radio'] = $.template("option-radio",
        "{{each options}}<input type='radio' name='radio-${$data.id}' {{if opt_default}}checked='yes'{{/if}} value='${option_id}'>${label}</input><br/>{{/each}}"
        );

ListField.prototype.template = {};
ListField.prototype.template['select'] = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "<select {{if multiple_choice}}multiple='multiple'{{/if}} name='select-${id}' id='${id}'>\n" +
  "{{tmpl($data) 'option-select'}}</select>" +
  "</li>\n");

ListField.prototype.template['checkbox'] = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "{{tmpl($data) 'option-checkbox'}}" +
  "</li>\n");

ListField.prototype.template['radio'] = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "{{tmpl($data) 'option-radio'}}" +
  "</li>\n");

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

ListField.prototype.redraw = function () {
  $('#' + this.props.id + '_container').html($(this.render()).html());
  this.addBehaviour();
}

ListField.prototype.addBehaviour = function () {
  var instance = this;
  var labelSelector = '#' + this.props.id + 'Label';

  var instantFeedback = function () {
      setupCopyValue({from:'#EditLabel', to:labelSelector, defaul:'Question'});
      setupCopyValue({from:'#EditDescription', to:'#' + instance.props.id +
          'Description', defaul:null, br:true});
      $('#EditRequired').change(function (e) {
        var origin = $('#EditRequired');
        var dest = $('#' + instance.props.id + 'Required');
        if (origin.attr('checked'))
            dest.html('*');
        else
            dest.html('');
      });
  }

  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  var funcForOnClickEdit = function (target, defaul) {
    return function () {
      fields.switchToEdit(instance);
      instantFeedback();
      $(target).focus();
      // Sometimes also select the text. (If it is the default value.)
      if ($(target).val() === defaul) $(target).select();
      return false;
    };
  };

  $(labelSelector).click(funcForOnClickEdit('#EditLabel', this.defaultLabel));
  $('#' + this.props.id).click(funcForOnClickEdit('#EditDefault'));
  $('#' + this.props.id + 'Description')
    .click(funcForOnClickEdit('#EditDescription'));


};

// Register it
fields.types['ListField'] = ListField;
