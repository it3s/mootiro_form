// Constructor
function ListField(props) {
    this.defaultLabel = 'List field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'ListField',
            label : this.defaultLabel,
            defaul : '',
            description : '',
            required : '',
            list_type : 'select',
            options: [{id:'new', label:'option 1', value:''}]
        };
    }
}

ListField.prototype.render = function () {
    return $.tmpl(this.template[this.props.list_type], this.props);
}

ListField.prototype.renderOptions = function () {
    var instance = this;
    domOptions = $.tmpl(this.optionsTemplate, this.props);
    $('input[name="optionLabel"]', domOptions).each(function (idx, ele) {
      ele.opt_id = instance.props.options[idx].id;  
    });
    $('#addOption', domOptions).click(function () {
       var newOptionDom = $("<input type='text' name='optionLabel' value=''/>");
       var newOption = {id:'new', label:'', value:''};
       instance.props.options.push(newOption);
       newOptionDom.opt_id = 'new';
       $('#listOptions').append(newOptionDom);  
    });
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
  "<div id='listOptions'><b>List options</b><p/>{{tmpl($data) 'options-edit'}}\n" +
  "</div><span id='addOption' style='float:right;'><img alt='Add option' title='Add option' src='" + route_url('root') + "/static/img/icons-edit/move_large.png'/></span></div>"
  );

ListField.prototype.optionsEditTemplate = $.template("options-edit",
  "{{each options}}<input type='text' name='optionLabel' value='${label}'/>{{/each}}\n"
        );

ListField.prototype.option_template = {};
ListField.prototype.option_template['select'] = $.template("option-select",
        "{{each options}}<option value='${id}'>${label}</option>{{/each}}"
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
  "<select name='select-${id}' id='${id}'>\n" +
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

ListField.prototype.save = function() {
  var instance = this;
  // Copies to props the information in the left form
  this.props.label = $('#EditLabel').val();
  this.props.defaul = '';
  this.props.list_type = $('#listType option:selected').val();
  this.props.required = $('#EditRequired').attr('checked');
  this.props.description = $('#EditDescription').val();
  $('input[name="optionLabel"]').each(function (idx, ele) {
    instance.props.options[idx].label = $(this).val();
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
