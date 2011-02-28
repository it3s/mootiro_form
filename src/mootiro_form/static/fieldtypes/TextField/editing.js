// Constructor
function TextField(props) {
    this.defaultLabel = 'Text field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'TextField',
            label : this.defaultLabel,
            defaul : '',
            description : '',
            required : ''
        };
    }
}

// Fields

TextField.prototype.optionsTemplate = $.template(
  "<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
  "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<input type='text' name='defaul' value='${defaul}' id='EditDefault' />\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
  "<input type='checkbox' id='EditRequired' name='required' />\n" +
  "<label for='EditRequired'>required</label>\n");

TextField.prototype.template = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "<input readonly type='text' name='${id}' id='${id}' value='${defaul}' />\n" +
  "</li>\n");

// Methods

TextField.prototype.render = function() {
  return $.tmpl(this.template, this.props);
};

TextField.prototype.save = function(field) {
  // Copies to props the information in the left form
  field.props.label = $('#EditLabel').val();
  field.props.defaul = $('#EditDefault').val();
  field.props.required = $('#EditRequired').attr('checked');
  field.props.description = $('#EditDescription').val();
}

TextField.prototype.insert = function (position) {
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

  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  var funcForOnClickEdit = function (target) {
    return function () {
      switchToEdit(instance);
      instantFeedback();
      $(target).focus();
      return false;
    };
  };
  $(labelSelector).click(funcForOnClickEdit('#EditLabel'));
  $('#' + this.props.id).click(funcForOnClickEdit('#EditDefault'));
  $('#' + this.props.id + 'Description')
    .click(funcForOnClickEdit('#EditDescription'));
};
