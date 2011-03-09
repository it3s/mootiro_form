// Constructor
function TextField(props) {
    this.defaultLabel = 'Text field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id: fieldId.nextString(),
            field_id: 'new',
            type: 'TextField',
            label: this.defaultLabel,
            defaul: '',
            description: '',
            required: false,
            minLength: 0,
            maxLength: 255
        };
    }
}

// Fields

TextField.prototype.optionsTemplate = $.template(
"<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
"<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
"<ul class='Props'><li>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
"</li><li>\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<p id='ErrorDefault' class='error'></p>\n" +
  "<input type='text' name='defaul' value='${defaul}' id='EditDefault' />\n" +
"</li><li>\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
"</li><li>\n" +
  " <input type='checkbox' id='EditRequired' name='required' />\n" +
  " <label for='EditRequired'>required</label>\n" +
"</li><li>\n" +
  "<table id='EditLength' style='width:99%;'><tr>\n" +
  "<td style='vertical-align: top;'><label class='desc'>Length:</label>\n" +
  "</td><td>&nbsp;</td>\n" +
  "<td><label for='EditMinLength'>Min</label>\n" +
  "<p id='ErrorMinLength' class='error'></p>\n" +
  "<input type='text' name='min' id='EditMinLength' value='${minLength}' " +
  "size='6' title='Minimum length, in characters' /></td><td>&nbsp;</td>\n" +
  "<td><label for='EditMaxLength'>Max</label>\n" +
  "<p id='ErrorMaxLength' class='error'></p>\n" +
  "<input type='text' name='max' id='EditMaxLength' value='${maxLength}' " +
  "size='6' title='Maximum length, in characters' /></td>" +
  "</tr></table>" +
"</li></ul>\n"
);

TextField.prototype.template = $.template(
  "<li id='${id}_container'><div style='float: left;'>\n" +
  "<label id='${id}Label' class='desc' for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description NewLines' id='${id}Description'>${description}</div>\n" +
  "<input readonly type='text' name='${id}' id='${id}' value='${defaul}' /></div>\n" +
  "<div class='fieldButtons'/><div style='clear:both;'/></li>\n");

// Methods
// TextField.prototype.renderPreview = function() {

TextField.prototype.save = function () {
    this.props.defaul = $('#EditDefault').val();
    this.props.minLength = $('#EditMinLength').val();
    this.props.maxLength = $('#EditMaxLength').val();
}

TextField.prototype.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    var min = Number($('#EditMinLength').val());
    var max = Number($('#EditMaxLength').val());
    errors.min = positiveIntValidator(min);
    errors.max = positiveIntValidator(max);
    if (!errors.max && min > max) errors.min = 'Higher than max';
    var lendefault = $('#EditDefault').val().length;
    if (lendefault === 0)  return errors;
    if (min > lendefault) errors.defaul = 'Shorter than min length';
    if (max < lendefault) errors.defaul = 'Longer than max length';
    return errors;
}

TextField.prototype.showErrors = function () {
    var errors = this.getErrors();
    $('#ErrorDefault')  .text(errors.defaul);
    $('#ErrorMinLength').text(errors.min);
    $('#ErrorMaxLength').text(errors.max);
}

TextField.prototype.instantFeedback = function () {
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id,
        obj: this, callback: 'showErrors'});
    var h = methodCaller(this, 'showErrors');
    $('#EditMinLength').keyup(h).change(h);
    $('#EditMaxLength').keyup(h).change(h);
}

TextField.prototype.addBehaviour = function () {
  var instance = this;
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  var funcForOnClickEdit2 = function (target, defaul) {
    return function () {
      if (!fields.switchToEdit(instance))  return false;
      fields.instantFeedback();
      $(target).focus();
      // Sometimes also select the text. (If it is the default value.)
      if ($(target).val() === defaul) $(target).select();
      return false;
    };
  };
  $('#' + this.props.id).click(funcForOnClickEdit2('#EditDefault'));
};

// Register it
fields.types['TextField'] = TextField;

$('img.TextFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/iconHover.png'});
});
