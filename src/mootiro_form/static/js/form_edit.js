// Like Python dir(). Useful for debugging.
function dir(object) {
    var methods = [];
    for (z in object) {
        if (typeof(z) !== 'number') methods.push(z);
    }
    return methods.join(', ');
}

String.prototype.contains = function (t) {
    return this.indexOf(t) != -1;
}
String.prototype.wordCount = function () {
    var initialBlanks = /^\s+/;
    var leftTrimmed = this.replace(initialBlanks, "");
    var words = leftTrimmed.split(/\s+/);
    // The resulting array may have an empty last element which must be removed
    if (!words[words.length-1])  words.pop();
    return words.length;
}

function positiveIntValidator(s, min) {
    if (typeof(s) === 'number') s = s.toString();
    if (s.contains('.')) return 'Invalid';
    var n = Number(s);
    if (isNaN(n)) return 'Invalid';
    if (min==null) min = 0;
    if (n < min) return 'Minimum is ' + min;
    return '';
}

function methodCaller(o, method, arg) {
    return function () {
        return o[method](arg);
    }
}

// Sets up an input so changes to it are reflected somewhere else
function setupCopyValue(o) { // from, to, defaul, obj, callback
    if (o.defaul==null) o.defaul = '';
    var to = $(o.to);
    to.text($(o.from)[0].value || o.defaul);
    function handler(e) {
        var v = this.value || o.defaul;
        // update value and innerText, but not innerHTML!
        if (to.val) to.val(v);
        if (to.text) to.text(v);
        if (o.callback) {
            o.obj[o.callback](v);
        }
    }
    $(o.from).keyup(handler).change(handler);
}


// Constructor
function Tabs(tabs, contents) {
    $(contents).hide();
    $(contents + ":first").show();
    $(tabs + " li:first").addClass("selected");
    var instance = this;
    this.to = function (tab) { // Most important method, switches to a tab.
        $(contents).hide();
        $(tabs + " li").removeClass("selected");
        $(tab).addClass("selected");
        $($(tab).children().attr("href")).show();
        $('#PanelTitle').text($(tab).children().attr('title'));
    };
    $(tabs + " li").click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
}
// Methods
Tabs.prototype.showNear = function (tabName, domNode) {
    // Changes tabs and shows the panel right besides domNode.
    // If domNode is not passed, the panel position is reset.
    if (!domNode) domNode = $('#RightCol');
    var tab = $('#Tab' + tabName);
    var panel = $('#Panel' + tabName);
    var desiredTop = domNode.position().top - $('#RightCol').position().top;
    panel.css('margin-top', desiredTop);
    this.to(tab);
}


// Object that generates new field IDs
fieldId = {};
fieldId.current = 0;
fieldId.currentString = function () {
    return 'field_' + this.current;
}
fieldId.next = function () {
    return ++this.current;
}
fieldId.nextString = function () {
    this.next();
    return this.currentString();
}


// As the page loads, GET the templates file and compile the templates
$.get(route_url('root') + 'static/fieldtypes/form_edit_templates.html',
    function (fragment) {
        $('body').append(fragment);
        $.template('FieldBase', $('#fieldBaseTemplate'));
        $.template('optionsBase', $('#optionBaseTemplate'));
    }
);

// validate the format of a datestring as isoformat.
function dateValidation(string) {
    if (string) {
        var date = Date.parseExact(string, "yyyy-mm-dd HH:mm");
        if (date) {
            return {date:date, valid:true};
        } else {
            return {msg:
                "Please enter a valid date of the format yyyy-mm-dd hh:mm",
                valid: false};
        }
    } else {
        return {valid: true};
    }
}

// validate whether start date is before end date
function intervalValidation(start_date, end_date) {
    if (start_date < end_date) {
        return "";
    }
    else if (start_date > end_date) {
        return "The start date must be before the end date";
    } else {
        return "";
    }
}


function validatePublishDates() {
    var start_date = $('#start_date').val();
    var end_date = $('#end_date').val();

    var start_date_dict = dateValidation(start_date);
    var end_date_dict = dateValidation(end_date);
    var valid_start_date = start_date_dict['valid'];
    var valid_end_date = end_date_dict['valid'];
    // validate start date
    if (valid_start_date) {
        $('#StartDateError').text('');
    } else {
        $('#StartDateError').text(start_date_dict['msg']);
    }
    // validate end date
    if (valid_end_date) {
        end_date = end_date_dict['date'];
        if (end_date < new Date()) {
            $('#EndDateError').text('The end date must be in the future');
        }
        else {
            $('#EndDateError').text('');
        }
    } else {
        $('#EndDateError').text(end_date_dict['msg']);
    }
    // validate interval
    if (valid_start_date) {
        start_date = start_date_dict['date'];
        if (valid_end_date) {
          $('#IntervalError').text(intervalValidation(start_date, end_date));
        }
    } else {
        $('#IntervalError').text('');
    }
}

// validate publish dates in realtime
$('#start_date, #end_date').keyup(validatePublishDates).change(validatePublishDates);


function onHoverSwitchImage(selector, where, hoverImage, normalImage) {
    $(selector, where).hover(
        function () { $(this).attr({src: hoverImage }); },
        function () { $(this).attr({src: normalImage}); }
    );
}


// Constructor; must be called in the page.
function FieldsManager(formId, json, field_types) {
    var instance = this;

    this.formId = formId;
    this.all = {};
    this.types = {};

    $.each(field_types, function (index, type) {
        instance.types[type] = eval(type);
    });

    this.toDelete = [];
    this.current = null; // the field currently being edited

    var whenReady = function () {
        instance.place = $('#FormFields');
        $.each(json, function (index, props) {
            instance.insert(instance.instantiateField(props));
        });
        instance.formPropsFeedback();
        // this.place.bind('AddField', addField);
        instance.resetPanelEdit();
        // Finally remove this ajaxStop handler since this function is
        // supposed to be executed only once:
        $(document).unbind('ajaxStop', whenReady);
    }

    $(document).ajaxStop(whenReady);

    $.each(this.types, function (type_name, type) {
      if (type.prototype.load) {
          type.prototype.load();
      }
    });
}

FieldsManager.prototype.instantiateField = function (props) {
    // Finds the field type and instantiates it. The argument may be
    // the field type (as a string) or a real properties object.
    var cls;

    if (typeof(props)==='string') {
        cls = this.types[props];
        props = null;
    } else {
        cls = this.types[props.type];
    }
    return new cls(props);
}

FieldsManager.prototype.renderPreview = function (field) {
    // Returns a DOM node containing the rendered field for the right column.
    // If the field implements renderPreview(), use that instead.
    if (field.renderPreview) {
        return field.renderPreview();
    } else {
        var tplContext = {props: field.props, fieldTpl: field.previewTemplate};
        return $.tmpl('FieldBase', tplContext);
    }
}

FieldsManager.prototype.renderOptions = function (field) {
    // Returns a DOM node containing the HTML for the Edit tab.
    // If the field implements renderOptions(), use that instead.
    if (field.renderOptions)
        return field.renderOptions();
    else {
        var tplContext = {props: field.props,
            BottomBasicOptionsTpl: field.bottomBasicOptionsTemplate,
            AdvancedOptionsTpl: field.advancedOptionsTemplate};
        return $.tmpl('optionsBase', tplContext);
    }
}

FieldsManager.prototype.insert = function (field, position) {
    // Renders and displays the passed `field` at `position`.
    // For now, only insert at the end; ignore `position`.
    // If field is a string, that is the field type; create a brand new field
    if (window.console) console.log('insert()');
    if (typeof(field)==='string') {
        field = this.instantiateField(field);
    }
    // `field` is now a real field object.
    this.all[field.props.id] = field;
    field.domNode = this.renderPreview(field);
    this.addBehaviour(field);
    field.domNode.appendTo(this.place); // make appear on the right
    // $.event.trigger('AddField', [field, domNode, position]);
}

FieldsManager.prototype.redrawPreview = function (field) {
    if (window.console) console.log('redrawPreview()');
    if (field.redrawPreview) {
        field.redrawPreview();
    } else {
        var domNode = this.renderPreview(field);
        //field.domNode = this.renderPreview(field);
        // Replace the old node contents:
        $('#' + field.props.id + '_container').html(domNode.html());
        field.domNode = $('#' + field.props.id + '_container');
        this.addBehaviour(field);
    }
}

FieldsManager.prototype.validateCurrent = function () {
    // Returns true if there are no problems in the field currently being edited
    var c = this.current;
    if (c.getErrors) {
        var e = this.current.getErrors();
        for (i in e) {
            if (typeof(e[i])==='string' && e[i]) return false;
        }
    }
    return true;
}

FieldsManager.prototype.saveCurrent = function () {
    if (window.console) console.log('saveCurrent()');
    // If there is no current field, we just don't care:
    if (!this.current)  return true;
    // First validate the alterations to the field.
    if (!this.validateCurrent()) {
        tabs.to('#TabEdit'); // Display the errors so the user gets a hint
        if (confirm('The current field has errors, displayed on ' +
                    'the left column.\nLose your alterations?')) {
            this.redrawPreview(this.current);
            $('#PanelEdit').html(this.renderOptions(this.current));
            return true; // don't save but proceed
        } else {
            return false; // don't save and stop
        }
    }
    // Store (in the client) the information in the left form
    var p = this.current.props;
    p.label = $('#EditLabel').val();
    p.required = $('#EditRequired').attr('checked');
    p.description = $('#EditDescription').val();
    // These are the common attributes; now to the specific ones:
    if (this.current.save)  this.current.save();
    return true;
}

FieldsManager.prototype.switchToEdit = function (field) {
    if (window.console) console.log('switchToEdit()');
    tabs.to('#TabEdit');
    // There is no need to switch to the same field.
    if (field === this.current) return true;
    // First, save the field previously being edited
    if (!this.saveCurrent()) return false;
    if (this.current) {
        this.current.domNode.toggleClass('fieldEditActive', false);
        this.current = null; // for safety, until the end of this method
    }
    // Make `field` visually active at the right
    field.domNode.toggleClass('fieldEditActive', true);
    // Render the field properties at the left
    $('#PanelEdit').html( this.renderOptions(field));
    // TODO: Remove 'magic' position 120
    function scrollWindow() {
        $('html, body').animate({scrollTop: field.domNode.offset().top});
    }
    $('#PanelEdit').animate({'margin-top': field.domNode.offset().top -
        $('#PanelTitle').offset().top - 20}, 200, scrollWindow);
    if (field.showErrors)  field.showErrors();
    // Set the current field, for next click
    this.current = field;
    return true;
}

FieldsManager.prototype.formPropsFeedback = function () {
    setupCopyValue({from:'#deformField1', to:'#DisplayTitle',
        defaul:'Untitled form'});
    setupCopyValue({from:'#deformField2', to:'#DisplayDescription',
        defaul:'Public description of this form'});
    setupCopyValue({from:'#deformField3', to:'#submit',
        defaul:'Submit'});
    $('#submit').click(function () {
        tabs.to('#TabForm');
        $('#deformField3').focus();
    });
}

FieldsManager.prototype.instantFeedback = function () {
    setupCopyValue({from:'#EditLabel',
        to:$('#' + this.current.props.id + 'Label'),
        defaul:'\n'});
    setupCopyValue({from:'#EditDescription', to:'#' + this.current.props.id +
                   'Description', defaul:null});
    var instance = this;
    $('#EditRequired').change(function (e) {
        var origin = $('#EditRequired');
        var dest = $('#' + instance.current.props.id + 'Required');
        if (origin.attr('checked'))
            dest.html('*');
        else
            dest.html('');
    });
    if (this.current.instantFeedback) this.current.instantFeedback();
}

var PanelEditHtmlContent = $('#PanelEdit').html();
FieldsManager.prototype.resetPanelEdit = function () {
    $('#PanelEdit').html(PanelEditHtmlContent);
    this.current = null;
}

FieldsManager.prototype.addBehaviour = function (field) {
    if (window.console) console.log('addBehaviour()');
    $('#' + field.props.id + 'Label', field.domNode)
        .click(funcForOnClickEdit(field, '#EditLabel', field.defaultLabel));
    $('#' + field.props.id + 'Description', field.domNode)
        .click(funcForOnClickEdit(field, '#EditDescription'));
    // Buttons at field right: clone, move, delete
    onHoverSwitchImage('.cloneField', field.domNode,
        route_url('root') + 'static/img/icons-edit/cloneHover.png',
        route_url('root') + 'static/img/icons-edit/clone.png');
    onHoverSwitchImage('.moveField', field.domNode,
        route_url('root') + 'static/img/icons-edit/moveHover.png',
        route_url('root') + 'static/img/icons-edit/move.png');
    onHoverSwitchImage('.deleteField', field.domNode,
        route_url('root') + 'static/img/icons-edit/deleteHover.png',
        route_url('root') + 'static/img/icons-edit/delete.png');
    var instance = this;
    $('.deleteField', field.domNode).click(function () {
        if (field.props.field_id !== 'new') {
            instance.toDelete.push(field.props.field_id);
        }
        field.domNode.remove();
        delete instance.all[field.props.id];
        // If the field being deleted is the current field, remove its
        // properties from the left column.
        if (field === instance.current) instance.resetPanelEdit();
    });
    if (field.addBehaviour)  field.addBehaviour();
};

FieldsManager.prototype.persist = function () {
    if (window.console) console.log('persist()');
    // Saves the whole form, through an AJAX request.
    // First, save the field previously being edited
    if (!this.saveCurrent()) return false;
    /* Prepare form fields */
    var ff = [];
    $.each(this.all, function (id, field) {
        ff.push(field.props);
    });
    /* Prepare form properties */
    var json = {};
    json.fields = ff;
    json.form_id = this.formId || 'new';
    json.form_desc = $('textarea[name=description]').val();
    json.form_title = $('input[name=name]').val();
    json.submit_label = $('input[name=submit_label]').val();
    json.start_date = $('#start_date').val();
    json.end_date = $('#end_date').val();
    json.form_public = $('input[name=public]').attr('checked');
    json.form_thanks_message = $('textarea[name=thanks_message]').val();
    json.deleteFields = this.toDelete;
    json.fields_position = $('#FormFields').sortable('toArray');
    // POST and set 2 callbacks: success and error.
    var instance = this;
    var jsonRequest = {json: $.toJSON(json)};
    var url = route_url('form', {action:'edit', id: json.form_id});
    $.post(url, jsonRequest)
    .success(function (data) {
        if (data.field_validation_error) {
          alert("Sorry, error updating fields on the server.\n" +
            "Your form has NOT been saved.\n" + data.field_validation_error);
          return false;
        }
        if (data.panel_form) {
            $('#PropertiesForm').html(data.panel_form);
            instance.formPropsFeedback();
        }
        if (data.error) {
            tabs.to('#TabForm');
            alert("Sorry, your alterations have NOT been saved.\nPlease " +
                  "correct the errors as proposed in the highlighted text.")
        }
        if (data.publish_error) {
            tabs.to('#TabPublish');
            $('#StartDateError').text(data.publish_error['interval.start_date']
              || '');
            $('#EndDateError').text(data.publish_error['interval.end_date']
              || '');
            $('#IntervalError').text(data.publish_error.interval || '');
            alert("Sorry, your alterations have NOT been saved.\n" +
              "Please correct the errors as proposed in the highlighted text.");
        } else {
            instance.formId = data.form_id;
            /* When the user clicks on save multiple times, this
             * prevents us from adding a new field more than once. */
            $.each(data.new_fields_id, function (f_idx, f) {
                instance.all[f_idx].props.field_id = f.field_id;
            });
            $.each(data.save_options_result, function (f_idx, f) {
                instance.all[f_idx].update(f);
            });
            // Assume any deleted fields have been deleted at the DB
            instance.toDelete = [];
            // Show the generated public link
            if (data.form_public_url)
                $('#form_public_url').attr('value', data.form_public_url);
        }
    })
    .error(function (data) {
        alert("Sorry, error updating fields on the server.\n" +
            "Your form has NOT been saved.\n" +
            "Status: " + data.status); // + "\n" + data.responseText);
    });
    return true;
}


// When user clicks on the right side, the Edit tab appears and the
// corresponding input gets the focus.
function funcForOnClickEdit(field, target, defaul) {
    return function () {
        if (!fields.switchToEdit(field))  return false;
        fields.instantFeedback();
        $(target).focus();
        // Sometimes also select the text. (If it is the default value.)
        if ($(target).val() === defaul) $(target).select();
        return false;
    };
}


// Object that shares code between Text and TextArea fields,
textLength = {};  // especially for char and word length validation.
textLength.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    var minLength = $('#EditMinLength').val();
    var maxLength = $('#EditMaxLength').val();
    var minWords = $('#EditMinWords').val();
    var maxWords = $('#EditMaxWords').val();
    errors.minLength = positiveIntValidator(minLength, 1);
    errors.maxLength = positiveIntValidator(maxLength, 1);
    errors.minWords = positiveIntValidator(minWords, 1);
    errors.maxWords = positiveIntValidator(maxWords, 1);
    // Only now convert to number, to further validate
    minLength = Number(minLength);
    maxLength = Number(maxLength);
    minWords = Number(minWords);
    maxWords = Number(maxWords);
    if (!errors.maxLength && minLength > maxLength)
        errors.minLength = 'Higher than max';
    if (!errors.maxWords && minWords > maxWords)
        errors.minWords = 'Higher than max';
    var defaul = $('#EditDefault').val();
    var lendefault = defaul.length;
    var enableWords = $('#EnableWords').attr('checked');
    var enableLength = $('#EnableLength').attr('checked');
    if (lendefault && enableLength) {
        if (minLength > lendefault) errors.defaul += 'Shorter than min length. ';
        if (maxLength < lendefault) errors.defaul += 'Longer than max length. ';
    }
    if (lendefault && enableWords) {
        var words = defaul.wordCount();
        if (minWords > words) errors.defaul += 'Shorter than min words.';
        if (maxWords < words) errors.defaul += 'Longer than max words.';
    }
    return errors;
}
textLength.showErrors = function (errors) {
    if (!errors) errors = this.getErrors();
    $('#ErrorDefault').text(errors.defaul);
    $('#ErrorMinWords').text(errors.minWords);
    $('#ErrorMaxWords').text(errors.maxWords);
    $('#ErrorMinLength').text(errors.minLength);
    $('#ErrorMaxLength').text(errors.maxLength);
}
textLength.instantFeedback = function (field) {
    setupCopyValue({from: '#EditDefault', to: '#' + field.props.id,
        obj: field, callback: 'showErrors'});
    var h = methodCaller(field, 'showErrors');
    $('input.LengthEdit').keyup(h).change(h);
    $('#EnableLength').change(h);
    $('#EnableWords').change(h);
    // Display length options when "Specify length" is clicked
    collapsable({divSelector: '#LengthProps'});
}
textLength.save = function (field) {
    var p = field.props;
    p.defaul = $('#EditDefault').val();
    p.maxWords = $('#EditMaxWords').val();
    p.minWords = $('#EditMinWords').val();
    p.maxLength = $('#EditMaxLength').val();
    p.minLength = $('#EditMinLength').val();
    p.enableWords = $('#EnableWords').attr('checked');
    p.enableLength = $('#EnableLength').attr('checked');
}


collapsable = function (o) {
    // Makes a div appear collapsed; it expands when user clicks on the handle.
    // Adds a dynamic triangular icon to the left of the handle.
    // The argument is an options object which may contain:
    // divSelector (required), handleSelector, iconCollapsed, iconCollapsable.
    if (!o.handleSelector)  o.handleSelector = o.divSelector + 'Handle';
    var handle = $(o.handleSelector);

    // If a method is already there, this function has already run, so do nothing.
    if (handle[0].toggleIcon)  return;

    var div = $(o.divSelector);
    div.hide();
    handle.addClass('Collapser');
    handle.html("<span class='CollapserIcon'>\u25b6</span> " + handle.html());
    var icon = $('span.CollapserIcon', handle);
    if (!o.iconCollapsed)   o.iconCollapsed = '\u25b6';  // '▶';
    if (!o.iconCollapsable) o.iconCollapsable = '\u25bc'; // ▼
    handle.toggleIcon = handle[0].toggleIcon = function () {
        if (icon.text() == o.iconCollapsed)
            icon.text(o.iconCollapsable);
        else
            icon.text(o.iconCollapsed);
    };
    handle.click(function () {
        div.slideToggle();
        handle[0].toggleIcon();
    });
}

// Initialization of the form editor... on DOM ready:
$(function () {
    $('#SaveForm').click(function (e) { fields.persist(); });
    tabs = new Tabs('.ui-tabs-nav', '.ui-tabs-panel');
    $('#FormFields').sortable({
        placeholder: 'fieldSpace',
        forcePlaceholderSize: true,
        handle: '.moveField',
        containment: 'document',
        stop: movePanel});
    $("#form_public_url").click(function(){
        this.select();
    });
    // The start and end date datetimepicker of the publish tab. First line is
    // necessary to disable automated positioning of the widget.
    $.extend($.datepicker,
        {_checkOffset: function (inst,offset,isFixed) { return offset; }});
    $('#start_date').datetimepicker({
        dateFormat: 'yy-mm-dd',
        timeFormat: 'hh:mm',
        hour: 00,
        minute: 00,
        beforeShow: function(input, inst) {
          inst.dpDiv.addClass('ToTheRight');
        }
    });
    $('#end_date').datetimepicker({
        dateFormat: 'yy-mm-dd',
        timeFormat: 'hh:mm',
        hour: 23,
        minute: 59,
        beforeShow: function(input, inst) {
            inst.dpDiv.addClass('ToTheRight');
        }
    });

    // The "add field" button, at the bottom left, must show icons besides the
    // field currently being edited.
    $('#AddField').click(function () {
        if (fields.current)
            tabs.showNear('Add', fields.current.domNode);
        else
            tabs.showNear('Add');
    });
    // The "Add field" tab, when clicked, must show its contents at the TOP.
    $('#TabAdd').unbind().click(function () {
        tabs.showNear('Add');
    });
});

// Moves the panel close to the field being edited
function movePanel(event, ui) {
    if (!fields.current)  return false;
    $('#PanelEdit').animate({'margin-top': fields.current.domNode.offset().top
        - $('#PanelTitle').offset().top - 20});
}
