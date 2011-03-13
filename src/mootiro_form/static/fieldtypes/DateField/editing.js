// Constructor
function DateField(props) {
    this.defaultLabel = 'Date field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id: fieldId.nextString(),
            field_id: 'new',
            type: 'DateField',
            label: this.defaultLabel,
            defaul: '',
            input_date_format: '%Y-%m-%d',
            export_date_format: '%Y-%m-%d',
            description: '',
            required: false,
        };
    }
}

// Fields

DateField.prototype.optionsTemplate = $.template(
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
  "<label for='InputDateFormat'>Input date format</label>\n" +
  "<p id='ErrorInputDateFormat' class='error'></p>\n" +
  "<select name='input_date_format' value='${input_date_format}' id='InputDateFormat'>\n" +
    "<option value='%Y-%m-%d'>2012-01-31</option>\n" +
  "</select>\n" +
"</li><li>\n" +
  "<label for='ExportDateFormat'>Export date format</label>\n" +
  "<p id='ErrorExportDateFormat' class='error'></p>\n" +
  "<select name='export_date_format' value='${export_date_format}' id='ExportDateFormat'>\n" +
    "<option value='%Y-%m-%d'>2012-01-31</option>\n" +
  "</select>\n" +
"</li><li>\n" +
  " <input type='checkbox' id='EditRequired' name='required' />\n" +
  " <label for='EditRequired'>required</label>\n" +
"</li></ul>\n"
);

DateField.prototype.renderOptions = function () {

    var instance = this;
    var optionsDom = $.tmpl(instance.optionsTemplate, instance.props);

    $("#EditDefault", optionsDom).datepicker({ dateFormat: 'yy-mm-dd' });

    return optionsDom;

}

DateField.prototype.previewTemplate = $.template(
  "<input readonly type='text' name='${id}' id='${id}' value='${defaul}' />\n");

// Methods

DateField.prototype.save = function () {
    this.props.defaul = $('#EditDefault').val();
    this.props.input_date_format = $('#InputDateFormat option:selected').val();
    this.props.export_date_format = $('#ExportDateFormat option:selected').val();
}

DateField.prototype.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    return errors;
}

DateField.prototype.showErrors = function () {
    var errors = this.getErrors();
}

DateField.prototype.instantFeedback = function () {
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id});
}

DateField.prototype.addBehaviour = function () {
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
  $('#' + this.props.id, this.domNode).click(funcForOnClickEdit2('#EditDefault'));
};

// Register it
fields.types['DateField'] = DateField;

$('img.DateFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/DateField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/DateField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/DateField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/DateField/iconHover.png'});
});