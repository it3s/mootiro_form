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
  "<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
  "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
  "<ul class='Props'><li>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
  "</li><li>\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<textarea name='defaul' id='EditDefault'>${defaul}</textarea>\n" +
  "</li><li>\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
  "</li><li>\n" +
  "<input type='checkbox' id='EditRequired' name='required' />\n" +
  "<label for='EditRequired'>required</label>\n" +
  "</li></ul>\n");

TextAreaField.prototype.template = $.template(
  "<li id='${id}_container'><div style='float:left;'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description NewLines' id='${id}Description'>${description}</div>\n" +
  "<textarea readonly name='${id}' id='${id}'>${defaul}</textarea></div>\n" +
  "<div class='fieldButtons'/><div style='clear:both;'/></li>\n");

// Methods
// TextAreaField.prototype.renderPreview = function() {

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
  $('#' + this.props.id).click(funcForOnClickEdit2('#EditDefault'));
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
