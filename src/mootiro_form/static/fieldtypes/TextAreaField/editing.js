// Constructor
function TextAreaField(props) {
    this.defaultLabel = 'Text area';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'TextAreaField',
            label : this.defaultLabel,
            defaul : '',
            description : '',
            required : ''
        };
    }
}

// Fields

TextAreaField.prototype.optionsTemplate = $.template(
  "<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
  "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<textarea name='defaul' id='EditDefault'>${defaul}</textarea>\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
  "<input type='checkbox' id='EditRequired' name='required' />\n" +
  "<label for='EditRequired'>required</label>\n");

TextAreaField.prototype.template = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "<textarea readonly name='${id}' id='${id}'>${defaul}</textarea>\n" +
  "</li>\n");

// Methods
// TextField.prototype.render = function() {

TextField.prototype.save = function() {
    this.props.defaul = $('#EditDefault').val();
}

TextAreaField.prototype.addBehaviour = function () {
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
fields.types['TextAreaField'] = TextAreaField;
