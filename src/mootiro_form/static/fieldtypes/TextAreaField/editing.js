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
  "<ul class='Props'><li><label for='EditDefault'>Default value</label>\n" +
  "<textarea name='defaul' id='EditDefault'>${defaul}</textarea></li></ul>\n");

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
