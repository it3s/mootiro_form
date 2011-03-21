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
            required : false
        };
    }
}

// Fields

TextAreaField.prototype.optionsTemplate = $.template(
"<ul class='Props'><li>\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<textarea name='defaul' id='EditDefault'>${defaul}</textarea>\n" +
"</li><li>\n" +
  "<table id='EditChars' style='width:99%;'><tr>\n" +
  "<td style='vertical-align: top; width: 40%;'>\n" +
  "<input type='checkbox' name='enableLength' id='enableLength' />&nbsp;" +
  "<label for='enableLength' class='desc'>Characters</label>\n" +
  "</td><td>&nbsp;</td>\n" +
  "<td><label for='EditMinLength'>Min</label>\n" +
  "<p id='ErrorMinLength' class='error'></p>\n" +
  "<input type='text' name='min' id='EditMinLength' value='${minLength}' " +
  "size='5' title='Minimum length, in characters' /></td><td>&nbsp;</td>\n" +
  "<td><label for='EditMaxLength'>Max</label>\n" +
  "<p id='ErrorMaxLength' class='error'></p>\n" +
  "<input type='text' name='max' id='EditMaxLength' value='${maxLength}' " +
  "size='5' title='Maximum length, in characters' /></td>" +
  "</tr></table>" +
"</li><li>\n" +
  "<table id='EditWords' style='width:99%;'><tr>\n" +
  "<td style='vertical-align: top; width: 40%;'>\n" +
  "<input type='checkbox' name='enableWords' id='enableWords' />\n" +
  "<label for='enableWords' class='desc'>Words</label>\n" +
  "</td><td>&nbsp;</td>\n" +
  "<td><label for='EditMinWords'>Min</label>\n" +
  "<p id='ErrorMinWords' class='error'></p>\n" +
  "<input type='text' name='min' id='EditMinWords' value='${minWords}' " +
  "size='5' title='Minimum length, in words' /></td><td>&nbsp;</td>\n" +
  "<td><label for='EditMaxWords'>Max</label>\n" +
  "<p id='ErrorMaxWords' class='error'></p>\n" +
  "<input type='text' name='max' id='EditMaxWords' value='${maxWords}' " +
  "size='5' title='Maximum length, in words' /></td>" +
  "</tr></table>" +
"</li></ul>\n");

TextAreaField.prototype.previewTemplate = $.template(
  "<textarea readonly name='${id}' id='${id}'>${defaul}</textarea>\n");

// Methods

TextAreaField.prototype.save = function() {
    this.props.defaul = $('#EditDefault').val();
}

TextAreaField.prototype.instantFeedback = function () {
    setupCopyValue({from:'#EditDefault', to:'#' + this.props.id});
}

TextAreaField.prototype.addBehaviour = function () {
  var instance = this;
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  var funcForOnClickEdit2 = function (target, defaul) {
    return function () {
      fields.switchToEdit(instance);
      fields.instantFeedback();
      $(target).focus();
      // Sometimes also select the text. (If it is the default value.)
      if ($(target).val() === defaul) $(target).select();
      return false;
    };
  };
  $('#' + this.props.id, this.domNode).click(funcForOnClickEdit2('#EditDefault'));
};

// Register it
fields.types['TextAreaField'] = TextAreaField;

$('img.TextAreaFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/iconHover.png'});
});
