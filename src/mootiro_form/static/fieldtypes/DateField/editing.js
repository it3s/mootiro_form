if (!$('#dateOptions').data('tmpl')) {
    $.get('/static/fieldtypes/DateField/templates/_date.tmpl.html',
      function (template) {
        $('body').append(template);
        $.template('datePreview', $('#datePreview'));
        $.template('dateOptions', $('#dateOptions'));
    });
}

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
DateField.prototype.previewTemplate = 'datePreview';


// Methods

DateField.prototype.renderOptions = function () {
    var instance = this;

    var tplContext = {props: this.props, optionsTpl: 'dateOptions'};
    var optionsDom = $.tmpl('optionsBase', tplContext);
    var date_format = '';

    convertDateFormat = function (date) {
        var date_format = '';
    
        switch (date) {
            case '%Y/%m/%d':
                date_format = 'yy/mm/dd';
                break;
            case '%d-%m-%Y':
                date_format = 'dd-mm-yy';
                break;
            case '%d/%m/%Y':
                date_format = 'dd/mm/yy';
                break;
            default:
                date_format = 'yy-mm-dd';
                break;
        }
        return date_format;
    }

    date_format = convertDateFormat(instance.props.input_date_format);
    $("#EditDefault", optionsDom).datepicker({ dateFormat: date_format });

    $("#InputDateFormat", optionsDom).change(function () {
        var old_date_format = instance.props.input_date_format;
        old_date_format = convertDateFormat(old_date_format);
        var new_date_format = convertDateFormat(this.value);
        $("#EditDefault", optionsDom).dateFormat = new_date_format;
        instance.props.input_date_format = this.value;
        var date = $.datepicker.parseDate(old_date_format,
            $("#EditDefault", optionsDom).val());
        var new_date = $.datepicker.formatDate(new_date_format, date);
        instance.props.defaul = new_date;
        $("#EditDefault", optionsDom).val(new_date);
        fields.redrawPreview(instance);
    });
    return optionsDom;
}

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
    // TODO Edgar SENTA PROGRAMA!!!
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
