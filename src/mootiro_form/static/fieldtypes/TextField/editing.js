// Constructor
function TextField(props) {
    this.defaultLabel = _('Text field');
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
            minLength: 1, maxLength: 300, enableLength: false,
            minWords : 1, maxWords : 100, enableWords : false
        }
    }
    this.bottomBasicOptionsTemplate = 'TextFieldBottomBasicOptions';
    this.advancedOptionsTemplate = 'TextFieldAdvancedOptions';
    this.previewTemplate = 'TextFieldPreview';
}

TextField.prototype.load = function () {
    // As the page loads, GET the templates file and compile the templates
    $.get('/static/fieldtypes/TextField/text.tmpl.html',
        function (fragment) {
            $('body').append(fragment);
            $.template('TextFieldBottomBasicOptions',
                $('#TextFieldBottomBasicOptions'));
            $.template('TextFieldAdvancedOptions',
                $('#TextFieldAdvancedOptions'));
            $.template('TextFieldPreview', $('#TextFieldPreview'));
        }
    );
}

TextField.prototype.save = function () {
    return textLength.save(this);
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
    // When user clicks on the right side, the Edit tab appears and the
    // corresponding input gets the focus.
    $('#' + this.props.id, this.domNode).click(
        funcForOnClickEdit(this, '#EditDefault'));
};

$('img.TextFieldIcon').hover(function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/TextField/iconHover.png'});
}, function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/TextField/icon.png'});
}).mousedown(function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/TextField/iconActive.png'});
}).mouseup(function () {
    $(this).attr({src: jurl('static') +
        '/fieldtypes/TextField/iconHover.png'});
});
