// Constructor
function TextAreaField(props) {
  this.defaultLabel = 'Text area';
  if (props) {
      this.props = props;
      this.props.id = fieldId.nextString();
  } else {
      this.props = {
          id: fieldId.nextString(),
          type: 'TextAreaField',
          label: this.defaultLabel,
          defaul: '',
          field_id: 'new',
          required: false,
          description: '',
          minLength: 1, maxLength: 800, enableLength: false,
          minWords : 1, maxWords : 400, enableWords : false,
          width: 400, height: 40
      };
  }
  this.optionsTemplate = 'TextAreaOptions';
  this.previewTemplate = 'TextAreaPreview';
}

TextAreaField.prototype.load = function () {
  // As the page loads, GET the templates file and compile the templates
  $.get('/static/fieldtypes/TextAreaField/textarea.tmpl.html',
    function (fragment) {
      $('body').append(fragment);
      $.template('TextAreaOptions', $('#TextAreaOptions'));
      $.template('TextAreaPreview', $('#TextAreaPreview'));
    }
  );
}

// Methods

TextAreaField.prototype.save = function () {
  textLength.save(this);
  var p = this.props;
  p.width = $('#EditWidth').val();
  p.height = $('#EditHeight').val();
}

TextAreaField.prototype.getErrors =  function () {
  return textLength.getErrors();
}

TextAreaField.prototype.showErrors = function () {
  return textLength.showErrors();
}

TextAreaField.prototype.instantFeedback = function () {
  textLength.instantFeedback(this);
  var instance = this;
  var area = $('.TextAreaWrapper', this.domNode);
  // Resize the textarea when user types size at the left
  var handler = function () {
    var val = $(this).val();
    if (val) {
      area.resizable('destroy');
      area.width(val);
      instance.makeResizable();
    }
  }
  $('#EditWidth').keyup(handler).change(handler);
  handler = function () {
    var val = $(this).val();
    area.resizable('destroy');
    area.height(val);
    instance.makeResizable();
  }
  $('#EditHeight').keyup(handler).change(handler);
}

TextAreaField.prototype.addBehaviour = function () {
  this.makeResizable();
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  $('#' + this.props.id, this.domNode).click(
    funcForOnClickEdit(this, '#EditDefault'));
};

TextAreaField.prototype.makeResizable = function () {
  var sizeDiv = $('#' + this.props.id + '_size', this.domNode);
  var instance = this;
  sizeDiv.hide();
  // Make the textarea preview the right size, then make it resizable
  var area = $('.TextAreaWrapper', this.domNode);
  area.resizable({minWidth: 200, maxWidth: 500, minHeight: 40, maxHeight: 500,
    resize : function (event, ui) {
      // Show a div on top of the textarea to display the size
      sizeDiv.css('position', 'absolute').position({of: area}).show();
      sizeDiv.text('Width: ' + (ui.size.width) + '. Height: '
        + (ui.size.height));
      // Also update the size values at the left
      $('#EditWidth').val(ui.size.width);
      $('#EditHeight').val(ui.size.height);
    },
    stop: function (event, ui) {
      sizeDiv.fadeOut(1000);
    },
    start: function (event, ui) {
      sizeDiv.fadeIn(300);
      fields.switchToEdit(instance);
    }
  });
}


$('img.TextAreaFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') +
        '/static/fieldtypes/TextAreaField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') +
        '/static/fieldtypes/TextAreaField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') +
        '/static/fieldtypes/TextAreaField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') +
        '/static/fieldtypes/TextAreaField/iconHover.png'});
});
