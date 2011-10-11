// Constructor
function ImageField(props) {
    this.defaultLabel = _('Image field');
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = mergeNewFieldProps({
            type: 'ImageField',
            label: this.defaultLabel,
            showPlaceholder: true,
            width:240, height:320,
            mimeTypes: {".jpg, .jpeg": true,
                        ".png": true,
                        ".gif": true,
                        ".bmp": true}
        });
    }
    this.bottomBasicOptionsTemplate = 'ImageFieldBottomBasicOptions';
    this.advancedOptionsTemplate = 'ImageFieldAdvancedOptions';
    this.previewTemplate = 'ImageFieldPreview';
}

ImageField.prototype.load = function () {
  // As the page loads, GET the templates file and compile the templates
  $.get('/static/fieldtypes/ImageField/image.tmpl.html',
    function (fragment) {
      $('body').append(fragment);
      $.template('ImageFieldBottomBasicOptions',
                 $('#ImageFieldBottomBasicOptions'));
      $.template('ImageFieldAdvancedOptions',
                 $('#ImageFieldAdvancedOptions'));
      $.template('ImageFieldPreview', $('#ImageFieldPreview'));
    }
  );
}

ImageField.prototype.save = function () {
  var p = this.props;
  p.mimeTypes = {};
  var handler = function (index) {
    p.mimeTypes[$(this).val()] = true;
  }

  $('input[name=EditMimetype]:checked').each(handler);
  p.showPlaceholder = $('#EditPlaceholder').attr('checked');
  p.width = $('#EditWidth').val();
  p.height = $('#EditHeight').val();
}

ImageField.prototype.getErrors = function () {
  var errors = {defaul: '',
                width: '',
                height: '',
                mimeTypes: ''};
  var width = $('#EditWidth').val();
  var height = $('#EditHeight').val();
  var limits = this.getSizeLimits();
  if (!errors.width) {
    if (width < limits.minWidth)  errors.width = _('Too small.');
    if (width > limits.maxWidth)  errors.width = _('Too big.');
  }
  if (!errors.height) {
    if (height < limits.minHeight)  errors.height = _('Too small.');
    if (height > limits.maxHeight)  errors.height = _('Too big.');
  }
  var n_mimeTypes = $('input[name=EditMimetype]:checked').length;
  if (!errors.MimeTypes) {
    if (n_mimeTypes == 0)  errors.mimeTypes = _('You must select at least one file type');
  }
  return errors;
}

ImageField.prototype.showErrors = function () {
  var errors = this.getErrors();
  $('#ErrorEditWidth').text(errors.width);
  $('#ErrorEditHeight').text(errors.height);
  $('#ErrorMimeTypes').text(errors.mimeTypes);
}

ImageField.prototype.instantFeedback = function () {
  var instance = this;
  var area = $('.ImageFieldWrapper', this.domNode);
  // Resize the textarea when user types size at the left
  var handler = function () {
    instance.showErrors();
    var val = $(this).val();
    if (val) {
      area.resizable('destroy');
      area.width(val);
      instance.makeResizable();
    }
  }
  $('#EditWidth').keyup(handler).change(handler);
  var handler = function () {
    instance.showErrors();
    var val = $(this).val();
    if (val) {
      area.resizable('destroy');
      area.height(val);
      instance.makeResizable();
    }
  }
  $('#EditHeight').keyup(handler).change(handler);
  var handler = function () {
    instance.showErrors();
    var checked = $(this).attr('checked');
    if (checked) {
      area.show();
    } else {
      area.hide();
    }
  }
  $('#EditPlaceholder').change(handler);
  var handler = function () {
    instance.showErrors();
    var checked = $(this).attr('checked');
    if (checked) {
      $('input[name=EditMimetype]').attr('checked', true)
    }
  }
  $('#EditMimetype-all').change(handler);
  var handler = function () {
    instance.showErrors();
    var checked = $(this).attr('checked');
    if (!checked) {
      $('#EditMimetype-all').attr('checked', false)
    }
  }
  $('input[name=EditMimetype]').change(handler);
}

ImageField.prototype.addBehaviour = function () {
  this.makeResizable();
  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  $('#' + this.props.id, this.domNode).click(
    funcForOnClickEdit(this, '#EditDefault'));
};

function imageValidator(image) {
  return "";
}

ImageField.prototype.getSizeLimits = function () {
    return {minWidth: 50, maxWidth: 640, minHeight: 50, maxHeight: 640};
}

ImageField.prototype.makeResizable = function () {
    var sizeDiv = $('#' + this.props.id + '_size', this.domNode);
    var instance = this;
    sizeDiv.hide();
    // Make the textarea preview the right size, then make it resizable
    var $area = $('.ImageFieldWrapper', this.domNode);
    var args = this.getSizeLimits();
    args.resize = function (e, ui) {
        dirt.onAlteration(e);
        // Show a div on top of the textarea to display the size
        sizeDiv.css('position', 'absolute').position({of: $area}).show();
        sizeDiv.text(_('width: [0], height: [1]').interpol(ui.size.width,
            ui.size.height));
        // Also update the size values at the left
        $('#EditWidth').val(ui.size.width);
        $('#EditHeight').val(ui.size.height);
        instance.showErrors();
    };
    args.stop = function (event, ui) {
        sizeDiv.fadeOut(1000);
    };
    args.start = function (event, ui) {
        sizeDiv.fadeIn(300);
        fields.switchToEdit(instance);
    };
    $area.resizable(args);
}



$('img.ImageFieldIcon').hover(function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ImageField/iconHover.png'});
}, function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ImageField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ImageField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: jurl('__static') +
        '/fieldtypes/ImageField/iconHover.png'});
});
