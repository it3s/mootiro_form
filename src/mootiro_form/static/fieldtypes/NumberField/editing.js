// Constructor
function NumberField(props) {
    this.defaultLabel = 'Number field';
    if (props) {
        this.props = props;
        // adjusts number exibithion
        if (this.props.precision == 0 && this.props.defaul != '')
            this.props.defaul = Math.floor(this.props.defaul);
        else {
            if (this.props.separator == ',')
                this.props.defaul = this.props.defaul.toString().replace(/\./, ',');
        }
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id: fieldId.nextString(),
            field_id: 'new',
            type: 'NumberField',
            label: this.defaultLabel,
            defaul: '',
            description: '',
            required: false,
            precision: 0, // integer by default
            separator: '.',
            prefix: '',
            suffix: ''
        };
    }
    this.optionsTemplate = $.template('NumberOptions');
    this.previewTemplate = $.template('NumberPreview');
}

NumberField.prototype.load = function () {
    // As the page loads, GET the templates file and compile the templates
    $.get('/static/fieldtypes/NumberField/jquery_templates.html',
      function (fragment) {
        $('body').append(fragment);
        //$.template('NumberBasicOptionsBottom', $('#NumberOptions'));
        $.template('NumberOptions', $('#NumberOptions'));
        $.template('NumberPreview', $('#NumberPreview'));
      }
    );
}

// Methods
NumberField.prototype.save = function () {
    this.props.separator = $("input[name='separator']:checked").val();
    
    if (this.props.separator == ',')
        this.props.defaul = $('#EditDefault').val().replace(/\,/, '.');
    else
        this.props.defaul = $('#EditDefault').val();

    if ($("input[name='num_type']:checked").val() == 'integer')
        this.props.precision = 0;
    else
        this.props.precision = $("select[name='precision']").val();

    this.props.prefix = $("#EditPrefix").val();
    this.props.suffix = $("#EditSuffix").val();
}

NumberField.prototype.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    var d = Number($('#EditDefault').val());
    if ($("input[name='num_type']:checked").val() == 'integer')
        errors.defaul = integerValidator($('#EditDefault').val())
    if ($("input[name='num_type']:checked").val() == 'decimal') {
        sep = $("input[name='separator']:checked").val();
        prec = $("select[name='precision']").val();
        errors.defaul = decimalValidator($('#EditDefault').val(), sep, prec)
    }

    return errors;
}

NumberField.prototype.showErrors = function () {
    var errors = this.getErrors();
    $('#ErrorDefault').text(errors.defaul);
}

NumberField.prototype.instantFeedback = function () {
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id,
        obj: this, callback: 'showErrors'});
    var h = methodCaller(this, 'showErrors');
    $("#EditDefault").keyup(h).change(h);
    $("input[name='num_type'], select[name='precision'], input[name='separator']").change(h);

    setupCopyValue({from: '#EditPrefix', to: '#' + this.props.id + '_prefix',
        obj: this});
    setupCopyValue({from: '#EditSuffix', to: '#' + this.props.id + '_suffix',
        obj: this});

    var funcForShowingPrecisionList = function () {
      if (this.value == 'integer')
          $("div#EditPrecision").hide();
      if (this.value == 'decimal')
          $("div#EditPrecision").show();
          $("select[name='precision']").val('2'); // set default precision
    };
    $("input[name='num_type']").click(funcForShowingPrecisionList);
}

NumberField.prototype.addBehaviour = function () {
  var instance = this;
  $('#' + this.props.id, this.domNode).click(funcForOnClickEdit(instance,
    '#EditDefault'));
  $('#' + this.props.id + '_prefix', this.domNode).click(
    funcForOnClickEdit(instance, '#EditPrefix'));
  $('#' + this.props.id + '_suffix', this.domNode).click(
    funcForOnClickEdit(instance, '#EditSuffix'));
};

$('img.NumberFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/NumberField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/NumberField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/NumberField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/NumberField/iconHover.png'});
});

// Auxiliar functions
function rangeNum (s, e) {
    range = new Array();
    for (i = 0, j = s; i <= e-s; i++, j++) {
        range[i] = j;
    }
    return range;
}

function integerValidator(v) {
    v = v.toString(); // exibithion value
    var n = Number(v.replace(',', '.')); // persisted value
    if (isNaN(n))
        return 'Not a number';
    if (v.contains('.') || v.contains(','))
        return 'Not an integer number';
    return '';
}

// Receives a value v and a precision prec for the decimal number
function decimalValidator(v, sep, prec) {
    v = v.toString(); // exibithion value
    var x = Number(v.replace(',', '.')); // persisted value
    if (isNaN(x))
        return 'Not a number';
    if ((sep == '.' && v.match(/\,/)) ||
        (sep == ',' && v.match(/\./)))
        return 'Wrong separator';
    arr = v.split(sep);
    if (arr[1] && arr[1].length > prec)
        return 'Precision overflow';
    return '';
}
