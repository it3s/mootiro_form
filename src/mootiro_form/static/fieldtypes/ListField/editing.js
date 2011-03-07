$.template('optTemplate', "<div><input name='defOpt' class='multipleChoice' {{if opt_default}}checked='yes'{{/if}} type='checkbox'/><input class='editOptionLabel' type='text' name='optionLabel' value='${label}'/>" +
                          "<img class='moveOpt' alt='Add option' title='Move option' src='" + route_url('root') + "/static/img/icons-edit/moveOpt.png'/>\n" +
                          "<img class='addOpt' alt='Add option' title='Add option' src='" + route_url('root') + "/static/img/icons-edit/addOpt.png'/>\n" +
                          "<img class='deleteOpt' alt='Delete option' title='Delete option' src='" + route_url('root') + "/static/img/icons-edit/deleteOpt.png'/>\n</div>" );

$.template('multipleChoice', "<div>Multiple choice? <input type='checkbox' class='multipleChoice' {{if checked}}checked{{/if}} name='multipleChoice'/></div>");

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
        this.props.options['option_' + fieldId.next()] = {option_id:'new', label:'option 1', value:'', opt_default: true};
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
           var newOptionDom = $.tmpl('optTemplate');
           var newOption = {option_id:'new', label:'', value:'', opt_default: false};
           var opt_idx = 'option_' + fieldId.next();
           instance.props.options[opt_idx] = newOption;
           $('input[type=text]', newOptionDom)[0].opt_idx = opt_idx;
           $('input[type=text]', newOptionDom)[0].option = newOption;
           $('#listOptions').append(newOptionDom[0]);  
           instance.redraw();
           buttonsBehaviour(newOptionDom);
        });

        $('input[name=defOpt]', domOptions).change(function () {
            $(this).next()[0].option.opt_default = $(this).attr('checked');
            instance.redraw();
        });

       /* Redraw field when changing option label */
       $('.editOptionLabel', dom).keyup(function () {
           instance.save();
           instance.redraw();
       });

    };

    buttonsBehaviour(domOptions);

    $('#listOptions', domOptions).sortable({handle: '.moveOpt'});

    /* Redraw field when changing list type */
    $('#listType', domOptions).change(function () {
        instance.props.list_type = $('option:selected', this).val();
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
  "<option {{if list_type == 'radio'}}selected{{/if}} value='radio'>radio</option></select>" + 
  "<div id='multipleChoice'/>" +
  "<p/><b>List options</b><div id='listOptions'>{{tmpl($data) 'options-edit'}}\n" 
  );

ListField.prototype.optionsEditTemplate = $.template("options-edit",
  "{{each options}}{{tmpl($value) 'optTemplate'}}" + 
  "{{/each}}\n"
   );

ListField.prototype.option_template = {};
ListField.prototype.option_template['select'] = $.template("option-select",
        "{{each options}}<option {{if opt_default}}selected='yes'{{/if}} value='${id}'>${label}</option>{{/each}}"
        );

ListField.prototype.option_template['radio'] = $.template("option-radio",
        "{{each options}}<input type='radio' name='radio-${$data.id}' value='${id}'>${label}</input><br/>{{/each}}"
        );

ListField.prototype.template = {};
ListField.prototype.template['select'] = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "<select {{if multiple_choice }}multiple='multiple'{{/if}} name='select-${id}' id='${id}'>\n" +
  "{{tmpl($data) 'option-select'}}</select>" +
  "</li>\n");

ListField.prototype.template['radio'] = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "{{tmpl($data) 'option-radio'}}</select>" +
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
}

ListField.prototype.redraw = function () {
  $('#' + this.props.id + '_container').html($(this.render()).html());
  this.addBehaviour();
}

ListField.prototype.addBehaviour = function () {
  var instance = this;
  var labelSelector = '#' + this.props.id + 'Label';

  var instantFeedback = function () {
      setupCopyValue('#EditLabel', labelSelector, 'Question');
      setupCopyValue('#EditDescription', '#' + instance.props.id +
          'Description', null, true);
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
