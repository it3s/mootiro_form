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
  return textLength.getErrors();
}

TextField.prototype.showErrors = function () {
  return textLength.showErrors();
}

TextField.prototype.instantFeedback = function () {
  return textLength.instantFeedback(this);
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
