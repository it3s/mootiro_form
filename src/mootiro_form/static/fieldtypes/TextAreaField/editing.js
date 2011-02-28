// Constructor
function TextAreaField(props) {
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'TextAreaField',
            label : 'Text Area',
            defaul : '',
            required : ''
        };
    }
}

// Fields

TextAreaField.prototype.template = $.template(
  "<li id='${id}_container'><label id='${id}Label' " +
  "for='${id}'>${label}</label>\n" +
  "<textarea readonly name='${id}' id='${id}' value='${defaul}' />\n" +
  "</li>\n");

TextAreaField.prototype.optionsTemplate = $.template(
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

TextAreaField.prototype.render = function() {
  return $.tmpl(this.template, this.props);
};

TextAreaField.prototype.save = function(field) {
  // Copies to props the information in the left form
  field.props.label = $('#EditLabel').val();
  field.props.defaul = $('#EditDefault').val();
  field.props.required = $('#EditRequired').attr('checked');
  field.props.description = $('#EditDescription').val();
}

TextAreaField.prototype.insert = function(position) {
  // for now, only insert at the end
  domNode = this.render();
  $.event.trigger('AddField', [this, domNode]);
  var instance = this;
  var labelSelector = '#' + this.props.id + 'Label';

  var instantFeedback = function () {
      setupCopyValue('#EditLabel', labelSelector, 'Question');
      setupCopyValue('#EditDefault', '#' + instance.props.id);
      setupCopyValue('#EditDescription', '#' + instance.props.id +
          'Description', null, true);
      $('#EditRequired').change(function (e){
        var origin = $('#EditRequired');
        var dest = $('#' + instance.props.id + 'Required');
        if (origin.attr('checked'))
            dest.html('*');
        else
            dest.html('');
      });
  }

  $(labelSelector).click(function () {
      switchToEdit(instance);
      instantFeedback();
      $('#EditLabel').focus();
      return false;
  });

  $('#' + this.props.id).click(function () {
      switchToEdit(instance);
      instantFeedback();
      $('#EditDefault').focus();
      return false;
  });
};
