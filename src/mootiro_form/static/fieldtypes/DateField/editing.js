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
            input_date_format: 0,
            export_date_format: 0,
            description: '',
            required: false,
        };
    }
    this.bottomBasicOptionsTemplate = 'DateBottomBasicOptions';
    this.advancedOptionsTemplate = 'DateAdvancedOptions';
    this.previewTemplate = 'DatePreview';
}

DateField.prototype.load = function () {
  $.get('/static/fieldtypes/DateField/templates/_date.tmpl.html',
    function (template) {
      $('body').append(template);
      $.template('DateBottomBasicOptions', $('#DateBottomBasicOptions'));
      $.template('DateAdvancedOptions', $('#DateAdvancedOptions'));
      $.template('DatePreview', $('#DatePreview'));
   });
}

// Methods
DateField.prototype.renderOptions = function () {
    var instance = this;

    var tplContext = {props: this.props,
        BottomBasicOptionsTpl: this.bottomBasicOptionsTemplate,
        AdvancedOptionsTpl: this.advancedOptionsTemplate};
    var optionsDom = $.tmpl('optionsBase', tplContext);
    var date_format = '';

    date_format = field_conf_json['DateField']['date_formats'][instance.props.input_date_format]['js'];
    $("#EditDefault", optionsDom).datepicker({ dateFormat: date_format });

    $("#InputDateFormat", optionsDom).change(function () {
        // var old_date_format = instance.props.input_date_format;
        old_date_format = field_conf_json['DateField']['date_formats'][instance.props.input_date_format]['js'];
        // var new_date_format = convertDateFormat(this.value);
        $("#EditDefault", optionsDom).dateFormat = field_conf_json['DateField']['date_formats'][this.value]['js'];
        instance.props.input_date_format = this.value;
        var date = $.datepicker.parseDate(old_date_format, $("#EditDefault", optionsDom).val());
        var new_date = $.datepicker.formatDate(field_conf_json['DateField']['date_formats'][instance.props.input_date_format]['js'], date);
        instance.props.defaul = new_date;
        $("#EditDefault", optionsDom).val(new_date);
        fields.saveCurrent();
        fields.redrawPreview(instance);
    });
    return optionsDom;
}

DateField.prototype.save = function () {
    this.props.defaul = $('#EditDefault').val();
    this.props.input_date_format = $('#InputDateFormat option:selected').val();

    // The behaviour below is temporary.
    // It's waiting for csv export configuration page (Feature #621)
    this.props.export_date_format = this.props.input_date_format;
}

DateField.prototype.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    return errors;
}

DateField.prototype.showErrors = function () {
    var errors = this.getErrors();
    // TODO Edgar SENTA PROGRAMA!!!
}

$('img.DateFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + 'static/fieldtypes/DateField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + 'static/fieldtypes/DateField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + 'static/fieldtypes/DateField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + 'static/fieldtypes/DateField/iconHover.png'});
});
