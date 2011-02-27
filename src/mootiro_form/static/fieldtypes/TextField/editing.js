// Constructor
function TextField(props) {
    if (props) {
        this.props = props;
        this.props.id = fieldId.next();
    } else {
        this.props = {
            id : fieldId.next(),
            field_id : 'new',
            type : 'TextField',
            label : 'Text Field',
            defaul : '',
            required : ''
        };
    }
}

// Fields

TextField.prototype.template = $.template(
  "<li id='${id}_container'><label id='${id}Label' " +
  "for='${id}'>${label}</label>\n" +
  "<input readonly type='text' name='${id}' id='${id}' value='${defaul}' />\n" +
  "</li>\n");

TextField.prototype.optionsTemplate = $.template(
    "<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
    "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
    "<label for='EditLabel'>Label*</label>\n" +
    "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
    "<label for='EditDefault'>Default value</label>\n" +
    "<input type='text' name='defaul' value='${defaul}' id='EditDefault' />\n" +
    "<label for='EditExplain'>Brief explanation</label>\n" +
    "<textarea id='EditExplain' name='explain'></textarea>\n" +
    "<input type='checkbox' id='EditRequired' name='required' />\n" +
    "<label for='EditRequired'>required</label>\n");

// Methods

TextField.prototype.render = function() {
  return $.tmpl(this.template, this.props);
};

TextField.prototype.save = function(field) {
    field.props.label = $('#EditLabel').val();
    field.props.defaul = $('#EditDefault').val();
    if ($('#EditRequired').attr('checked')) {
        field.props.required = true;    
    } else {
        field.props.required = false;    
    }
}

TextField.prototype.insert = function(position) {
  // for now, only insert at the end
  domNode = this.render();
  $.event.trigger('AddField', [this, domNode]);
  var instance = this;
  var labelSelector = '#' + this.props.id + 'Label';

  var instantFeedback = function() {
      setupCopyValue('#EditLabel', labelSelector, 'Question');
      setupCopyValue('#EditDefault', '#' + instance.props.id);
      setupCopyValue('#EditExplain', '#' + instance.props.id + 'Explain',
                     null, true);
  }

  $(labelSelector).click(function() {
      switchToEdit(instance);
      instantFeedback();
      $('#EditLabel').focus();
      return false;
  });

  $('#' + this.props.id).click(function() {
      switchToEdit(instance);
      instantFeedback();
      $('#EditDefault').focus();
      return false;
  });

//  instantFeedback();
};


