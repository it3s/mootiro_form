// As the page loads, GET the templates file and compile the templates
$.get('/static/fieldtypes/TextAreaField/textarea.tmpl.html',
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

// Methods

TextAreaField.prototype.save = function() {
  var p = this.props;
  p.width = $('#EditWidth').val();
  p.height = $('#EditHeight').val();
  p.defaul = $('#EditDefault').val();
  p.maxWords = $('#EditMaxWords').val();
  p.minWords = $('#EditMinWords').val();
  p.maxLength = $('#EditMaxLength').val();
  p.minLength = $('#EditMinLength').val();
  p.enableWords = $('#EnableWords').attr('checked');
  p.enableLength = $('#EnableLength').attr('checked');
}

TextAreaField.prototype.instantFeedback = function () {
    setupCopyValue({from: '#EditDefault', to: '#' + this.props.id});
    var instance = this;
    var area = $('textarea', this.domNode)
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
    // Display length options when "Specify length" is clicked
    $('#LengthPropsHandle').click(function () {
      $('#LengthProps').slideToggle();
      toggleText('▶', '▼', '#LengthIcon');
    });
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
  var area = $('textarea', this.domNode)
  area.resizable({minWidth: 204, maxWidth: 504, minHeight: 44, maxHeight: 504,
    resize : function (event, ui) {
      // Show a div on top of the textarea to display the size
      sizeDiv.css('position', 'absolute')
        .position({of: area}).show();
      sizeDiv.text('Width: ' + (ui.size.width - 4) + '. Height: '
        + (ui.size.height - 4));
      // Also update the size values at the left
      $('#EditWidth').val(ui.size.width - 4);
      $('#EditHeight').val(ui.size.height - 4);
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

// Register it
fields.types['TextAreaField'] = TextAreaField;


function toggleText(text1, text2, selector) {
  var current = $(selector).text();
  if (current == text1)
    $(selector).text(text2);
  else
    $(selector).text(text1);
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
