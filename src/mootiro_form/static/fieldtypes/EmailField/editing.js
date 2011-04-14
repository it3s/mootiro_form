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
        };
    }
    this.bottomBasicOptionsTemplate = 'EmailFieldBottomBasicOptions';
    this.previewTemplate = 'EmailFieldPreview';
}

EmailField.prototype.load = function () {
  // As the page loads, GET the templates file and compile the templates
  $.get('/static/fieldtypes/EmailField/email.tmpl.html',
    function (fragment) {
      $('body').append(fragment);
      $.template('EmailFieldBottomBasicOptions', $('#EmailFieldBottomBasicOptions'));
      $.template('EmailFieldPreview', $('#EmailFieldPreview'));
    }
  );
}

EmailField.prototype.save = function () {
  this.props.defaul = $('#EditDefault').val();
}

EmailField.prototype.getErrors = function () {
  errors = {defaul: ''};
  var mail = $('#EditDefault').val();
  if (mail) {
  errors.defaul = emailValidator(mail);
  }
  return errors;
}

EmailField.prototype.showErrors = function () {
  var errors = this.getErrors();
  $('#ErrorDefault').text(errors.defaul);
}

EmailField.prototype.instantFeedback = function () {
  setupCopyValue({from: '#EditDefault', to: '#' + this.props.id,
      obj: this, callback: 'showErrors'});
  var h = methodCaller(this, 'showErrors');
  $("#EditDefault").keyup(h).change(h);
}

EmailField.prototype.addBehaviour = function () {
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  $('#' + this.props.id, this.domNode).click(
    funcForOnClickEdit(this, '#EditDefault'));
};

function emailValidator(mail) {
  filter = /^[+a-zA-Z0-9_.-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]{2,6}$/;
  //var atpos=mail.indexOf("@");
  //if (atpos !=-1 && atpos<1) {
  //  return "The 'local' part of local@domain is missing"
  //}
  if (filter.test(mail)) {
      return "";
  }
  else {
    return "Please enter a valid email address of the format: local@domain"
  }
}


$('img.EmailFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/EmailField/iconHover.png'});
});
