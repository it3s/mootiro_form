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
// TextField.prototype.render = function() {

TextField.prototype.save = function() {
    this.props.defaul = $('#EditDefault').val();
}

TextField.prototype.addBehaviour = function () {
  var instance = this;
  // Overload form_edit.js' instantFeedback()
  var instantFeedback = function () {
      setupCopyValue('#EditDefault', '#' + instance.props.id);
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
  $('#' + this.props.id).click(funcForOnClickEdit('#EditDefault'));
};

// Register it
fields.types['TextField'] = TextField;
