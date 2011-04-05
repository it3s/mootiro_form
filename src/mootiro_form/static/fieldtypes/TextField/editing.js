// Constructor
function TextField(props) {
    this.defaultLabel = 'Text field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id: fieldId.nextString(),
            field_id: 'new',
            type: 'TextField',
            label: this.defaultLabel,
            defaul: '',
            description: '',
            required: false,
            minLength: 0,
            maxLength: 255
        };
    }
    this.optionsTemplate = 'TextFieldOptions';
    this.previewTemplate = 'TextFieldPreview';
}

TextField.prototype.load = function () {
  // As the page loads, GET the templates file and compile the templates
  $.get('/static/fieldtypes/TextField/text.tmpl.html',
    function (fragment) {
      $('body').append(fragment);
      $.template('TextFieldOptions', $('#TextFieldOptions'));
      $.template('TextFieldPreview', $('#TextFieldPreview'));
    }
  );
}

TextField.prototype.save = function () {
    this.props.defaul = $('#EditDefault').val();
    this.props.minLength = $('#EditMinLength').val();
    this.props.maxLength = $('#EditMaxLength').val();
}

TextField.prototype.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    var min = $('#EditMinLength').val();
    var max = $('#EditMaxLength').val();
    errors.min = positiveIntValidator(min);
    errors.max = positiveIntValidator(max);
    // Only now convert to number, to further validate
    min = Number(min);
    max = Number(max);
    if (!errors.max && min > max) errors.min = 'Higher than max';
    var lendefault = $('#EditDefault').val().length;
    if (lendefault === 0)  return errors;
    if (min > lendefault) errors.defaul = 'Shorter than min length';
    if (max < lendefault) errors.defaul = 'Longer than max length';
    return errors;
}

TextField.prototype.showErrors = function () {
    var errors = this.getErrors();
    $('#ErrorDefault')  .text(errors.defaul);
    $('#ErrorMinLength').text(errors.min);
    $('#ErrorMaxLength').text(errors.max);
}

TextField.prototype.instantFeedback = function () {
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id,
        obj: this, callback: 'showErrors'});
    var h = methodCaller(this, 'showErrors');
    $('#EditMinLength').keyup(h).change(h);
    $('#EditMaxLength').keyup(h).change(h);
}

TextField.prototype.addBehaviour = function () {
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

$('img.TextFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextField/iconHover.png'});
});
