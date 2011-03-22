// As the page loads, GET the templates file and compile the templates
$.get('/static/fieldtypes/TextAreaField/jquery_templates.html',
  function (fragment) {
    $('body').append(fragment);
    $.template('TextAreaOptions', $('#TextAreaOptions'));
    $.template('TextAreaPreview', $('#TextAreaPreview'));
  }
);

// Constructor
function TextAreaField(props) {
    this.defaultLabel = 'Text area';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'TextAreaField',
            label : this.defaultLabel,
            defaul : '',
            description : '',
            required : false,
            minLength : 1, maxLength: 800, enableLength: false,
            minWords  : 1, maxWords : 400, enableWords : false
        };
    }
    this.optionsTemplate = $.template('TextAreaOptions');
    this.previewTemplate = $.template('TextAreaPreview');
}

// Methods

TextAreaField.prototype.save = function() {
  var p = this.props;
  p.defaul = $('#EditDefault').val();
  p.enableLength = $('#EnableLength').attr('checked');
  p  .minLength = $('#EditMinLength').val();
  p .maxLength = $('#EditMaxLength').val();
  p.enableWords = $('#EnableWords').attr('checked');
  p   .minWords = $('#EditMinWords').val();
  p   .maxWords = $('#EditMaxWords').val();
  if (window.console) console.log(p);
}

TextAreaField.prototype.instantFeedback = function () {
    setupCopyValue({from:'#EditDefault', to:'#' + this.props.id});
}

TextAreaField.prototype.addBehaviour = function () {
  var instance = this;
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  var funcForOnClickEdit2 = function (target, defaul) {
    return function () {
      fields.switchToEdit(instance);
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
fields.types['TextAreaField'] = TextAreaField;


$('img.TextAreaFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') + '/static/fieldtypes/TextAreaField/iconHover.png'});
});
