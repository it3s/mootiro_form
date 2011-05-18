function TextAreaField(props) {  // Constructor
    this.defaultLabel = _('Text area');
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id: fieldId.nextString(),
            field_id: 'new',
            type: 'TextAreaField',
            label: this.defaultLabel,
            defaul: '',
            description: '',
            required: false,
            minLength: 1, maxLength: 800, enableLength: false,
            minWords : 1, maxWords : 400, enableWords : false,
            width: 400, height: 80
        };
    }
    this.bottomBasicOptionsTemplate = 'TextAreaBottomBasicOptions';
    this.advancedOptionsTemplate = 'TextAreaAdvancedOptions';
    this.previewTemplate = 'TextAreaPreview';
}

TextAreaField.prototype.load = function () {
    // As the page loads, GET the templates file and compile the templates
    $.get('/static/fieldtypes/TextAreaField/textarea.tmpl.html',
        function (fragment) {
            $('body').append(fragment);
            $.template('TextAreaBottomBasicOptions',
                $('#TextAreaBottomBasicOptions'));
            $.template('TextAreaAdvancedOptions',
                $('#TextAreaAdvancedOptions'));
            $.template('TextAreaPreview', $('#TextAreaPreview'));
        }
    );
}

TextAreaField.prototype.save = function () {
    textLength.save(this);
    var p = this.props;
    p.width = $('#EditWidth').val();
    p.height = $('#EditHeight').val();
}

TextAreaField.prototype.getErrors =  function () {
    var errors = textLength.getErrors();
    var width = $('#EditWidth').val();
    var height = $('#EditHeight').val();
    errors.width = positiveIntValidator(width);
    errors.height = positiveIntValidator(height);
    width = Number(width);
    height = Number(height);
    var limits = this.getSizeLimits();
    if (!errors.width) {
        if (width < limits.minWidth)  errors.width = _('Too narrow');
        if (width > limits.maxWidth)  errors.width = _('Too wide');
    }
    if (!errors.height) {
        if (height < limits.minHeight)  errors.height = _('Too short');
        if (height > limits.maxHeight)  errors.height = _('Too tall');
    }
    return errors;
}

TextAreaField.prototype.showErrors = function () {
    var errors = this.getErrors();
    textLength.showErrors(errors);
    $('#ErrorEditWidth').text(errors.width);
    $('#ErrorEditHeight').text(errors.height);
}

TextAreaField.prototype.instantFeedback = function () {
    textLength.instantFeedback(this);
    var instance = this;
    var area = $('.TextAreaWrapper', this.domNode);
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
    handler = function () {
        instance.showErrors();
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

TextAreaField.prototype.getSizeLimits = function () {
    return {minWidth: 200, maxWidth: 500, minHeight: 40, maxHeight: 500};
}

TextAreaField.prototype.makeResizable = function () {
    var sizeDiv = $('#' + this.props.id + '_size', this.domNode);
    var instance = this;
    sizeDiv.hide();
    // Make the textarea preview the right size, then make it resizable
    var $area = $('.TextAreaWrapper', this.domNode);
    var args = this.getSizeLimits();
    args.resize = function (e, ui) {
        dirt.onAlteration(e);
        // Show a div on top of the textarea to display the size
        sizeDiv.css('position', 'absolute').position({of: $area}).show();
        sizeDiv.text(_('Width: [0]. Height: [1]').interpol(ui.size.width,
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


$('img.TextAreaFieldIcon').hover(function () {
    $(this).attr({src: route_url('root') +
        'static/fieldtypes/TextAreaField/iconHover.png'});
}, function () {
    $(this).attr({src: route_url('root') +
        'static/fieldtypes/TextAreaField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: route_url('root') +
        'static/fieldtypes/TextAreaField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: route_url('root') +
        'static/fieldtypes/TextAreaField/iconHover.png'});
});
