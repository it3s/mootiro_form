// Constructor
function NumberField(props) {
    this.defaultLabel = 'Number field';
    if (props) {
        this.props = props;
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
"<form id='Jonas'>" +
"<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
"<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
"<ul class='Props'><li>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<textarea id='EditLabel' name='label'>${label}</textarea> \n" +
"</li><li>\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<p id='ErrorDefault' class='error'>instant error</p>\n" +
  "<input type='text' name='defaul' value='${defaul}' id='EditDefault' />\n" +
"</li><li>\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
"</li><li>\n" +
  " <input type='checkbox' id='EditRequired' name='required' />\n" +
  " <label for='EditRequired'>required</label>\n" +
"</li><li>\n" +
  // the 'num_type' field is not persisted, it just exists for more user-friendness
  "<label><input id='num_type_integer' type='radio' name='num_type' value='integer' {{if precision == 0}}checked='checked'{{/if}}/>integer</label>" +
  "<label><input id='num_type_float' type='radio' name='num_type' value='float' {{if precision > 0}}checked='checked'{{/if}}/>float</label>" +
  "<br/>" +
  "<label id='EditPrecision' for='precision' {{if precision == 0}}style='display: none'{{/if}}>Precision: " +
    "<select name='precision'>" +
      "{{each rangeNum(1, 20)}}<option value='${$value}' {{if precision == $value}}selected = 'selected'{{/if}}>${$value}</option>{{/each}}" +
    "</select>" +
  "</label>" +
"</li><li>\n" +
  "<label><input id='EditSeparator' type='radio' name='separator' value='.' {{if separator == '.'}}checked='checked'{{/if}}/>dot (.)</label>" +
  "<label><input id='EditSeparator' type='radio' name='separator' value=',' {{if separator == ','}}checked='checked'{{/if}}/>comma (,)</label>" +
"</li></ul>\n" +
"</form>"
);

NumberField.prototype.previewTemplate = $.template(
  "<input readonly type='text' name='${id}' id='${id}' value='${defaul}' />\n");

// Methods

NumberField.prototype.save = function () {
    this.props.defaul = $('#EditDefault').val();
    this.props.separator = $('#EditSeparator').val();

    if ($("input[name='num_type']:checked").val() == 'integer')
        this.props.precision = 0;
    else
        this.props.precision = $('#EditPrecision').val();
}

NumberField.prototype.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    var d = Number($('#EditDefault').val());
    if ($("input[name='num_type']:checked").val() == 'integer')
        errors.defaul = integerValidator($('#EditDefault').val())
    if ($("input[name='num_type']:checked").val() == 'float') {
        prec = $('#EditPrecision select').val();
        errors.defaul = floatValidator($('#EditDefault').val(), prec)
    }

    return errors;
}

NumberField.prototype.showErrors = function () {
    //alert("showErrors")
    var errors = this.getErrors();
    $('#ErrorDefault').text(errors.defaul);
}

NumberField.prototype.instantFeedback = function () {
    /*
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id,
        obj: this, callback: 'showErrors'});
    var h = methodCaller(this, 'showErrors');
    $('#EditMinLength').keyup(h).change(h);
    $('#EditMaxLength').keyup(h).change(h);
    */
    var h = methodCaller(this, 'showErrors');
    $("#EditDefault").keyup(h).change(h);
    $("#num_type_integer, #num_type_float, #EditPrecision select").change(h);
    
    var funcForShowingPrecisionList = function () {
      if (this.value == 'integer')
          $("#EditPrecision").hide();
      if (this.value == 'float')
          $("#EditPrecision").show();
    };

  $("#num_type_float").click(funcForShowingPrecisionList);
  $("#num_type_integer").click(funcForShowingPrecisionList);
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
    if (typeof(s) === 'number') v = v.toString();
    var n = Number(v);
    if (isNaN(n))
        return 'Not a number';
    if (v.contains('.') || v.contains(','))
        return 'Not an integer number';
    return '';
}

// Receives a value v and a precision prec for the float number
function floatValidator(v, prec) {
    if (typeof(s) === 'number') v = v.toString();
    var x = Number(v);
    if (isNaN(x))
        return 'Not a number';
    if (v.split('.')[1].length > prec)
        return 'Precision overflow';
    return '';
}