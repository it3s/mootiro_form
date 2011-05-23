// Constructor
function DateField(props) {
    this.defaultLabel = _('Date field');
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
            month_selector: false,
            year_selector: false,
            show_week: false
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
    $("#EditDefault", optionsDom).datepicker({ dateFormat: date_format,
                                               showWeek: true,
                                               changeMonth: true,
                                               changeYear: true
                                             });

    $("#InputDateFormat", optionsDom).change(function () {
        $("#EditDefault", optionsDom).datepicker("option", "dateFormat", field_conf_json['DateField']['date_formats'][this.value]['js']);
        instance.props.input_date_format = this.value;
        instance.props.defaul = $("#EditDefault", optionsDom).val();
        fields.saveCurrent();
        fields.redrawPreview(instance);
    });

    if (instance.props.month_selector) {
       $('#month_selector', optionsDom).attr({checked: true});
    } else {
       $('#month_selector', optionsDom).attr({checked: false});
    }

    if (instance.props.year_selector) {
       $('#year_selector', optionsDom).attr({checked: true});
    } else {
       $('#year_selector', optionsDom).attr({checked: false});
    }

    if (instance.props.show_week) {
       $('#show_week', optionsDom).attr({checked: true});
    } else {
       $('#show_week', optionsDom).attr({checked: false});
    }

    return optionsDom;
}

DateField.prototype.save = function () {
    this.props.defaul = $('#EditDefault').val();
    this.props.input_date_format = $('#InputDateFormat option:selected').val();
    this.props.month_selector = $('#month_selector').attr('checked');
    this.props.year_selector = $('#year_selector').attr('checked');
    this.props.show_week = $('#show_week').attr('checked');
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

DateField.prototype.instantFeedback = function () {
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id,
        obj: this, callback: 'showErrors'});
}

DateField.prototype.addBehaviour = function () {
    // When user clicks on the right side, the Edit tab appears and the
    // corresponding input gets the focus.
    $('#' + this.props.id, this.domNode).click(
        funcForOnClickEdit(this, '#EditDefault'));
};

$('img.DateFieldIcon').hover(function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/DateField/iconHover.png'});
}, function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/DateField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/DateField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/DateField/iconHover.png'});
});
