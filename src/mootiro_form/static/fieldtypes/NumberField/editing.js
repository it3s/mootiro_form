// Constructor
function NumberField(props) {
    this.defaultLabel = 'Number field';
    if (props) {
        this.props = props;
        // adjusts number exibithion
        if (this.props.precision == 0)
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
            separator: '.'
        };
    }
}

// Fields
NumberField.prototype.optionsTemplate = $.template(
"<ul class='Props'><li>\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<p id='ErrorDefault' class='error'></p>\n" +
  "<input type='text' name='defaul' value='${defaul}' id='EditDefault' />\n" +
"</li><li>\n" +
  // the 'num_type' field is not persisted, it just exists for more user-friendness
  "<label><input type='radio' name='num_type' value='integer' {{if precision == 0}}checked='checked'{{/if}}/>integer</label>" +
  "<label><input type='radio' name='num_type' value='decimal' {{if precision > 0}}checked='checked'{{/if}}/>decimal</label>" +
  "<br/>" +
  "<label id='EditPrecision' for='precision' {{if precision == 0}}style='display: none'{{/if}}>Precision: " +
    "<select name='precision'>" +
      "{{each rangeNum(1, 20)}}" +
        "<option value='${$value}' {{if precision == $value}}selected = 'selected'{{/if}}>${$value}</option>" +
      "{{/each}}" +
    "</select>" +
  "</label>" +
"</li><li>\n" +
  "<label><input type='radio' name='separator' value='.' {{if separator == '.'}}checked='checked'{{/if}}/>dot (.)</label>" +
  "<label><input type='radio' name='separator' value=',' {{if separator == ','}}checked='checked'{{/if}}/>comma (,)</label>" +
"</li>\n" +
"</ul>"
);

NumberField.prototype.previewTemplate = $.template(
  "<input readonly type='text' name='${id}' id='${id}' value='${defaul}' />\n");

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

    var funcForShowingPrecisionList = function () {
      if (this.value == 'integer')
          $("label#EditPrecision").hide();
      if (this.value == 'decimal')
          $("label#EditPrecision").show();
          $("select[name='precision']").val('5');
    };

  $("input[name='num_type']").click(funcForShowingPrecisionList);
}

NumberField.prototype.addBehaviour = function () {
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
fields.types['NumberField'] = NumberField;

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