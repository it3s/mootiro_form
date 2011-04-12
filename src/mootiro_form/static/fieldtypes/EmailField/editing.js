// Constructor
function EmailField(props) {
    this.defaultLabel = 'Email field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id: fieldId.nextString(),
            field_id: 'new',
            type: 'EmailField',
            label: this.defaultLabel,
            defaul: '',
            description: '',
            required: false,
            minLength: 0,
            maxLength: 255
        };
    }
    this.bottomBasicOptionsTemplate = 'EmailFieldBottomBasicOptions';
    this.advancedOptionsTemplate = 'EmailFieldAdvancedOptions';
    this.previewTemplate = 'EmailFieldPreview';
}

EmailField.prototype.load = function () {
  // As the page loads, GET the templates file and compile the templates
  $.get('/static/fieldtypes/EmailField/email.tmpl.html',
    function (fragment) {
      $('body').append(fragment);
      $.template('EmailFieldBottomBasicOptions', $('#EmailFieldBottomBasicOptions'));
      $.template('EmailFieldAdvancedOptions', $('#EmailFieldAdvancedOptions'));
      $.template('EmailFieldPreview', $('#EmailFieldPreview'));
    }
  );
}

EmailField.prototype.save = function () {
  return textLength.save(this);
}

EmailField.prototype.getErrors = function () {
  return textLength.getErrors();
}

EmailField.prototype.showErrors = function () {
  return textLength.showErrors();
}

EmailField.prototype.instantFeedback = function () {
  return textLength.instantFeedback(this);
}

EmailField.prototype.addBehaviour = function () {
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  $('#' + this.props.id, this.domNode).click(
    funcForOnClickEdit(this, '#EditDefault'));
};

$('img.EmailFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/iconHover.png'});
});
